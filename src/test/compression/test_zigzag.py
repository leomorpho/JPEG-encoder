
import pytest
import logging
from src.compression.zigzag import *

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
#   Zigzag                              #
#                                       #
#########################################

test_zigzag = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [16, 11],
            [12, 12],
        ],
        expected_output=[16, 11, 12, 12]
    ),
    InputOutputCase(
        name="Nominal",
        input_val=[
            [16, 11, 10, 16],
            [12, 12, 14, 19],
            [14, 13, 16, 24],
            [14, 17, 22, 29]
        ],
        expected_output=[16, 11, 12, 14, 12, 10, 16, 14, 13, 14, 17, 16, 19, 24, 22, 29]
    )
]


@pytest.mark.parametrize("case", test_zigzag)
def test_zigzag(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = zigzag(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)

#########################################
#                                       #
#   Un-zigzag                           #
#                                       #
#########################################
