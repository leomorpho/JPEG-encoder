from typing import List
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Find tables at p.284 of Professor's book
# TODO: special quantization for chroma not implemented yet.
chrominance = [[]]

Q10 = [[80, 60, 50, 80, 120, 200, 255, 255],
       [55, 60, 70, 95, 130, 255, 255, 255],
       [70, 65, 80, 120, 200, 255, 255, 255],
       [70, 85, 110, 145, 255, 255, 255, 255],
       [90, 110, 185, 255, 255, 255, 255, 255],
       [120, 175, 255, 255, 255, 255, 255, 255],
       [245, 255, 255, 255, 255, 255, 255, 255],
       [255, 255, 255, 255, 255, 255, 255, 255]]

Q50 = [[16, 11, 10, 16, 24, 40, 51, 61],
       [12, 12, 14, 19, 26, 58, 60, 55],
       [14, 13, 16, 24, 40, 57, 69, 56],
       [14, 17, 22, 29, 51, 87, 80, 62],
       [18, 22, 37, 56, 68, 109, 103, 77],
       [24, 35, 55, 64, 81, 104, 113, 92],
       [49, 64, 78, 87, 103, 121, 120, 101],
       [72, 92, 95, 98, 112, 100, 130, 99]]

Q90 = [[3, 2, 2, 3, 5, 8, 10, 12],
       [2, 2, 3, 4, 5, 12, 12, 11],
       [3, 3, 3, 5, 8, 11, 14, 11],
       [3, 3, 4, 6, 10, 17, 16, 12],
       [4, 4, 7, 11, 14, 22, 21, 15],
       [5, 7, 11, 13, 16, 12, 23, 18],
       [10, 13, 16, 17, 21, 24, 24, 21],
       [14, 18, 19, 20, 22, 20, 20, 20]]



def quantize(block: List[List[int]], compression_level, chroma=False):
    """
    Quantize a block.

    :param block: an 8x8 block of integer values
    :param quantization_matrix: the quantization matrix to use
    :param chroma: whether to use chroma quantization table or not. TODO.
    """

    quantization_matrix = get_quantization_matrix(compression_level)

    # Divide every value in the block by the corresponding value
    # in the quantization matrix (aka, same x, y indices)
    log.info("Quantize block")
    for x in range(8):
        for y in range(8):
            block[y][x] = int(block[y][x] / quantization_matrix[y][x])

    return block

def dequantize(block: List[List[int]], compression_level: int, chroma=False):
    """
    Dequantize a block.

    :param block: an 8x8 block of integer values
    :param quantization_matrix: the quantization matrix to use
    :param chroma: whether to use chroma quantization table or not
    """
    quantization_matrix = get_quantization_matrix(compression_level)

    log.info("Dequantize block")
    # Multiply every value in the block by the corresponding value
    # in the quantization matrix (aka, same x, y indices)
    for x in range(8):
        for y in range(8):
            block[y][x] = int(block[y][x] * quantization_matrix[y][x])

    return block

def get_quantization_matrix(level):
    if level == 90:
        return Q90
    elif level == 50:
        return Q50
    elif level == 10:
        return Q10
    else:
        raise Exception("Quantization level not supported")
