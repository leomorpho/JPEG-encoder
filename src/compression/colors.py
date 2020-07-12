from typing import List

def RGB_to_YCbCr(rgb: List[int]) -> List[int]:
    """Convert RGB to YCbCr"""
    red = rgb[0]
    green = rgb[1]
    blue = rgb[3]

    Y = int(0.299 * red) + (0.587 * green) + (0.114 * blue)
    Cb = int(128 - (0.168736 * red) - (0.331264 * green) + (0.5 * blue))
    Cr = int(128 + (0.5 * red) - (0.418688 * green) - (0.081312 * blue))

    return [Y, Cb, Cr]

def RGB_to_YCbCr(YCbCr: List[int]) -> List[int]:
    """Convert YCbCr to RGB"""
    Y = YCbCr[0]
    Cb = YCbCr[1]
    Cr = YCbCr[2]

    red = int(Y + 1.402 * (Cr- 128))
    green = int(Y - 0.344136 * (Cb - 128) - 0.714136 * (Cr - 128))
    blue = int(Y + 1.772 * (Cb - 128))
