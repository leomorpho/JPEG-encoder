import pytest
import logging
from src.compression.quantization import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with non_quantized and expected quantized"""

    def __init__(self, name, non_quantized, quantized):
        self.name = name
        self.non_quantized = non_quantized
        self.quantized = quantized

#########################################
#                                       #
# Quantization                          #
#                                       #
#########################################


test_quantization_cases = [
    InputOutputCase(
        name="Nominal",
        non_quantized=[
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 130, 99]
        ],
        quantized=[
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


@pytest.mark.parametrize("case", test_quantization_cases)
def test_quantize(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.non_quantized))

    result = quantize(case.non_quantized)

    log.debug("Result: " + str(result))
    assert(result == case.quantized)

#########################################
#                                       #
# Dequantization                          #
#                                       #
#########################################

@pytest.mark.parametrize("case", test_quantization_cases)
def test_dequantize(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.non_quantized))

    result = dequantize(case.quantized)

    log.debug("Result: " + str(result))
    assert(result == case.quantized)
