import pytest
import logging
from src.codecs.image import IMGFile

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
# JPEG encoder-decoder                  #
#                                       #
#########################################


# 3 layers of vectors for Y, Cb, Cr
test_encode_cases = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [[123, 123], [123, 123]],
            [[123, 143], [123, 123]],
            [[123, 143], [123, 123]],
        ],
        expected_output=[
        ]
    )
]


@pytest.mark.parametrize("case", test_encode_cases)
def test_encode(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    im = IMGFile()
    result = im.encode(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)
