from typing import IO, Dict, List
import struct
import subprocess
import logging
from src.compression.lossless import HuffmanEncoder

log = logging.getLogger()
log.setLevel(logging.DEBUG)

L_ENDIAN = '< '  # little endian
BYTE1 = 1       # 1 byte
BYTE2 = 2       # 2 byte
BYTE3 = 2       # 3 byte
BYTE4 = 4       # 4 byte
UCHAR = "B"      # unsigned char    (1 byte)
USHORT = "H"    # unsigned short    (2 byte)
UINT = "I"      # unsigned int      (4 byte)
SINT = "i"      # signed int        (4 byte)

PATH_IMAGES = "./testdata/Proj1_Q3_Sample_Inputs/"


class CmnMixin:
    """Mixin that provides common functionality for Bmp files
    """

    def unpack(self,
               byte_data: bytes,
               endianness: str = None,
               unpack_type: str = None):
        """
        Unpacks bytes
        """
        flags = endianness + " " + unpack_type
        return struct.unpack(flags, byte_data)[0]

    def __repr__(self):
        """Pretty prints all attributes of object
        """
        # return "%s(%r)" % (self.__class__, self.__dict__)

        formatted_repr = f"{self.__class__}\n"
        for attr, val in self.__dict__.items():
            formatted_repr += "\t%20s: %12s\n" % (attr, val)
        return formatted_repr


class BmpFileHeader(CmnMixin):
    def __init__(self, f: IO):
        """
        :param f: file to read
        :type  f: file handle

        :attr _signature: 'BM'
        :attr _file_size: file size in bytes
        :attr _reserved: unused (=0)
        :attr _data_offset: offset from beginning of file to
            the beginning of the bitmap data
        """
        self._signature: str = f.read(BYTE2)
        self._file_size: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._reserved: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._data_offset: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)

    @property
    def data_offset(self):
        return self._data_offset


class BmpImageHeader(CmnMixin):
    def __init__(self, f: IO):
        """
        :param f: file to read
        :type  f: file handle

        :attr _size: size of InfoHeader =40
        :attr _width: horizontal width of bitmap in pixels
        :attr _height: vertical height of bitmap in pixels. The pixel data is ordered from bottom to top.
            If this value is negative, then the data is ordered from top to bottom.
        :attr _planes: number of Planes (=1)
        :attr _bits_per_pixel: bits per pixel used to store palette entry information.
            This also identifies in an indirect way the number of possible colors. Possible values are:
                1 = monochrome palette. NumColors = 1
                4 = 4bit palletized. NumColors = 16
                8 = 8bit palletized. NumColors = 256
                16 = 16bit RGB. NumColors = 65536
                24 = 24bit RGB. NumColors = 16M
        :attr _compression: Type of Compression
                0 = BI_RGB   no compression
                1 = BI_RLE8 8bit RLE encoding
                2 = BI_RLE4 4bit RLE encoding
        :attr _image_size: (compressed) Size of Image. =0 if Compression = 0
        :attr _X_pixels_per_M: horizontal resolution: Pixels/meter
        :attr _X_pixels_per_M: vertical resolution: Pixels/meter
        :attr _colors_used: number of actually used colors.
            For a 8-bit / pixel bitmap this will be 100h or 256.
        :attr _important_colors: Number of important colors. 0 = all
        """
        self._size: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._width: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._height: int = self.unpack(f.read(BYTE4), L_ENDIAN, SINT)
        self._planes: int = self.unpack(f.read(BYTE2), L_ENDIAN, USHORT)
        self._bits_per_pixel: int = self.unpack(
            f.read(BYTE2), L_ENDIAN, USHORT)
        self._compression: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._image_size: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._X_pixels_per_M: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._Y_pixels_per_M: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._colors_user: int = self.unpack(f.read(BYTE4), L_ENDIAN, UINT)
        self._important_colors: int = self.unpack(
            f.read(BYTE4), L_ENDIAN, UINT)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class BmpColorTable(CmnMixin):
    def __init__(self, f: IO):
        """
        :attr _red: red intensity
        :attr _green: green intensity
        :attr _blue: blue intensity
        :attr _reserved: unused (=0)
        """
        self._red: int = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
        self._green: int = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
        self._blue: int = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
        self._reserved: int = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
        pass


class BmpPixelData(CmnMixin):
    def __init__(self,
                 f: IO,
                 width: int,
                 height: int):
        """
        :param f: filehandle to file storing BMP
        :param width: width of image
        :param height: height of image
        """
        self._data = []
        row = []
        count_height: int = 0
        count_width: int = 0

        RGB_BYTES = 3
        # Padding of rows
        diff = (RGB_BYTES * width) % BYTE4
        padding = 0
        if diff:
            padding = BYTE4 - diff

        for _ in range(height):
            row = []
            for _ in range(width):
                B = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
                G = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
                R = self.unpack(f.read(BYTE1), L_ENDIAN, UCHAR)
                row.append([R, G, B])
                count_width += 1

            # row is finished, discard padding from file handle
            for _ in range(padding):
                f.read(1)
            self._data.insert(0, row)
            count_height += 1

    @property
    def data(self):
        """Get the data"""
        return self._data

    def __repr__(self):
        return "h x w x d = " + str(len(self.data)) + " x " + str(len(self.data[0])) \
            + " x " + str(len(self.data[0][0]))


class BmpFile(CmnMixin):
    def __init__(self, filename):
        """
        :param
        """
        # Private
        self._file_header = None
        self._image_header = None
        self._color_table = None

        # Public
        self.pixel_data = None

        self.read_file(filename)

    def read_file(self, filename):
        """Reads and populates the differents structures
        of the BMP file
        """
        with open(filename, "rb") as f:
            self._file_header = BmpFileHeader(f)
            self._image_header = BmpImageHeader(f)
            self._color_table = BmpColorTable(f)

        with open(filename, "rb") as f:
            f.seek(54)
            self.pixel_data = BmpPixelData(
                f,
                self.width,
                self.height)

    @property
    def matrix(self):
        """Get the matrix"""
        return self.pixel_data.data

    @property
    def width(self):
        """Get width of image"""
        return self._image_header.width

    @property
    def height(self):
        """Get height of image"""
        return self._image_header.height


class IMGFile(CmnMixin):
    """
    Format of compressed BMP file using JPEG-like encoder
    """

    def __init__(self):
        """
        :attr signature: type of file
        :type signature: 2 byte
        :attr width: the width of the image in number of block
        :type width: 4 byte
        :attr height: the length of the image in number of block
        :type height: 4 byte
        :attr block_size: the number of values in a row or column of the blocks used
        :type block_size: 4 byte
        """
        self._Y = []
        self._Cb = []
        self._Cr = []

        self._signature: str = None
        self._width: int = None
        self._height: int = None
        self._block_size: int = None
        self._data_size: int = None

        self.huffman = HuffmanEncoder()

    def encode(self, layers: List[List[int]]):
        """
        :param layers: list of vectors of blocks. Each vector
            represents one block of the blocked image. There are no more
            distinctions between rows. Example of layers[0]:
            [[123, 122, ..., 124], ..., [231, 123, ..., 125]]
        """
        # Save dimensions for later decompression
        self._width = len(layers[0][0])
        self._height = len(layers[0])
        self._block_size = len(layers[0][0][0])

        # Make one vector out of all values
        one_vec = self.layers_to_vector(layers)
        self.vec = one_vec

        # Huffman encode
        self.vec = self.huffman.encode(one_vec)

        # Encode Y, Cb, Cr with Huffman
        # Write Huffman tree to file
        # Write encoded data to file

    def decode(self, filename=None):
        # self.read_file(filename)
        vec = self.vec
        # Read header to get width, height
        # TODO: read from class for now

        # Read Huffman tree and recreate it
        # TODO: read from huffman class for now
        vec = self.huffman.decode(vec)


        # Reassemble layers from one-dimensional vector
        layers = self.vector_to_layers(vec)

        return layers

    def read_file(self, filename):
        """
        Read the entire IMG file
        """
        with open(filename, "rb") as f:
            self._signature: str = f.read(BYTE2)
            self._width: int = self.unpack(f.read(BYTE4), unpack_type=UINT)
            self._height: int = self.unpack(f.read(BYTE4), unpack_type= UINT)
            self._block_size: int = self.unpack(f.read(BYTE4), unpack_type=UINT)

    def vector_to_layers(self, vector: List[int]) -> List[List[List[int]]]:
        """
        Used for decompression and reading form disk.
        """
        v_len = len(vector)

        # Extract all layers as vectors
        layer_1_vector = vector[:int(v_len/3)]
        layer_2_vector = vector[int(v_len/3):int(v_len/3*2)]
        layer_3_vector = vector[int(v_len/3*2):]

        # Separate rows
        layer_1 = self.subdivide_layer(layer_1_vector)
        layer_2 = self.subdivide_layer(layer_2_vector)
        layer_3 = self.subdivide_layer(layer_3_vector)

        layers = [layer_1, layer_2, layer_3]

        return layers

    def subdivide_layer(self, vector: List[int]) -> List[List[int]]:
        """
        Separate the rows of a one-dimensional vector layer.
        This is used for decompression.
        """
        layer = []
        row = []
        for i in vector:
            row.append(i)
            if len(row) == self._width * self._block_size:
                layer.append(self.subdivide_row(row))
                row = []

        return layer

    def subdivide_row(self, vector: List[int]) -> List[List[int]]:
        """
        Separate the blocks of a one-dimensional row vector layer.
        This is used for decompression.
        """
        row = []
        block = []

        for i in vector:
            block.append(i)
            if len(block) == self._block_size:
                row.append(block)
                block = []

        return row

    #############################
    #                           #
    # Static Methods            #
    #                           #
    #############################
    @staticmethod
    def layers_to_vector(layers: List[List[List[int]]]) -> List[int]:
        """
        Used for compression and writing to disk.
        """
        vector = []

        for layer in layers:
            for row in layer:
                for block in row:
                    for item in block:
                        vector.append(item)
        return vector

