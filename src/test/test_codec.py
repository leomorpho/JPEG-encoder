import pytest
import logging
from src.codecs.image import IMGFile
import os

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, A, B):
        self.name = name
        self.A = A
        self.B = B

#########################################
#                                       #
# Convert btw layers and vectors        #
#                                       #
#########################################


# 3 layers of vectors for Y, Cb, Cr
full_image_test_cases = [
    InputOutputCase(
        name="Nominal",
        A=[
            [  # Layer 1
                [[123, 123], [123, 123]],
            ],
            [  # Layer 2
                [[123, 123], [123, 123]],
            ],
            [  # Layer 3
                [[123, 123], [123, 123]],
            ]
        ],
        B=[123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    )
]


@pytest.mark.parametrize("case", full_image_test_cases)
def test_layers_to_vector(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.A))

    im = IMGFile()
    result = im.layers_to_vector(case.A)

    log.debug("Result: " + str(result))
    assert(result == case.B)


@pytest.mark.parametrize("case", full_image_test_cases)
def test_vector_to_layers(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.B))

    im = IMGFile()
    im._width = 2
    im._height = 2
    im._block_size = 2
    result = im.vector_to_layers(case.B)

    log.debug("Result: " + str(result))
    assert(result == case.A)


#########################################
#                                       #
# Read/write                            #
#                                       #
#########################################

@pytest.fixture
def test_file():
    filename = "test.img"
    yield filename
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass


class EncodedData():
    """Represents a test case with input_val and expected expected_output"""
    def __init__(
            self,
            encoded_main_data,
            main_data_padding,
            bytes_size):
        self.encoded_main_data = encoded_main_data
        self.main_data_padding = main_data_padding
        self.bytes_size = bytes_size

encoded_main_data_cases = [
    EncodedData(
        encoded_main_data="0010101110",
        main_data_padding=6,
        bytes_size=32,
    ),
    EncodedData(
        encoded_main_data="10010101010000011111110101",
        main_data_padding=6,
        bytes_size=48,
    ),
    EncodedData(
        encoded_main_data="1101111010101110101011000011001011010011011011100011101011110110111111000001000010100001000010011000101000110101010010010010110011010011110100010100110101010101110110010110110111010111100000010110000101001001001010000101111001100011010111100101111110011111111111100111111111111111100101111110110000110010110100110110111000111010111101101111110000010000101000010000100110001010001101010100100100101100110100111101000101001101010101011101100101101101110101111000000101100001010010010010100001011110011000110101111001011111100111111111111001111111111111111001011111101100001100101101001101101110001110101111011011111100000100001010000100001001100010100011010101001001001011001101001111010001010011010101010111011001011011011101011110000001011000010100100100101000010111100110001101011110010111111001111111111110011111111111111110010111111011000011001011010011011011100011101011110110111111000001000010100001000010011000101000110101010010010010110011010011110100010100110101010101110110010110110111010111100000010110000101001001001010000101111001100011010111100101111110011111111111100111111111111111100101111110110000110010110100110110111000111010111101101111110000010000101000010000100110001010001101010100100100101100110100111101000101001101010101011101100101101101110101111000000101100001010010010010100001011110011000110101111001011111100111111111111001111111111111111001011111101100001100101101001101101110001110101111011011111100000100001010000100001001100010100011010101001001001011001101001111010001010011010101010111011001011011011101011110000001011000010100100100101000010111100110001101011110010111111001111111111110011111111111111110010111111",
        main_data_padding=5,
        bytes_size=1672,
    )
]


@pytest.mark.parametrize("case", encoded_main_data_cases)
def test_read_write_simple(test_file, case):
    im = IMGFile()
    width = 80
    height = 64
    block_size = 8
    filename = test_file

    im._width = width
    im._height = height
    im._block_size = block_size
    im._encoded_main_data = case.encoded_main_data
    im._main_data_padding = case.main_data_padding

    im.write(filename)
    im.read(filename)

    assert(im._width == width)
    assert(im._height == height)
    assert(im._block_size == block_size)
    assert(im._main_data_padding == case.main_data_padding)
    assert(im._encoded_main_data == case.encoded_main_data)
    assert(im.bytes_size == case.bytes_size)

full_image_test_case = [
    InputOutputCase(
        name="Nominal",
        A=[
            [  # Layer 1
                [
                    [1295, 554, -94, 128, 167, 253, 90, 0, 43, 170, 152, -24, -24, 3, 21, 25, -11, -34, -47, -74, 62, 26, -32, -18, -22, -16, -20,
                        11, 14, -1, 1, 4, 3, -10, -11, 13, 0, 0, 10, 2, 1, 0, -10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0, 0],
                    [1295, 554, -94, 128, 167, 253, 90, 0, 43, 170, 152, -24, -24, 3, 21, 25, -11, -34, -47, -74, 62, 26, -32, -18, -22, -16, -20,
                        11, 14, -1, 1, 4, 3, -10, -11, 13, 0, 0, 10, 2, 1, 0, -10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0, 0]
                ]
            ],
            [  # Layer 2
                [
                    [1295, 554, -94, 128, 167, 253, 90, 0, 43, 170, 152, -24, -24, 3, 21, 25, -11, -34, -47, -74, 62, 26, -32, -18, -22, -16, -20,
                        11, 14, -1, 1, 4, 3, -10, -11, 13, 0, 0, 10, 2, 1, 0, -10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0, 0],
                    [1295, 554, -94, 128, 167, 253, 90, 0, 43, 170, 152, -24, -24, 3, 21, 25, -11, -34, -47, -74, 62, 26, -32, -18, -22, -16, -20,
                        11, 14, -1, 1, 4, 3, -10, -11, 13, 0, 0, 10, 2, 1, 0, -10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0, 0]
                ]
            ],
            [  # Layer 3
                [
                    [1295, 554, -94, 128, 167, 253, 90, 0, 43, 170, 152, -24, -24, 3, 21, 25, -11, -34, -47, -74, 62, 26, -32, -18, -22, -16, -20,
                        11, 14, -1, 1, 4, 3, -10, -11, 13, 0, 0, 10, 2, 1, 0, -10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0, 0],
                    [1295, 554, -94, 128, 167, 253, 90, 0, 43, 170, 152, -24, -24, 3, 21, 25, -11, -34, -47, -74, 62, 26, -32, -18, -22, -16, -20,
                        11, 14, -1, 1, 4, 3, -10, -11, 13, 0, 0, 10, 2, 1, 0, -10, 0, 0, 0, 10, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0, 0]
                ]
            ]
        ],
        B=""
    )
]


@pytest.mark.parametrize("case", full_image_test_case)
def test_encode_decode(case, test_file):
    im = IMGFile()
    filename = test_file

    im.encode(case.A)
    vector = im.decode()
    log.debug(im._encoded_main_data)
    assert(case.A == vector)


@pytest.mark.parametrize("case", full_image_test_case)
def test_read_write_full(case, test_file):
    im = IMGFile()
    filename = test_file

    im.encode(case.A)
    im.write(filename)
    im.read(filename)
    vector = im.decode()
    log.debug(im._encoded_main_data)
    assert(case.A == vector)

    assert(im._width is not None)
    assert(type(im._width) is int)

    assert(im._height is not None)
    assert(type(im._height) is int)

    assert(im._block_size is not None)
    assert(type(im._block_size) == int)

    assert(im._main_data_padding is not None)
    assert(type(im._main_data_padding) is int)

    assert(im._encoded_main_data is not None)
    assert(type(im._encoded_main_data) is str)
