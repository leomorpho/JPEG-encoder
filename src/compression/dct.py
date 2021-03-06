import math
from typing import List
import logging
import scipy

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ZERO_CENTERING_VAL = 128


def dct_forward(block: List[List[int]]) -> List[List[int]]:
    """Perform Discrete Cosine Transform on an 8x8 block
    """
    # Perform DCT in 2 parts, first for rows, then for columns
    log.info("Run DCT on block")

    # Center data on zero before DCT and perform DCT on every row
    for index, row in enumerate(block):
        row = [val - ZERO_CENTERING_VAL for val in row]
        block[index] = scipy.fft.dct(row)

    # Perform DCT over every column
    for i in range(len(block)):
        col_vector = []
        # Create column vector
        for j in range(len(block)):      # TODO: is access by index faster than iteration?
            col_vector.append(block[j][i])

        col_vector = scipy.fft.dct(col_vector)

        # Set results to block
        for j in range(len(block)):      # TODO: is access by index faster than iteration?
            block[j][i] = col_vector[j]

    return block


def dct_inverse(block: List[List[int]]) -> List[List[int]]:
    """Perform reverse Discrete Cosine Transform on an 8x8 block
    """
    # Perform DCT in 2 parts, first for columns, then for rows
    log.info("Run inverse DCT on block")

    # Perform DCT over every column
    for i in range(len(block)):
        col_vector = []
        # Create column vector
        for j in range(len(block)):      # TODO: is access by index faster than iteration?
            col_vector.append(block[j][i])

        col_vector = scipy.fft.idct(col_vector)

        # Set results to block
        for j in range(len(block)):      # TODO: is access by index faster than iteration?
            block[j][i] = int(col_vector[j])

    # Perform DCT over every row
    for index, row in enumerate(block):
        block[index] = [int(x) for x in scipy.fft.idct(row)]

    # Reverse the centering on zero that was run before forward DCT.
    # For every row and every member of the row.
    for i, row in enumerate(block):
        for j, val in enumerate(row):
            block[i][j] = val + ZERO_CENTERING_VAL

    return block


# DCT type II, unscaled.
# See: https://en.wikipedia.org/wiki/Discrete_cosine_transform#DCT-II
def transform(vector):
    result = []
    factor = math.pi / len(vector)
    for i in range(len(vector)):
        sum = 0.0
        for (j, val) in enumerate(vector):
            sum += val * math.cos((j + 0.5) * i * factor)
        result.append(sum)
    return result


# DCT type III, unscaled.
# See: https://en.wikipedia.org/wiki/Discrete_cosine_transform#DCT-III
def inverse_transform(vector):
    result = []
    factor = math.pi / len(vector)
    for i in range(len(vector)):
        sum = vector[0] / 2
        for j in range(1, len(vector)):
            sum += vector[j] * math.cos(j * (i + 0.5) * factor)
        result.append(sum)
    return result
