import sys
import logging
from q1 import Utils

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class LZW:
    def __init__(self):
        pass

    @staticmethod
    def encode(sentence):

        encoded_sentence = []

        dictionary = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4
        }
        next_new_code = len(dictionary)

        s = sentence[0]
        sentence = sentence[1:]

        while sentence:
            c = sentence[0]
            sentence = sentence[1:]

            try:
                if dictionary[s+c]:
                    s = s + c

            except KeyError:
                encoded_sentence.append(str(dictionary[s]))
                dictionary[s + c] = next_new_code
                next_new_code += 1
                s = c

        encoded_sentence.append(str(dictionary[s]))

        return " ".join(encoded_sentence), dictionary


if __name__ == "__main__":
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        print("Please provide a sentence using letters from a/A to e/E\n",
              "Your sentence may contain spaces. \n",
              "E.g.: \"abbce\" or \"AB BA AC DE EE\"")
        sys.exit()

    sentence = "".join(sys.argv[1].split(" ")).upper()

    output_sequence, dictionary = LZW.encode(sentence)

    entropy_1st = Utils.get_str_entropy(sentence, entropy_2nd=False)
    entropy_2nd = Utils.get_str_entropy(sentence, entropy_2nd=True)

    print("\n ##########################\n",
          "#                        #\n",
          "#    Results             #\n",
          "#                        #\n",
          "##########################\n")
    print('%-30s%-.4f' % ("First-order entropy", entropy_1st))
    print('%-30s%-.4f' % ("Second-order entropy", entropy_2nd))
    print('%-30s%-32s' % ("Sentence", sentence))
    print('%-30s%-32s' % ("Output sequence", output_sequence))
    print('%-30s%-32s' % ("Dictionary", str(dictionary)))
