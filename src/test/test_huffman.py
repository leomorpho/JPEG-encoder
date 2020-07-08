import pytest
import logging
from src.compression.huffman import HuffmanEncoder, HuffmanNode


log = logging.getLogger()
log.setLevel(logging.DEBUG)

#########################################
#                                       #
# Huffman encode                        #
#                                       #
#########################################

class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, input_val, expected_output):
        self.name = name
        self.input_val = input_val
        self.expected_output = expected_output

test_encode_huffman = [
    InputOutputCase(
        name="Nominal",
        input_val=[1, 1, 1, 1, 10],
        expected_output="11110"
    ),
    InputOutputCase(
        name="From notes",
        input_val=["A", "A", "B", "B", "B", "B", "C", "C", "D", "E"],
        expected_output="1111110000101011001101"
    ),
    InputOutputCase(
        name="Nominal",
        input_val=[1, 2, 1, 2, 10, 2, 1, 4, 3, 6, 7, 4, 34, 3, 3, 6, 6, 7],
        expected_output="10111010111001001101010111110010001101011111110000100"
    )
]

@pytest.mark.parametrize("case", test_encode_huffman)
def test_encode_huffman(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    he = HuffmanEncoder()
    result = he.encode(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)
