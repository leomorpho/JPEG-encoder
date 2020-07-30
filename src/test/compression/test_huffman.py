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

    def __init__(self, name, input_val, expected_output, compression_ratio=None):
        self.name = name
        self.input_val = input_val
        self.expected_output = expected_output
        self.compression_ratio = compression_ratio


test_encode_huffman = [
    InputOutputCase(
        name="Nominal",
        input_val=[1, 10],
        expected_output=['0', '1'],
        compression_ratio=4.0
    ),
    InputOutputCase(
        name="Nominal",
        input_val=[87, 121, 123],
        expected_output=['10', '11', '0'],
        compression_ratio=6.0
    ),
    InputOutputCase(
        name="Nominal",
        input_val=[1, 1, 1, 1, 10],
        expected_output=['1', '1', '1', '1', '0'],
        compression_ratio=10.0
    ),
    InputOutputCase(
        name="From notes",
        input_val=[123, 123, 100, 100, 100, 100, 99, 99, 50, 10],
        # This result looks off because it has no '0', or '1', but it is correct.
        # Worked it out on paper, and the nodes are re-ordered on every node linkages,
        # this result can totally happen. It unfortunately results in a less efficient
        # encoding.
        expected_output=['00', '00', '11', '11',
                         '11', '11', '01', '01', '100', '101'],
        compression_ratio=10.0
    ),
    InputOutputCase(
        name="Nominal",
        input_val=[1, 2, 1, 2, 10, 2, 2, 2, 2, 2, 2, 2, 34, 3, 3, 6, 6, 7],
        expected_output=['1111', '0', '1111', '0', '1100', '0', '0', '0',
                         '0', '0', '0', '0', '1101', '100', '100', '101', '101', '1110'],
        compression_ratio=7.2
    )
]


@pytest.mark.parametrize("case", test_encode_huffman)
def test_encode_huffman(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    he = HuffmanEncoder()
    result = he.encode(case.input_val)
    cr = he.compression_ratio()

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)
    assert(cr == case.compression_ratio)

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
    encoded = "".join(he.encode(case))
    log.debug(encoded)
    decoded = he.decode(encoded)

    log.debug("Result: " + str(decoded))
    assert(decoded == case)

#########################################
#                                       #
# Write/read Huffman to/from disk       #
#                                       #
#########################################


class ReadWriteCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(
            self,
            name,
            input_val,
            expected_output,
            encoded_tree):
        self.name = name
        self.input_val = input_val
        self.expected_output = expected_output
        self.encoded_tree = encoded_tree


test_serialize = [
    ReadWriteCase(
        name="Nominal",
        input_val=[1, 10],
        expected_output=['0', '1'],
        encoded_tree=['1', '0', '00000001', '0', '00001010'],
    ),
    ReadWriteCase(
        name="Nominal",
        input_val=[87, 121, 123],
        expected_output=['10', '11', '0'],
        encoded_tree=['1', '0', '01111011', '1',
                      '0', '01010111', '0', '01111001'],
    ),
    ReadWriteCase(
        name="Nominal",
        input_val=[1, 1, 1, 1, 10],
        expected_output=['1', '1', '1', '1', '0'],
        encoded_tree=['1', '0', '00001010', '0', '00000001'],
    ),
    ReadWriteCase(
        name="From notes",
        input_val=[123, 123, 100, 100, 100, 100, 99, 99, 50, 10],
        # This result looks off because it has no '0', or '1', but it is correct.
        # Worked it out on paper, and the nodes are re-ordered on every node linkages,
        # this result can totally happen. It unfortunately results in a less efficient
        # encoding.
        expected_output=['00', '00', '11', '11',
                         '11', '11', '01', '01', '100', '101'],
        encoded_tree=['1', '1', '0', '01111011', '0', '01100011', '1',
                      '1', '0', '00110010', '0', '00001010', '0', '01100100'],
    ),
    ReadWriteCase(
        name="Nominal",
        input_val=[1, 2, 1, 2, 10, 2, 2, 2, 2, 2, 2, 2, 34, 3, 3, 6, 6, 7],
        expected_output=['1111', '0', '1111', '0', '1100', '0', '0', '0',
                         '0', '0', '0', '0', '1101', '100', '100', '101', '101', '1110'],
        encoded_tree=['1', '0', '00000010', '1', '1', '0', '00000011', '0', '00000110', '1',
                      '1', '0', '00001010', '0', '00100010', '1', '0', '00000111', '0', '00000001'],
    )
]


@pytest.mark.parametrize("case", test_serialize)
def test_serialize(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    he = HuffmanEncoder()
    result = he.encode(case.input_val)
    assert(result == case.expected_output)

    old_tree_root = he.root_node

    serialized = he.serialize_tree()
    log.info(serialized)
    assert(serialized == case.encoded_tree)

    he.deserialize_tree(serialized)
    serialized = he.serialize_tree()
    log.info(serialized)
    assert(serialized == case.encoded_tree)

    # Re-encode with the deserialized tree
    result = he.encode(case.input_val)
    assert(result == case.expected_output)
