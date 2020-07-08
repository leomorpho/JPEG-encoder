class LZWEncoder:
    def encode_wav(self, wav):
        """Wrapper function for WAV files
        """
        self.unencoded_samples = wav.samples
        self.encoded_samples = self.encode(wav.samples)


    def encode(self, data):
        encoded_sentence = []

        dictionary = dict()

        s = data[0]
        dictionary[s] = 0

        data = data[1:]
        next_new_code = len(dictionary)

        while data:
            c = data[0]
            data = data[1:]

            try:
                if dictionary[s+c]:
                    s = s + c

            except KeyError:
                encoded_sentence.append(str(dictionary[s]))
                dictionary[s + c] = next_new_code
                next_new_code += 1
                s = c

        return encoded_sentence.append(str(dictionary[s]))


    def compression_ratio(self):
        # Convert both lists to string. The unencoded string must be converted to binary.
        unencoded_binary = [bin(x) for x in self.unencoded_samples]

        len_unencoded = len("".join(unencoded_binary))
        len_encoded = len("".join(self.encoded_samples))
        return round(len_unencoded / len_encoded, 4)
