from typing import List
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.codecs.image import BmpFile, IMGFile
from src.compression.lossy import JPEG, read_JPEG
# TODO: remove json from everywhere
import json

img_format = "img"
bmp_format = "bmp"


class Image(QWidget):
    def __init__(self, path, compression=None, *args, **kwargs):
        """
        Display an image. If compression is set, will display the compressed image.
        """
        super().__init__(*args, **kwargs)

        file_extension = path.split(".")[-1]
        if file_extension.lower() == img_format:
            img = IMGFile()
            img.read(path)
            decoded = img.decode()
            self.matrix = read_JPEG(img.decode(), img.compression)
            with open("second.json", "w") as f:
                f.write(json.dumps(self.matrix))
            self.width = img.width
            self.height = img.height
            self.bytes_size = img.bytes_size
        elif file_extension.lower() == bmp_format:
            self.bmp_image = BmpFile(path)
            self.matrix = self.bmp_image.matrix
            self.width = self.bmp_image.width
            self.height = self.bmp_image.height
            self.bytes_size = self.bmp_image.bytes_size

            if compression:
                self.matrix, self.bytes_size = JPEG(
                    self.matrix, compression, path, self.width, self.height)
        else:
            raise NotImplementedError("Filetype not supported")

        self.path = path

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
        self.matrix, self.bytes_size = JPEG(
            self.bmp_image.matrix, compression_lvl,
            self.path, self.width, self.height)
        self.update()
