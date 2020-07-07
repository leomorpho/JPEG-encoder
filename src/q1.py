import logging
from typing import *
import math
import sys

log = logging.getLogger()
log.setLevel(logging.DEBUG)

BIT_PER_SYMBOL = "bit/symbol"


class HuffmanNode:
    def __init__(self):
        self.parent = None
        self.children = None        # can only have 2 children
        self.probability = None

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


class HuffmanTree:
    def __init__(self, sentence):
        self.utils = Utils()
        single_char_list = self.utils.str_to_list(sentence, word_len=1)
        double_char_list = self.utils.str_to_list(sentence, word_len=2)

        prob_distr_single = self.utils.create_prob_distribution(single_char_list)
        prob_distr_double = self.utils.create_prob_distribution(double_char_list)

        self._entropy_1 = self.utils.get_entropy(
            prob_distr_single, entropy_2nd=False)
        self._entropy_2 = self.utils.get_entropy(prob_distr_double, entropy_2nd=True)

        # Simple Huffman codeword (1 char)
        self._avg_codeword_len = self.avg_codeword_len(prob_distr_single)

        # Joint Huffman codeword (2 chars)
        self._avg_codeword_joint_len = self.avg_codeword_len(
                prob_distr_double, double_char=True)

    def get_repr(self):
        return {
            "entropy_1st": round(self._entropy_1, 4),
            "entropy_2nd": round(self._entropy_2, 4),
            "avg_code_len_1_symbol": round(self._avg_codeword_len, 4),
            "avg_code_len_2_symbols": round(self._avg_codeword_joint_len, 4),
        }

    @classmethod
    def avg_codeword_len(cls, prob_distr: Dict, double_char=False) -> float:
        """Calculate average codeword length for Huffman coding or
        2 symbol joint Huffman coding
        """
        leaves: List[HuffmanNode] = []

        for key, val in prob_distr.items():
            new_leaf = HuffmanNode()
            new_leaf.probability = val
            leaves.append(new_leaf)

        _ = cls.huffman_recurse(leaves)

        codeword_len = 0
        for leaf in leaves:
            edges = leaf.edges_to_root()
            if edges == 0:
                # A single node needs 1 bit for representation
                codeword_len += 1
            codeword_len += leaf.probability * leaf.edges_to_root()

        if double_char:
            return codeword_len / 2
        return codeword_len

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


    @staticmethod
    def create_prob_distribution(list_repr: List[Any]):
        prob_distribution = dict()

        for i in list_repr:
            try:
                prob_distribution[i] += 1
            except KeyError:
                prob_distribution[i] = 1

        for key, val in prob_distribution.items():
            prob_distribution[key] = val / len(list_repr)

        return prob_distribution

    @classmethod
    def get_str_entropy(self, sentence, entropy_2nd=False):
        list_o = self.str_to_list(sentence)
        prob_distr = self.create_prob_distribution(list_o)
        return self.get_entropy(prob_distr, entropy_2nd=entropy_2nd)


def pipeline(sentence: str):
    """Run pipeline on input string"""
    ht = HuffmanTree(sentence)

    return ht.get_repr()


if __name__ == "__main__":
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        print("Please provide a sentence of even length greater than 2.\n",
                "Your sentence may contain spaces. \n",
                "E.g.: \"0010111010\" or \"00 10 11 10 10\" or \"AAABDA\"")
        sys.exit()

    sentence = "".join(sys.argv[1].split(" "))

    if len(sentence) % 2 != 0:
        print(" Sentence must be of an even length.\n",
                f"Current length is {len(sentence)} characters.")
        sys.exit()

    result = pipeline(sentence)
    print(result)

    print("\n ##########################\n",
          "#                        #\n",
          "#    Results             #\n",
          "#                        #\n",
          "##########################\n")
    print('%-30s%-32s' % ("Sentence", sentence))
    print('%-30s%-.4f' % ("First-order entropy", result["entropy_1st"]))
    print('%-30s%-.4f' % ("Second-order entropy", result["entropy_2nd"]))
    print('%-30s%-.4f %s' % ("Average code length",
        result["avg_code_len_1_symbol"], BIT_PER_SYMBOL))
    print('%-30s%-.4f %s' % ("Average joint code length",
        result["avg_code_len_2_symbols"], BIT_PER_SYMBOL))
