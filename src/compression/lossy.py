from typing import List
import logging
import sys
import math
import time
from src.compression.dct import dct_forward, dct_inverse
from src.compression.quantization import quantize, dequantize
from src.compression.zigzag import zigzag, un_zigzag
from src.codecs import image
from src.compression import colors
from src.compression.lossless import HuffmanEncoder

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# TODO: implement GMM

JPEG_SUPPORTED_ENCODING_FORMATS = {"bmp"}
PIXEL_MAX = 255


def downsample(image: List[List[List[int]]]):
    pass


def JPEG(original_image: List[List[List[int]]],
        compression_level: int,
        path: str,
        width: int,
        height: int) -> List[List[List[int]]]:
    """Encode in JPEG-like format and return the decoded image
    """
    start = time.time()
    print(f"Encoding image to JPEG with {compression_level}% compression")
    he = HuffmanEncoder()

    # Convert to YCbCr
    print("Logging these pixels for debugging.")
    original_image = colors.image_RGB_to_YCbCr(original_image)
    print(original_image[100][100])

    # Separate into Y, Cb, Cr layers
    layers: List[List[List[int]]] = separate_image_layers(original_image)

    # Hold zigzaged layers which are ready to be Huffman encoded and
    # persisted to disk.
    layers_zigzagged = []

    # Make new copy for JPEG version
    for layer in layers:
        blocked_layer = block_split_layer(layer)
        blocked_layer_zigzagged = []

        for row in blocked_layer:
            blocked_row_vector = []
            for block in row:
                # Encode
                block = dct_forward(block)
                block = quantize(block, compression_level=compression_level)
                vector = zigzag(block)
                blocked_row_vector.append(vector.copy())

            blocked_layer_zigzagged.append(blocked_row_vector)
        layers_zigzagged.append(blocked_layer_zigzagged)

    im = image.IMGFile()
    im.height = height
    im.width = width
    im.compression = compression_level
    im.encode(layers_zigzagged)
    filepath = path.split(".")[0] + ".img"
    im.write(filepath)

    end = time.time()
    compression_time = end - start
    start = time.time()

    im.read(filepath)
    decoded_layers_zigzagged = im.decode()

    assert(layers_zigzagged == decoded_layers_zigzagged)

    end = time.time()
    decompression_time = end - start

    return read_JPEG(decoded_layers_zigzagged, compression_level), im.bytes_size, compression_time, decompression_time


def read_JPEG(layers, compression_lvl: int =None):
    """
    Layers start zigzagged
    """
    decompressed_layers = []
    print(f"Decoding JPEG with {compression_lvl}% compression")

    # Make new copy for JPEG version
    for i_layer, layer in enumerate(layers):
        blocked_layer = []
        for i_row, row in enumerate(layer):
            decompressed_row = []
            for i_vector, vector in enumerate(row):
                # Decode
                block = un_zigzag(vector)
                block = dequantize(block, compression_lvl)
                block = dct_inverse(block)
                # Update block in row
                decompressed_row.append(block)
            blocked_layer.append(decompressed_row)
        decompressed_layer = block_join_layer(blocked_layer)
        decompressed_layers.append(decompressed_layer)

    # Should be split in layers
    assert(decompressed_layers[0])
    assert(decompressed_layers[1])
    assert(decompressed_layers[2])

    final_image = join_image_layers(decompressed_layers)
    print(final_image[100][100])

    # Convert to RGB
    final_image = colors.image_YCbCr_to_RGB(final_image)
    print(final_image[100][100])

    return final_image


def separate_image_layers(image: List[List[List[int]]]) -> List[List[List[int]]]:
    """Divide the in Y, Cb and Cr layers
    """
    # Split the Y, Cb and Cr layers into 8x8 pixel blocks
    Y_layer = []
    Cb_layer = []
    Cr_layer = []

    for row in image:
        log.debug(row)
        Y_layer_row = []
        Cb_layer_row = []
        Cr_layer_row = []

        for YCbCr in row:
            Y_layer_row.append(YCbCr[0])
            Cb_layer_row.append(YCbCr[1])
            Cr_layer_row.append(YCbCr[2])

        Y_layer.append(Y_layer_row)
        Cb_layer.append(Cb_layer_row)
        Cr_layer.append(Cr_layer_row)

    return [Y_layer, Cb_layer, Cr_layer]


def join_image_layers(layers: List[List[List[int]]]) -> List[List[List[int]]]:
    """Join the Y, Cb, Cr layers into a single image
    """
    # Create image matrix with the same number of rows as there are in a layer.
    # For each row, add a list for every value in the layer's row. This is for (Y,Cb, Cr).
    image = [[[] for j in range(len(layers[0][0]))]
             for i in range(len(layers[0]))]

    for layer in layers:
        for row_index, row in enumerate(layer):
            for col_index, col in enumerate(row):
                image[row_index][col_index].append(col)

    return image


def block_split_layer(layer: List[List[int]], block_size=8):
    """
    Split the layer into blocks

    :param layer: the layer to split
    :param block_size: the size of the blocks to split the layer to
    """

    # If not enough values to create a block of the reruired size,
    # repeat closest values
    blocked_layer = []

    layer_width = len(layer[0])
    layer_height = len(layer)
    log.debug(f"Layer w x h: {layer_width} x {layer_height}")

    # Top of image is at 0, 0, which is the top-left corner of the actual image.
    x_layer, y_layer = 0, 0

    blocked_row = []
    while True:
        # Create empty row

        # Allocate new empty 8x8 block
        block = [[0 for i in range(block_size)] for i in range(block_size)]

        # Get square block
        for y_curr in range(y_layer, y_layer + block_size):
            for x_curr in range(x_layer, x_layer + block_size):
                # x and y are inversed in this representation. A row is a y-coordinate. Items
                # within a row are x-coordinate.
                try:
                    block[y_curr - y_layer][x_curr -
                                            x_layer] = layer[y_curr][x_curr]
                # If not enough values for 8x8 block, repeat last value.
                except IndexError:
                    # log.debug(f"x_curr: {x_curr}, y_curr: {y_curr}")
                    # Block intersects lower right corner of image
                    if x_curr >= layer_width and y_curr >= layer_height:
                        # log.debug("Block intersects right bottom corner of image")
                        block[y_curr - y_layer][x_curr -
                                                x_layer] = layer[layer_height - 1][layer_width - 1]
                    # Block intersects right edge of image
                    elif x_curr >= layer_width:
                        # log.debug("Block intersects right edge of image")
                        block[y_curr - y_layer][x_curr -
                                                x_layer] = layer[y_curr][layer_width - 1]
                    # Block intersects bottom edge of image
                    else:
                        # log.debug("Block intersects bottom edge of image")
                        block[y_curr - y_layer][x_curr -
                                                x_layer] = layer[layer_height - 1][x_curr]

        # log.debug(block)
        # Add block to row
        blocked_row.append(block)

        # Shift top-left corner of "block" window to the right
        x_layer += block_size

        # Test to see if we reached right edge of picture
        shift_down = False
        try:
            layer[y_layer][x_layer]
        except IndexError:
            shift_down = True

        if shift_down:
            shift_down = False
            # Add row to blocked layer
            blocked_layer.append(blocked_row)
            blocked_row = []

            # Shift block top-left origin down
            y_layer += block_size

            # Reset x-coordinate to left edge
            x_layer = 0

            # Test to see if we reached bottom of picture
            try:
                layer[y_layer][x_layer]
            except IndexError:
                break

    return blocked_layer


def block_join_layer(blocked_layer: List[List[int]]):
    """Join 8x8 blocks into a layer. This is the inverse operation
    of block_split_layer
    :param layer: the layer to split
    """
    # Structure of blocked_layer:
    # [[block, block],
    #  [block, block]]

    row_size = len(blocked_layer[0][0])

    # (1) Merge all blocks horizontally
    # Enumerate over ALL blocks
    horizontally_merged_blocks = []
    for blocks_row in blocked_layer:
        # Join blocks which are in the same row.
        joined_block_rows = [[] for i in range(row_size)]

        for block in blocks_row:

            # Enumerate over x, y of a block
            for block_row_index, block_row in enumerate(block):
                joined_block_rows[block_row_index].extend(block_row)
        log.debug(joined_block_rows)

        horizontally_merged_blocks.append(joined_block_rows)

    # (2) Merge all block rows vertically
    # Structure of blocked_layer:
    # [
    #   [
    #     [row], [row]
    #   ],
    #   [
    #     [row], [row]
    #   ],
    # ]
    layer = []
    for row_array in horizontally_merged_blocks:
        for row in row_array:
            layer.append(row)

    return layer


def PSNR(original: List[List[List[int]]], compressed: List[List[List[int]]]):
    height = len(original)
    width = len(original[0])

    sum_of_squares = 0.0

    for i in range(height):
        for j in range(width):
            R = (original[i][j][0] - compressed[i][i][0]) ** 2
            G = (original[i][j][1] - compressed[i][i][1]) ** 2
            B = (original[i][j][2] - compressed[i][i][2]) ** 2

            sum_of_squares += ((R + G + B) / 3)

    mse = (1 / (height * width)) * sum_of_squares

    return 20 * math.log10(PIXEL_MAX) - 10 * math.log10(mse)
