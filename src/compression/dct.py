from typing import List


def dct(block: List[List[int]]):
    """Perform Discrete Cosine Transform on an 8x8 block
    """
    # Center data on zero before DCT
    for row in block:
        row = [val - 128 for val in row]

    # The basic implementation of DCT taken from https://www.nayuki.io/res/fast-discrete-cosine-transform-algorithms/naivedct.py
