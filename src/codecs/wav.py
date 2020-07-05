import struct

LITTLE_ENDIAN = '< '


class WavFile():
    def __init__(self, filename):
        """
        :param chunkID: Contains the letters "RIFF" in ASCII form: (0x52494646 big-endian form).
        :type  chunkID: 4 byte str

        :param chunkSize: This is the size of the rest of the chunk following this number.
        :type  chunkSize: 4 byte int

        :param format: Contains the letters "WAVE": (0x57415645 big-endian form).
        :type format: 4 byte str

        :param subchunk1ID: Contains the letters "fmt ": (0x666d7420 big-endian form).
        :type  subchunk1ID: 4 byte str

        :param subchunk1Size: 16 for PCM.  This is the size of the rest of the Subchunk which follows this number.
        :type  subchunk1Size: 4 byte int

        :param audioFormat: PCM = 1 (i.e. Linear quantization). Values other than 1 indicate some form of compression.
        :type  audioFormat: 2 byte int

        :param numChannels: Mono = 1, Stereo = 2, etc.
        :type  numChannels: 2 byte int

        :param samplesPerSec: 8000, 44100, etc.
        :type  samplesPerSec: 4 byte int

        :param avgBytePerSec: == samplesPerSec * NumChannels * BitsPerSample / 8
        :type  avgBytePerSec: 4 byte int

        :param blockAlign: == NumChannels * BitsPerSample / 8. The number of bytes for one sample including all channels.
        :type  blockAlign: 2 byte int

        :param bitsPerSample: 8 bits = 8, 16 bits = 16, etc.
        :type  bitsPerSample: 2 byte int

        :param subchunk2ID: Contains the letters "data": (0x64617461 big-endian form).
        :type  subchunk2ID: 4 byte str

        :param subchunk2Size: == NumSamples * NumChannels * BitsPerSample / 8. Number of bytes in the data following this field.
        :type  subchunk2Size: 2 byte int

        """
        self.chunkID = []
        self.chunkSize = []
        self.format = ""
        self.subchunk1ID = ""
        self.subchunk1Size = ""
        self.audioFormat = 0
        self.numChannels = 0
        self.samplesPerSec = 0
        self.avgBytePerSec = 0
        self.blockAlign = 0
        self.bitsPerSample = 0
        self.subchunk2ID = ""
        self.subchunk2Size = 0
        self.maxValInSamples = 0

        self.open_file(filename)

    def open_file(self, filename: str):
        """Read and construct WavFile object
        """
        with open(filename, "rb") as f:
            self.chunkID = f.read(4)
            self.chunkSize = self.unpack('I', f.read(4))
            self.format = f.read(4)
            self.subchunk1ID = f.read(4)
            self.subchunk1Size = self.unpack('I', f.read(4))
            self.audioFormat = self.unpack('H', f.read(2))
            self.numChannels = self.unpack('H', f.read(2))
            self.samplesPerSec = self.unpack('I', f.read(4))
            self.avgBytePerSec = self.unpack('I', f.read(4))
            self.blockAlign = self.unpack('H', f.read(2))
            self.bitsPerSample = self.unpack('H', f.read(2))
            self.subchunk2ID = f.read(4)
            self.subchunk2Size = self.unpack('H', f.read(2))
            self.maxValInSamples = 0
            self.data = self.load_data(f)

    def unpack(self, flag, byte_data: bytes):
        return struct.unpack(LITTLE_ENDIAN + flag, byte_data)[0]

    def load_data(self, f: str):
        """Read the actual data stored in the WAV file"""
        data = []
        bytesPerSample = int(self.bitsPerSample / 8)
        numSamples = int(self.subchunk2Size / bytesPerSample)

        flag = None
        if bytesPerSample == 1:
            flag = "B"
        elif bytesPerSample == 2:
            flag = "H"
        elif bytesPerSample == 4:
            flag = "I"
        else:
            raise Exception("No flag for this bytePerSample")

        for _ in range(numSamples):
            sample = self.unpack(flag, f.read(bytesPerSample))
            if sample > self.maxValInSamples:
                self.maxValInSamples = sample
            data.append(sample)
        return data

    def onResize(self, event):
        pass

    def __repr__(self):
        valDict = {
            "chunkID": self.chunkID,
            "chunkSize": self.chunkSize,
            "format": self.format,
            "subchunk1ID": self.subchunk1ID,
            "subchunk1Size": self.subchunk1Size,
            "audioFormat": self.audioFormat,
            "numChannels": self.numChannels,
            "samplesPerSec": self.samplesPerSec,
            "avgBytePerSec": self.avgBytePerSec,
            "blockAlign": self.blockAlign,
            "bitsPerSample": self.bitsPerSample,
            "subchunk2ID": self.subchunk2ID,
            "subchunk2Size": self.subchunk2Size,
            "maxValInSample": self.maxValInSamples
        }
        formatted_repr = "{"
        for key, val in valDict.items():
            formatted_repr += f"\t{key}: \t{val}\n"

        formatted_repr += "}"
        return formatted_repr

    @property
    def samples(self):
        return self.data

    @property
    def getBitsPerSample(self):
        return self.bitsPerSample

    @property
    def time_quantization(self):
        return self.subchunk2Size
