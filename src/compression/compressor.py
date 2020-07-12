import logging
from typing import *
from src.codecs.wav import WavFile
from src.compression.lossless import HuffmanEncoder
from src.compression.lossless import LZWEncoder

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class SoundCompressor:
    def __init__(self):
        self.Huffman_compressed: WavFile = None
        self.LZW_compressed: WavFile = None

    def compress(self, wav_file: WavFile):
        """Compress WAV using all available compressors"""

        # Huffman encoding
        self.huffman_encoder = HuffmanEncoder(wav_file)
        self.huffman_encoder.encode_wav()

        # LZW encoding
        self.lzw_encoder = LZWEncoder(wav_file)
        self.lzw_encoder.encode_wav()

        # LZW-based Huffman encoding
        LZW_encoded = self.lzw_encoder.encoded_samples
        self.LZW_based_huffman_encoded = self.huffman_encoder.encode(LZW_encoded)
        assert(self.LZW_based_huffman_encoded!= LZW_encoded)

        # Huffman-based LZW encoding
        huffman_encoded = self.huffman_encoder.encoded_samples
        self.Huffman_based_LZW_encoded = self.lzw_encoder.encode(huffman_encoded)
        assert(self.Huffman_based_LZW_encoded != huffman_encoded)

    def get_huffman_compression_ratio(self):
        """Compress WAV using Huffman compression"""
        return self.huffman_encoder.compression_ratio()

    def get_LZW_compression_ratio(self):
        """Compress WAV using LZW compression"""
        return self.lzw_encoder.compression_ratio()

    def get_huffman_based_LZW_compression_rate(self):
        """Compress WAV using Huffman first and then LZW compression"""
        return self.huffman_encoder.compression_ratio(self.Huffman_based_LZW_encoded)

    def get_LZW_based_huffman_compression_rate(self):
        """Compress WAV using LZW first and then Huffman compression"""
        return self.lzw_encoder.compression_ratio(self.LZW_based_huffman_encoded)

class ImageCompressor:
    def __init__(self):
        pass

    def compress(image: List[List[int]]) -> List[List[int]]:
        """Compress an image in JPEG"""
        pass
