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
        # for attr, val in self.__dict__.items():
        #     formatted_repr += "\t%20s: %12s\n" % (attr, val)
        formatted_repr += f"sample value: {self.sample_value}"
        return formatted_repr


class HuffmanEncoder:
    def __init__(self, wav_file=None):
        if wav_file:
            self.wav_file = wav_file
            self._unencoded_samples = wav_file.samples
            self._encoded_samples = []

        # Encoded tree is a tree ready to be written to file
        self.serialized_tree = ""

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

        # Each member of the input data is a 2 byte short integer
        unencoded_binary_bytes = len(self._unencoded_samples) * 2
        encoded_samples_bytes = int(len("".join(encoded_samples)) / 8)
        if encoded_samples_bytes == 0:
            encoded_samples_bytes = 1

        log.debug(unencoded_binary_bytes)
        log.debug(encoded_samples_bytes)

        return round(unencoded_binary_bytes / encoded_samples_bytes, 4)

    def encode(self, data):
        self._unencoded_samples = data

        # Create probability distribution for the samples
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
        self.root_node = self.create_tree(leaves)

        # Assign code to every node
        self.root_node = self.assign_codes(self.root_node)

        # Create dict of sample to code
        # TODO: make sample_to_code_dict a local var once it is read from file in decoding
        self.sample_to_code_dict = self.create_sample_to_code_dict(leaves)

        # Encode samples to codes
        self._encoded_samples = self.convert_samples_to_codes(
            data, self.sample_to_code_dict)

        return self._encoded_samples

    def decode(self, data: str):
        if type(data) == list:
            data = "".join(data)
        # TODO: create dictionnary by reading huffman tree from file
        decoded = []
        current_node = self.root_node

        # Walk the tree until a leaf is found. Add the corresponding value.
        # Continue from root and next bit of encoded string.
        for bit in data:
            if current_node.children == None:
                decoded.append(current_node.sample_value)
                current_node = self.root_node
            if bit == "0":
                current_node = current_node.children[0]
            elif bit == "1":
                current_node = current_node.children[1]
            else:
                raise Exception("code is not legal")
        decoded.append(current_node.sample_value)

        return decoded

    def serialize_tree(self) -> str:
        # Recursive helper function
        def helper(node):
            """
            Convert the huffman tree to a string. A 1 represents a child.
            A 0 represents a leaf and is followed by the leaf value which
            is 1 byte wide.

            The encoded tree is a string representing a binary number.
            """
            serialized_tree = []
            if node.children:
                serialized_tree.append('1')
                serialized_tree += helper(node.children[0])
                serialized_tree += helper(node.children[1])
            else:
                serialized_tree.append('0')
                serialized_tree.append(
                    "{0:08b}".format(int(node.sample_value)))
            return serialized_tree

        return helper(self.root_node)

    def deserialize_tree(self, serialized):
        """
        Convert a list of 1 (indicating a child) and 0 (indicating a leaf)
        to a huffman tree.
        """
        # For testing purposes, serialized can be passed as a string.
        # This makes it easier to visualize what is going on under the hood.
        if type(serialized) == str:
            serialized = list(serialized)

        self.serialized_tree = serialized

        # Pop first 1 from the serialized string. It represents the root.
        self.serialized_tree.pop(0)

        self.root_node = self.expand()

    def expand(self):
        """
        Recursive helper function to expand a a string of 1 and 0 to a Huffman tree
        """
        log.info(self.serialized_tree)
        node = HuffmanNode()
        node.children = []

        next_val = self.serialized_tree.pop(0)
        log.info(next_val)
        if next_val == "1":
            left_child = self.expand()
            node.children.append(left_child)

        elif next_val == "0":
            binary_str = self.serialized_tree.pop(0)
            log.info(binary_str)
            left_child = HuffmanNode()
            left_child.sample_value = int("".join(binary_str), 2)
            node.children.append(left_child)
        else:
            raise Exception("It should be either a 1 or 0")

        # Do the same for the other side
        next_val = self.serialized_tree.pop(0)
        log.info(next_val)
        if next_val == "1":
            right_child = self.expand()
            node.children.append(right_child)

        elif next_val == "0":
            binary_str = self.serialized_tree.pop(0)
            log.info(binary_str)
            right_child = HuffmanNode()
            right_child.sample_value = int("".join(binary_str), 2)
            node.children.append(right_child)
        else:
            raise Exception("It should be either a 1 or 0")

        # A non-terminal node should always have 2 children
        assert(len(node.children) == 2)

        return node

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
            nodes.append(new_node)

        nodes.sort(key=lambda x: x.probability)
        assert(nodes[0].probability == 1)
        return nodes[0]

    @classmethod
    def assign_codes(cls, root: HuffmanNode) -> HuffmanNode:
        """Helper method to assign codes to every node of a Huffman tree.
        """
        # Only the root node has no code
        if root.children:
            root.children[0].code = "0"
            root.children[1].code = "1"

            # Set codes for right and left branches of root
            root.children[0] = cls.assign_code_recurse(root.children[0])
            root.children[1] = cls.assign_code_recurse(root.children[1])

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

        return node

    @staticmethod
    def create_sample_to_code_dict(leaves: List[HuffmanNode]):
        """Create a dictionary of sample value to code. This is used to encode
        a string of data.
        """
        newDict = {}
        for leaf in leaves:
            newDict[leaf.sample_value] = leaf.code
        return newDict

    @staticmethod
    def pad_to_full_byte(value):
        """
        Pad a value that is less than a byte to a full byte
        """
        padding = 8 - len(value) % 8

        for i in range(padding):
            value += "0"

        return value

    # TODO: convert samples to code and vice versa can be one function
    @staticmethod
    def convert_samples_to_codes(samples: List[int],
                                 sample_to_code_dict: Dict[int, int]) -> List[int]:
        """Encode a list of samples using a Huffman dictionary
        """
        result = []
        for sample in samples:
            result.append(sample_to_code_dict[sample])

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


class LZWEncoder:
    def __init__(self, wav_file=None):
        if wav_file:
            self.wav_file = wav_file
            self._unencoded_samples = wav_file.samples
        self._encoded_samples = []

    def encode_wav(self):
        """Wrapper function for WAV files
        """
        self._encoded_samples = self.encode(self.wav_file.samples)

    def encode(self, data):
        self._unencoded_samples = data
        encoded_sentence = []

        dictionary = dict()

        next_new_code = 0

        # Initialize dict with all samples of length 1
        # CAUTION: dict keys must be strings!
        for sample in data:
            try:
                _ = dictionary[str(sample)]
            except KeyError:
                dictionary[str(sample)] = next_new_code
                next_new_code += 1

        # Start encoding data
        s = data[0]

        data = data[1:]

        while data:
            c = data[0]
            data = data[1:]

            try:
                if dictionary[f"{s} {c}"]:
                    s = f"{s} {c}"

            except KeyError:
                encoded_sentence.append(str(dictionary[str(s)]))
                dictionary[f"{s} {c}"] = next_new_code
                next_new_code += 1
                s = c

        encoded_sentence.append(str(dictionary[str(s)]))
        self._encoded_samples = encoded_sentence
        return encoded_sentence

    def compression_ratio(self, encoded_samples=None):
        # Convert both lists to string. The unencoded string must be converted to binary.
        if not encoded_samples:
            encoded_samples = self._encoded_samples

        # Each member of the input data is a 2 byte short integer
        unencoded_binary_bytes = len(self._unencoded_samples) * 2
        encoded_samples_bytes = int(len("".join(encoded_samples)) / 8)
        if encoded_samples_bytes == 0:
            encoded_samples_bytes = 1

        log.debug(unencoded_binary_bytes)
        log.debug(encoded_samples_bytes)

        return round(unencoded_binary_bytes / encoded_samples_bytes, 4)

    @property
    def encoded_samples(self):
        return self._encoded_samples
