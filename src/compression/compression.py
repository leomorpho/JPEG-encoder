import logging
from typing import *
from src.codecs.wav import WavFile

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Compressor:
    def compress(self, wav_file):
        pass

    def get_huffman(self):
        return 3.2

    def get_LZW(self):
        return 2.3
