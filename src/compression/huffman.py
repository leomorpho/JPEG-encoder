import math
import logging
from typing import *

log = logging.getLogger()
log.setLevel(logging.DEBUG)


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
    # def __init__(self, data):
    #     self.utils = Utils()

    #     self._entropy_1 = self.utils.get_entropy(
    #         prob_distr, entropy_2nd=False)

    #     # Simple Huffman codeword
    #     self._avg_codeword_len = self.avg_codeword_len(prob_distr)

    #     self.tree = self.create_tree()

    def get_repr(self):
        return {
            "entropy_1st": round(self._entropy, 4),
            "avg_code_len_1_symbol": round(self._avg_codeword_len, 4),
        }

    def encode_wav(self, wav):
        """Wrapper function for WAV files
        """
        wav.samples = self.encode(wav.samples)
        return wav

    @classmethod
    def encode(cls, data):
        # Create probability distribution for the WAV samples
        prob_distr = cls.create_prob_distribution(data)

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
        root_node = cls.create_tree(leaves)

        # Assign code to every node
        root_node = cls.assign_codes(root_node)

        # Get all leaves
        leaves = cls.get_leaves(root_node)
        print(leaves)

        # Create dict of sample to code
        # TODO

        # Encode samples to codes
        # TODO
        return 0

    @classmethod
    def create_tree(cls, list_repr: List[HuffmanNode]) -> HuffmanNode:
        """Helper method to Create a Huffman tree from the given list and return the root node
        """
        return cls.huffman_recurse(list_repr)[0]

    @classmethod
    def huffman_recurse(cls, list_repr: List[HuffmanNode]) -> List[HuffmanNode]:
        """Recursive function to create a Huffman tree"""
        if len(list_repr) == 1:
            return list_repr
        list_repr.sort(key=lambda x: x.probability)

        child1 = list_repr[0]
        child2 = list_repr[1]
        new_node = HuffmanNode()
        new_node.probability = child1.probability + child2.probability
        child1.parent = new_node
        child2.parent = new_node
        new_node.children = [child1, child2]

        list_repr = list_repr[2:]
        list_repr.insert(0, new_node)

        list_repr = cls.huffman_recurse(list_repr)
        return list_repr

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
            node.children[0] = assign_code_recurse(node.children[0])
            node.children[1] = assign_code_recurse(node.children[1])

    @classmethod
    def get_leaves(cls, root):
        """Helper method to find all leaves of a binary tree"""
        return cls.get_leaf_recurse(root, [])

    @classmethod
    def get_leaf_recurse(cls, node, leaves) -> List[HuffmanNode]:
        """Recursive method to find a leaf"""
        leaves_l = []
        leaves_r = []
        if node.children:
            # Go down left and right branches
            leaves_l = cls.get_leaf_recurse(node.children[0], leaves)
            leaves_r = cls.get_leaf_recurse(node.children[1], leaves)
            return leaves_l + leaves_r

        return [node]


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


class Utils:
    @staticmethod
    def str_to_list(sentence: str, word_len=2) -> List[Any]:
        """Convert a even length string with minimum size of 2 to
        a list of pair of characters
        """
        sentence_len = len(sentence)
        pairs_list = []

        count = 0
        while count < sentence_len:
            pair = sentence[count:count+word_len]
            pairs_list.append(pair)
            count += word_len

        return pairs_list

    @staticmethod
    def get_entropy(prob_distribution: Dict, entropy_2nd):
        """Calculate first or second order entropy
        """
        entropy: float = 0

        # entropy = SUM(prob * log_2 (prob))
        for prob in prob_distribution.values():
            res = prob * math.log((1 / prob), 2)
            entropy += res

        if entropy_2nd:
            return entropy / 2
        return entropy

    @classmethod
    def get_str_entropy(self, sentence, entropy_2nd=False):
        list_o = self.str_to_list(sentence)
        prob_distr = self.create_prob_distribution(list_o)
        return self.get_entropy(prob_distr, entropy_2nd=entropy_2nd)
