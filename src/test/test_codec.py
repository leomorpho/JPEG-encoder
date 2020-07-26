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


def test_read_write_simple(test_file):
    im = IMGFile()
    width = 80
    height = 64
    block_size = 8
    main_data_num_bytes = 3
    encoded_main_data = "1101111010101110101"
    main_data_padding = 5
    filename = test_file

    im._width = width
    im._height = height
    im._block_size = block_size
    im._main_data_num_bytes = main_data_num_bytes
    im._encoded_main_data = encoded_main_data
    im._main_data_padding = main_data_padding

    im.write(filename)
    im.read(filename)

    assert(im._width == width)
    assert(im._height == height)
    assert(im._block_size == block_size)
    assert(im._main_data_num_bytes == main_data_num_bytes)
    assert(im._encoded_main_data == encoded_main_data)
    assert(im._main_data_padding == main_data_padding)


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
    #assert(case.A == vector)

    assert(im._width is not None)
    assert(type(im._width) is int)

    assert(im._height is not None)
    assert(type(im._height) is int)

    assert(im._block_size is not None)
    assert(type(im._block_size) == int)

    assert(im._main_data_padding is not None)
    assert(type(im._main_data_padding) is int)

    assert(im._main_data_num_bytes is not None)
    assert(type(im._main_data_num_bytes) is int)

    assert(im._encoded_main_data is not None)
    assert(type(im._encoded_main_data) is str)
