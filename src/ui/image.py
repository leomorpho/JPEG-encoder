from typing import List
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Image(QWidget):
    def __init__(self, path, effect=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bmp_image = BmpFile(path)
        self.path = path
        self.effect = effect
        self.matrix = self.bmp_image.matrix
        self.width = self.bmp_image.width
        self.height = self.bmp_image.height
        self.setMinimumSize(int(self.width * 1.5), int(self.height * 1.5))


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
        painter.drawPixmap(self.rect(), pixmap)
