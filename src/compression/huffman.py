import math
import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

class HuffmanTree:
    def __init__(self, sentence):
        self.utils = Utils()

        prob_distr_single = self.utils.create_prob_distribution(single_char_list)

        self._entropy_1 = self.utils.get_entropy(
            prob_distr_single, entropy_2nd=False)

        # Simple Huffman codeword
        self._avg_codeword_len = self.avg_codeword_len(prob_distr_single)


    def get_repr(self):
        return {
            "entropy_1st": round(self._entropy, 4),
            "avg_code_len_1_symbol": round(self._avg_codeword_len, 4),
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


