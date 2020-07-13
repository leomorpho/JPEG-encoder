from typing import List
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# TODO: implement JPEG
# TODO: implement GMM


def downsample(image: List[List[List[int]]]):
    pass


def JPEG(image: List[List[List[int]]]) -> List[List[List[int]]]:
    """Encode in JPEG-like format and return the decoded encoded image
    """
    # Separate into Y, Cb, Cr layers
    layers: List[List[List[int]]] = separate_image_layers(image)

    # Split into 8x8 blocks
    block_split_layers = []
    for layer in layers:
        block_split_layers.append(block_split_layer(layer))

        # Call DCT on every block
        # Quantize every block
        # Zigzag entropy code

        # Save file

        # De-encode Huffman
        # Dequantize every block
        # Call DCT inverse on every block

        # Join 8x8 blocks
        block_join_layer()

    # Join Y, Cb, Cr layers
    image: List[List[List[int]]] = join_image_layers(layers)

    return image


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
    image = [[[] for j in len(layers[0][0])] for i in len(layers[0])]

    for layer in layers:
        for row_index, row in enumerate(layer):
            for col_index, col in enumerate(row):
                image[row_index][col_index].append(col)

    return image


def block_split_layer(layer: List[List[int]]):
    """Split the layer into 8x8 blocks
    """
    # If not enough values to create an 8x8 block, repeat closest values
    blocked_layer = []

    layer_width = len(layer[0])
    layer_height = len(layer)

    # Top of image is at 0, 0, which is the top-left corner of the actual image.
    x_layer, y_layer = 0, 0

    while True:
        # Create empty row
        blocked_row = []

        # Allocate new empty 8x8 block
        block = [[0 for i in range(8)] for i in range(8)]

        for y_curr in range(y_layer, y_layer + 8):
            for x_curr in range(x_layer, x_layer + 8):
                # x and y are inversed in this representation. A row is a y-coordinate. Items
                # within a row are x-coordinate.
                try:
                    block[y_curr - y_layer][x_curr -
                                            x_layer] = layer[y_curr][x_curr]
                # If not enough values for 8x8 block, repeat last value.
                except IndexError:
                    # Block intersects lower right corner
                    if x_curr > layer_width and y_curr > layer_height:
                        block[y_curr - y_layer][x_curr -
                                                x_layer] = layer[layer_height - 1][layer_width - 1]
                    # Block intersects right edge of image
                    elif x_curr > layer_width:
                        block[y_curr - y_layer][x_curr -
                                                x_layer] = layer[y_curr][layer_width - 1]
                    # Block intersects bottom edge of image
                    else:
                        block[y_curr - y_layer][x_curr -
                                                x_layer] = layer[layer_height - 1][x_curr]

        # Add block to row
        blocked_row.append(block)

        # Shift top-left corner of "block" window to the right
        x_layer += 8

        # Test to see if we reached right edge of picture
        try:
            layer[y_layer][x_layer]
        except IndexError:
            shift_down = True

        if shift_down:
            # Add row to blocked layer
            blocked_layer.append(blocked_row)

            # Shift block top-left origin down
            y_layer += 8

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
    """
    # Structure of blocked_layer:
    # [[block, block],
    #  [block, block]]

    # (1) Merge all blocks horizontally
    # Enumerate over ALL blocks
    horizontally_merged_blocks = []
    for blocks_row in blocked_layer:
        # Join blocks which are in the same row.
        # It should be 8 heigh by (8 x number of blocks) long.
        joined_block_rows = [[] for i in range(8)]
        for block in blocks_row:

            # Enumerate over x, y of a block
            for block_row_index, block_row in enumerate(block):
                joined_block_rows[block_row_index].extend(block_row)

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
