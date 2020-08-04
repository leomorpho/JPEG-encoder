from typing import List


def RGB_to_YCbCr(rgb: List[int]) -> List[int]:
    """Convert RGB to YCbCr"""
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]

    Y = int(0.299 * red) + (0.587 * green) + (0.114 * blue)
    Cb = int(128 - (0.168736 * red) - (0.331264 * green) + (0.5 * blue))
    Cr = int(128 + (0.5 * red) - (0.418688 * green) - (0.081312 * blue))

    return [Y, Cb, Cr]


def YCbCr_to_RGB(YCbCr: List[int]) -> List[int]:
    """Convert YCbCr to RGB"""
    Y = YCbCr[0]
    Cb = YCbCr[1]
    Cr = YCbCr[2]

    red = int(Y + 1.402 * (Cr - 128))
    green = int(Y - 0.344136 * (Cb - 128) - 0.714136 * (Cr - 128))
    blue = int(Y + 1.772 * (Cb - 128))

    if red > 255:
        red = 255
    if red < 0:
        red = 0

    if green > 255:
        green = 255
    if green < 0:
        green = 0

    if blue > 255:
        blue = 255
    if blue < 0:
        blue = 0

    return [red, green, blue]


def image_RGB_to_YCbCr(image: List[List[List[int]]]) -> List[List[List[int]]]:
    YCbCr_image = []
    for row in image:
        YCbCr_row = []
        for pixel in row:
            YCbCr_row.append(RGB_to_YCbCr(pixel))
        YCbCr_image.append(YCbCr_row)

    return YCbCr_image


def image_YCbCr_to_RGB(image: List[List[List[int]]]) -> List[List[List[int]]]:
    RGB_image = []
    for row in image:
        RGB_row = []
        for pixel in row:
            RGB_row.append(YCbCr_to_RGB(pixel))
        RGB_image.append(RGB_row)

    return RGB_image
