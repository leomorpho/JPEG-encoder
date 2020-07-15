
import pytest
import logging
from src.compression.zigzag import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with block and expected vector"""

    def __init__(self, name, block, vector):
        self.name = name
        self.block = block
        self.vector = vector


test_zigzag_cases = [
    InputOutputCase(
        name="Nominal",
        block=[
            [16, 11],
            [12, 12],
        ],
        vector=[16, 11, 12, 12]
    ),
    InputOutputCase(
        name="Nominal",
        block=[
            [16, 11, 10, 16],
            [12, 12, 14, 19],
            [14, 13, 16, 24],
            [14, 17, 22, 29]
        ],
        vector=[16, 11, 12, 14, 12, 10,
                         16, 14, 13, 14, 17, 16, 19, 24, 22, 29]
    )
]

#########################################
#                                       #
#   Zigzag                              #
#                                       #
#########################################


@pytest.mark.parametrize("case", test_zigzag_cases)
def test_zigzag(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.block))

    result = zigzag(case.block)

    log.debug("Result: " + str(result))
    assert(result == case.vector)

#########################################
#                                       #
#   Un-zigzag                           #
#                                       #
#########################################


@pytest.mark.parametrize("case", test_zigzag_cases)
def test_unzigzag(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.block))

    result = un_zigzag(case.vector)

    log.debug("Result: " + str(result))
    assert(result == case.block)
