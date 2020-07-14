import pytest
import logging
from src.compression.quantization import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, input_val, expected_output):
        self.name = name
        self.input_val = input_val
        self.expected_output = expected_output

#########################################
#                                       #
# Quantization                          #
#                                       #
#########################################


test_quantize = [
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
        ],
        expected_output=[
            # The 8x8 square of values become a "single value" at (0, 0)
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
    )
]


@pytest.mark.parametrize("case", test_quantize)
def test_quantize(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = quantize(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)

#########################################
#                                       #
# Dequantization                          #
#                                       #
#########################################


test_dequantize = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ],
        expected_output=[
            # The 8x8 square of values become a "single value" at (0, 0)
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


@pytest.mark.parametrize("case", test_dequantize)
def test_dequantize(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = dequantize(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)
