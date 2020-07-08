class LZWEncoder:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self._unencoded_samples = wav_file.samples
        self._encoded_samples = []

    def encode_wav(self):
        """Wrapper function for WAV files
        """
        self._encoded_samples = self.encode(self.wav_file.samples)


    def encode(self, data):
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
        return encoded_sentence


    def compression_ratio(self, encoded_samples=None):
        # Convert both lists to string. The unencoded string must be converted to binary.
        if not encoded_samples:
            encoded_samples = self._encoded_samples

        unencoded_binary = [bin(x) for x in self._unencoded_samples]

        len_unencoded = len("".join(unencoded_binary))
        len_encoded = len("".join(self.encoded_samples))
        return round(len_unencoded / len_encoded, 4)

    @property
    def encoded_samples(self):
        return self._encoded_samples
