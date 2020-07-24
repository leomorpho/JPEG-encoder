import pytest
import logging
from src.compression.dct import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, input_val):
        self.name = name
        self.input_val = input_val

#########################################
#                                       #
# DCT II (forward)                      #
#                                       #
#########################################


test_dct = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 130, 99]
        ]
    )
]

@pytest.mark.parametrize("case", test_dct)
def test_dct(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    block = dct_forward(case.input_val)

    log.debug("Result: " + str(block))
    for i in range(8):
        for j in range(8):
            assert(type(block[i][j] == int))

#########################################
#                                       #
# DCT III (backward)                    #
#                                       #
#########################################


test_dct_inverse = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 130, 99]
        ]
    )
]


@pytest.mark.parametrize("case", test_dct_inverse)
def test_dct(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    block = dct_inverse(case.input_val)

    log.debug("Result: " + str(block))
    for i in range(8):
        for j in range(8):
            assert(type(block[i][j] == int))
