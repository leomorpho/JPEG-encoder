import logging
from typing import *
from src.codecs.wav import WavFile
from src.compression.huffman import HuffmanEncoder
from src.compression.lzw import LZWEncoder

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Compressor:
    def __init__(self):
        self.Huffman_compressed: WavFile = None
        self.LZW_compressed: WavFile = None

    def compress(self, wav_file: WavFile):
        """Compress WAV using all available compressors"""
        self.huffman_encoder = HuffmanEncoder()
        self.huffman_encoder.encode_wav(wav_file)

        self.lzw_encoder = LZWEncoder()
        self.lzw_encoder.encode_wav(wav_file)

    def get_huffman_compression_ratio(self):
        """Compress WAV using Huffman compression"""
        return self.huffman_encoder.compression_ratio()

    def get_LZW_compression_ratio(self):
        """Compress WAV using LZW compression"""
        return self.lzw_encoder.compression_ratio()

    def get_huffman_based_LZW_compression_rate(self):
        """Compress WAV using Huffman first and then LZW compression"""
        return 1

    def get_LZW_based_huffman_compression_rate(self):
        """Compress WAV using LZW first and then Huffman compression"""
        return 1
