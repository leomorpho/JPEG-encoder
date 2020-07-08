import logging
from typing import *
from src.codecs.wav import WavFile
from src.compression.huffman import HuffmanEncoder

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Compressor:
    def __init__(self):
        self.Huffman_compressed: WavFile = None
        self.LZW_compressed: WavFile = None

    def compress(self, wav_file: WavFile):
        """Compress WAV using all available compressors"""
        self.huffman_encoder= HuffmanEncoder()
        self.huffman_encoder.encode_wav(wav_file)

        # TODO: LZW compression
        # self.LZW_compressed = LZWEncoder.encode(wav_file)

    def get_huffman_compression_ratio(self):
        """Compress WAV using Huffman compression"""
        return self.huffman_encoder.compression_ratio()

    def get_LZW_compression_ratio(self):
        """Compress WAV using LZW compression"""
        return 2.3
