import pytest
import logging
from src.compression.lossless import LZWEncoder

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, input_val, output_val, compression_ratio):
        self.name = name
        self.input_val = input_val
        self.output_val = output_val
        self.compression_ratio = compression_ratio


test_lzw = [
    InputOutputCase(
        name="From notes. Result will be different because starting dict is different",
        input_val=[1, 10],
        output_val=['0', '1'],
        compression_ratio=4.0
    ),
    InputOutputCase(
        name="From notes",
        input_val=[123, 123, 100, 100, 100, 100, 99, 99, 50, 10],
        output_val=['0', '0', '1', '7', '1', '2', '2', '3', '4'],
        compression_ratio=20.0
    ),
]


@pytest.mark.parametrize("case", test_lzw)
def test_lzw(case):
    """Test calculate 2nd order entropy from sentence"""
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    lzw = LZWEncoder()
    result = lzw.encode(case.input_val)
    cr = lzw.compression_ratio()

    log.debug("Result: " + str(result))
    assert(result == case.output_val)
    assert(cr == case.compression_ratio)

