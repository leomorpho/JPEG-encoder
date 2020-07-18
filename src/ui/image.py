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
                colorQt = None
                if self.effect == "grayscale":
                    avg = int((color[0] + color[1] + color[2]) / 3)
                    colorQt = qRgb(avg, avg, avg)
                elif self.effect == "darken":
                    mult = 0.5
                    R = int(mult * color[0])
                    G = int(mult * color[1])
                    B = int(mult * color[2])
                    colorQt = qRgb(R, G, B)
                elif self.effect == "vivid":
                    colors = [color[0], color[1], color[2]]
                    colors = self.make_vivid(colors)
                    colorQt = qRgb(colors[0], color[1], color[2])
                else:
                    colorQt = qRgb(color[0], color[1], color[2])
                image.setPixel(x_position, y_position, colorQt)

        pixmap = QPixmap(image)
        painter.drawPixmap(self.rect(), pixmap)

    def make_vivid(self, colors: List[int]) -> List[int]:
        """Push each pixel towards light or dark, depending on initial state"""
        grey = int((colors[0] + colors[1] + colors[2]) / 3)
        for index, val in enumerate(colors):
            colors[index] = int(val * 2 - grey * 0.9)
            if colors[index] > 255:
                colors[index] = 255
            if colors[index] < 0:
                colors[index] = 0
        return colors

