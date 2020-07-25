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
test_layers_to_vector_cases = [
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


@pytest.mark.parametrize("case", test_layers_to_vector_cases)
def test_layers_to_vector(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.A))

    im = IMGFile()
    result = im.layers_to_vector(case.A)

    log.debug("Result: " + str(result))
    assert(result == case.B)


@pytest.mark.parametrize("case", test_layers_to_vector_cases)
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
    os.remove(filename)


def test_read_write(test_file):
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

#########################################
#                                       #
# Read/write                            #
#                                       #
#########################################

test_byte_array_cases = [
    InputOutputCase(
        name="Nominal",
        A="1111111100000000",
        B=[255, 0]
    )
]

@pytest.mark.parametrize("case", test_byte_array_cases)
def test_byte_array(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.A))

    im = IMGFile()
    result = im.str_to_byte_array(case.A)

    log.debug("Result: " + str(result))
    assert(result == case.B)
