from typing import List
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.codecs.image import BmpFile, IMGFile
from src.compression.lossy import JPEG

img_format = "img"
bmp_format = "bmp"

class Image(QWidget):
    def __init__(self, path, compression=None, *args, **kwargs):
        """
        Display an image. If compression is set, will display the compressed image.
        """
        super().__init__(*args, **kwargs)

        file_extension = self.image_file_path.split(".")[-1]
        if file_extension.lower()  == img_format:
            self.img_image = BmpFile(path)
            self.matrix = self.img_image.matrix
            self.width = self.img_image.width
            self.height = self.img_image.height
            self.bytes_size = self.img_image.bytes_size
        elif file_extension.lower()  == bmp_format:
            self.bmp_image = BmpFile(path)
            self.matrix = self.bmp_image.matrix
            self.width = self.bmp_image.width
            self.height = self.bmp_image.height
            self.bytes_size = self.bmp_image.bytes_size
        else:
            raise NotImplementedError("Filetype not supported")


        self.path = path

        if compression:
            self.matrix, self.bytes_size = JPEG(self.matrix, compression)

        self.setMinimumSize(int(self.width), int(self.height))

    @property
    def get_bmp_image(self):
        return self.bmp_image

    def onResize(self, event):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)

        image = QImage(self.width, self.height, QImage.Format_RGB32)

        # Create image from matrix
        for y_position in range(self.height):
            for x_position in range(self.width):
                color = self.matrix[y_position][x_position]
                colorQt = qRgb(color[0], color[1], color[2])
                image.setPixel(x_position, y_position, colorQt)

        pixmap = QPixmap(image)
        pixmap = pixmap.scaled(self.height, self.width, Qt.KeepAspectRatio)
        painter.drawPixmap(self.rect(), pixmap)

    def update_image(self, compression_lvl):
        self.matrix = JPEG(self.bmp_image.matrix, compression_lvl)
        self.update()
