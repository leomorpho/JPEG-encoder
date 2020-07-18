from typing import List
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.codecs.image import BmpFile


class Image(QWidget):
    def __init__(self, path=None, matrix=None, *args, **kwargs):
        """
        Image can display an image given either:
            - A path to a BMP image
            - a matrix representing an image
        """
        super().__init__(*args, **kwargs)

        if path:
            self.bmp_image = BmpFile(path)
            self.path = path
            self.matrix = self.bmp_image.matrix
            self.width = self.bmp_image.width
            self.height = self.bmp_image.height
        elif matrix:
            self.matrix = matrix
            self.width = len(matrix[0])
            self.height = len(matrix)
        else:
            raise Exception("Image format not supported")

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
