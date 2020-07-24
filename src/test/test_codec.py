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
            [ # Layer 1
                [[123, 123], [123, 123]],
            ],
            [ # Layer 2
                [[123, 123], [123, 123]],
            ],
            [ # Layer 3
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
    tree_byte_length = 14
    data_byte_length = 28
    filename = test_file

    im._width = width
    im._height = height
    im._block_size = block_size
    im._tree_byte_length = tree_byte_length
    im._data_byte_length = data_byte_length

    im.write(filename)
    im.read(filename)

    assert(im._width == width)
    assert(im._height== height)
    assert(im._block_size == block_size)
    assert(im._tree_byte_length == tree_byte_length)
    assert(im._data_byte_length == data_byte_length)

