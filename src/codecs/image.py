from typing import IO, Dict, List
import struct
import subprocess

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


class BmpCmnMixin:
    """Mixin that provides common functionality for Bmp files
    """

    def unpack(self, byte_data: bytes, endianness: str, unpack_type: str):
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


class BmpFileHeader(BmpCmnMixin):
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


class BmpImageHeader(BmpCmnMixin):
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


class BmpColorTable(BmpCmnMixin):
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


class BmpPixelData(BmpCmnMixin):
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


class BmpFile(BmpCmnMixin):
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
