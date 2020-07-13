import pytest
import logging
from src.compression.lossy import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)

#########################################
#                                       #
# Block splitting & joining             #
#                                       #
#########################################


class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, input_val, expected_output):
        self.name = name
        self.input_val = input_val
        self.expected_output = expected_output


test_block_split = [
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
            [
                [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ]
            ]
        ]
    ),
    InputOutputCase(
        name="Height of 9 should create 2 blocks",
        input_val=[
            [1, 1, 1, 1, 1, 1, 1, 1],
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
            [
                [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ]
            ],
            [
                [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ]
            ]
        ]
    )
]


@pytest.mark.parametrize("case", test_block_split)
def test_block_splitting(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = block_split_layer(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)


test_block_join = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [
                [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]
                ]
            ]
        ],
        expected_output=[
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]
    ),
]


@pytest.mark.parametrize("case", test_block_join)
def test_block_joining(case):
    """This test is the opposite of test_block_splitting and
    uses the same test data, except reversed.
    """
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = block_join_layer(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)

#########################################
#                                       #
# YCbCr splitting & joining             #
#                                       #
#########################################


test_YCbCr_split = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [[1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1]]
        ],
        expected_output=[
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ]
        ]
    ),
    InputOutputCase(
        name="3x4 iamges",
        input_val=[
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ],
        expected_output=[
            [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ]
        ]
    ),
]


@pytest.mark.parametrize("case", test_YCbCr_split)
def test_YCbCr_splitting(case):
    """This test is the opposite of test_block_splitting and
    uses the same test data, except reversed.
    """
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = separate_image_layers(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)

test_YCbCr_join = [
    InputOutputCase(
        name="Nominal",
        input_val=[
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ],
            [
                [1, 1],
                [1, 1]
            ]
        ],
        expected_output=[
            [[1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1]]
        ]
    ),
    InputOutputCase(
        name="3x4 iamges",
        input_val=[
            [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ],
            [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
            ]
        ],
        expected_output=[
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
        ]
    ),
]


@pytest.mark.parametrize("case", test_YCbCr_join)
def test_YCbCr_splitting(case):
    """This test is the opposite of test_block_splitting and
    uses the same test data, except reversed.
    """
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = join_image_layers(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)
