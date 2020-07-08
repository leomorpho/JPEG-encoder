import math
import logging
from typing import *
import os

log = logging.getLogger()
log.setLevel(logging.DEBUG)

ENCODED_WAV_FILEPATH = "encoded_file.wav"


class HuffmanNode:
    def __init__(self):
        self.code = None            # The code for the value A
        # The value A (only leaves should have values)
        self.sample_value = None
        self.parent = None
        self.children = None        # can only have 2 children
        self.probability = None     # The probability P(A)

    def edges_to_root(self):
        """Return number of num_edges to root
        """
        # If this is the root
        if not self.parent:
            return 0

        count = 1
        curr_node = self.parent

        while curr_node.parent:
            count += 1
            curr_node = curr_node.parent

        return count

    def __repr__(self):
        """Pretty prints all attributes of object
        """
        # return "%s(%r)" % (self.__class__, self.__dict__)

        formatted_repr = f"\n{self.__class__}\n"
        for attr, val in self.__dict__.items():
            formatted_repr += "\t%20s: %12s\n" % (attr, val)
        return formatted_repr


class HuffmanEncoder:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self._unencoded_samples = wav_file.samples
        self._encoded_samples = []

    @property
    def encoded_samples(self):
        return self._encoded_samples

    def encode_wav(self):
        """Wrapper function for WAV files
        """
        self._encoded_samples = self.encode(self.wav_file.samples)

    def compression_ratio(self, encoded_samples=None):
        # Convert both lists to string. The unencoded string must be converted to binary.
        if not encoded_samples:
            encoded_samples = self._encoded_samples

        unencoded_binary = [bin(x) for x in self._unencoded_samples]

        len_unencoded = len("".join(unencoded_binary))
        len_encoded = len("".join(encoded_samples))
        return round(len_unencoded / len_encoded, 4)

    def encode(self, data):
        # Create probability distribution for the WAV samples
        prob_distr = self.create_prob_distribution(data)

        # Create starting leaves from ordered probability distribution
        # The keys of the dict are the sample values.
        leaves = []
        for key, val in prob_distr.items():
            new_leaf = HuffmanNode()
            new_leaf.sample_value = key
            new_leaf.probability = val
            leaves.append(new_leaf)

        # Optimize heap
        del(prob_distr)

        # Create Huffman tree
        root_node = self.create_tree(leaves)

        # Assign code to every node
        root_node = self.assign_codes(root_node)

        # Create dict of sample to code
        sample_to_code_dict = self.sample_to_code_dict(leaves)

        # Encode samples to codes
        return self.encode_to_list(data, sample_to_code_dict)

    @classmethod
    def create_tree(cls, nodes: List[HuffmanNode]) -> HuffmanNode:
        """Create a Huffman tree from the given list and return the root node
        """

        while len(nodes) > 1:
            nodes.sort(key=lambda x: x.probability)
            child1 = nodes[0]
            child2 = nodes[1]
            new_node = HuffmanNode()
            new_node.probability = child1.probability + child2.probability
            child1.parent = new_node
            child2.parent = new_node
            new_node.children = [child1, child2]

            nodes = nodes[2:]
            nodes.insert(0, new_node)

        return nodes[0]

    @classmethod
    def assign_codes(cls, root: HuffmanNode) -> HuffmanNode:
        """Helper method to assign codes to every node of a Huffman tree.
        """
        # Only the root node has no code
        root.children[0].code = "0"
        root.children[1].code = "1"

        # Set codes for right and left branches of root
        cls.assign_code_recurse(root.children[0])
        cls.assign_code_recurse(root.children[1])

        return root

    @classmethod
    def assign_code_recurse(cls, node: HuffmanNode):
        # Assign codes to children
        node_code = node.code

        if node.children:
            node.children[0].code = node_code + "0"
            node.children[1].code = node_code + "1"

            # Set codes for right and left branches of node
            node.children[0] = cls.assign_code_recurse(node.children[0])
            node.children[1] = cls.assign_code_recurse(node.children[1])

    @staticmethod
    def sample_to_code_dict(leaves: List[HuffmanNode]):
        """Create a dictionary of sample value to code. This is used to encode
        a stringa of data.
        """
        newDict = {}
        for leaf in leaves:
            newDict[leaf.sample_value] = leaf.code
        return newDict

    @staticmethod
    def encode_to_list(samples: List[int], sample_to_code: Dict[int, int]) -> List[int]:
        """Encode a list of samples using the Huffman dictionary
        """
        result = []
        for sample in samples:
            result.append(sample_to_code[sample])

        return result

    @staticmethod
    def create_prob_distribution(samples: List[Any]) -> Dict[int, float]:
        """
        Create a dictionary of sample value to probability
        """
        prob_distribution = dict()

        for i in samples:
            try:
                prob_distribution[i] += 1
            except KeyError:
                prob_distribution[i] = 1

        for key, val in prob_distribution.items():
            prob_distribution[key] = val / len(samples)

        return prob_distribution
