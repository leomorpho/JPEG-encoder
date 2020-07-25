import pytest
import logging
from src.compression.lossless import HuffmanEncoder, HuffmanNode


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
        expected_output=['1', '1', '1', '1', '0']
    ),
    InputOutputCase(
        name="From notes",
        input_val=["A", "A", "B", "B", "B", "B", "C", "C", "D", "E"],
        expected_output=['111', '111', '0', '0',
                         '0', '0', '10', '10', '1100', '1101']
    ),
    InputOutputCase(
        name="Nominal",
        input_val=[1, 2, 1, 2, 10, 2, 1, 4, 3, 6, 7, 4, 34, 3, 3, 6, 6, 7],
        expected_output=['101', '110', '101', '110', '0100', '110', '101',
                         '011', '111', '00', '100', '011', '0101', '111', '111', '00', '00', '100']

    )
]


@pytest.mark.skip(reason="needs to be fixed")
@pytest.mark.parametrize("case", test_encode_huffman)
def test_encode_huffman(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    he = HuffmanEncoder()
    result = he.encode(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)

#########################################
#                                       #
# Huffman decoding                      #
#                                       #
#########################################


test_decode_cases = [
    ([0, 123, 2, 1]),
    ([123, 121, 1, 4, 5, 3, 98, 54, 32, 12, 58, 98, 178, 20, 1, 3, 5, 85])
]


@pytest.mark.parametrize("case", test_decode_cases)
def test_decode_huffman(case):
    log.debug("Input: " + str(case))

    he = HuffmanEncoder()
    encoded = he.encode(case)
    log.debug(encoded)
    decoded = he.decode(encoded)

    log.debug("Result: " + str(decoded))
    assert(decoded == case)
