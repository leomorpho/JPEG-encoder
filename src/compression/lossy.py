from typing import List

# TODO: implement JPEG
# TODO: implement GMM


def downsample(image: List[List[int]]):
    pass


def JPEG(image):
    layers = separate_image_layers(image)

    for layer in layers:
        blocked_layer = block_split_layer(layer)


def separate_image_layers(image: List[List[int]]) -> List[List[List[int]]]:
    """Divide the in Y, Cb and Cr layers
    """
    # Split the Y, Cb and Cr layers into 8x8 pixel blocks
    Y_layer = []
    Cb_layer = []
    Cr_layer = []

    for row in image:
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


# Call DCT on every block
# Quantize every block
# Zigzag entropy code
