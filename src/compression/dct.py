import math
from typing import List


def dct(block: List[List[int]], inverse=False) -> List[List[int]]:
    """Perform Discrete Cosine Transform on an 8x8 block
    """
    # Perform DCT in 2 parts, first for rows, then for columns

    # Center data on zero before DCT and perform DCT on every row
    for row in block:
        row = [val - 128 for val in row]
        if inverse:
            row = inverse_transform(row)
        else:
            row = transform(row)
        row = transform(row)

    # Perform DCT over every column
    for i in range(len(block)):
        col_vector = []
        # Create column vector
        for j in range(len(block)):      # TODO: is access by index faster than iteration?
            col_vector.append(block[j][i])

        if inverse:
            col_vector = inverse_transform(col_vector)
        else:
            col_vector = transform(col_vector)

        # Set results to block
        for j in range(len(block)):      # TODO: is access by index faster than iteration?
            block[j][i] = col_vector[j]

    return block


#TODO: rewrite DCT in my own code.

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
