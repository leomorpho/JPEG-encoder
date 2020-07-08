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
        expected_output=[1, 5]
    )
]

@pytest.mark.parametrize("case", test_encode_huffman)
def test_encode_huffman(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = HuffmanEncoder.encode(case.input_val)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)

#########################################
#                                       #
# Get leaves                            #
#                                       #
#########################################

test_get_leaves_recursive = [
    InputOutputCase(
        name="Nominal",
        input_val=[1, 1, 1, 1, 10],
        expected_output=2
    )
]

@pytest.mark.parametrize("case", test_get_leaves_recursive)
def test_get_leaves_recursive(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    hf = HuffmanEncoder()
    prob_distr = hf.create_prob_distribution(case.input_val)

    # Create starting leaves from ordered probability distribution
    # The keys of the dict are the sample values.
    leaves = []
    for key, val in prob_distr.items():
        new_leaf = HuffmanNode()
        new_leaf.sample_value = key
        new_leaf.probability = val
        leaves.append(new_leaf)

    # Create Huffman tree
    root_node = hf.create_tree(leaves)

    # Get all leaves
    leaves = hf.get_leaves(root_node)

    log.debug("Result: " + str(leaves))
    assert(len(leaves) == case.expected_output)

