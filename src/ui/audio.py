from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.codecs.wav import WavFile
import logging
from src.compression.compressor import SoundCompressor

log = logging.getLogger()
log.setLevel(logging.DEBUG)

BLACK = 0
WHITE = 255


class WaveformImage(QWidget):
    def __init__(self, wavFile, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wavFile = wavFile
        self.samples: List[int] = self.wavFile.samples
        self.downsampled_samples = []
        self.setMinimumSize(700, 500)

        self.create_matrix()

    @property
    def getWavFile(self):
        return self.wavFile

    def create_matrix(self):
        # Matrix must be downsized. If not, it can be HUGE (aka
        # 50,000 by 50,000), which crashes python.

        # Image dimensions
        self.time_pixels = 2000
        self.amplitude_pixels = 512

        if self.time_pixels > len(self.samples):
            self.time_pixels = len(self.samples)

        bitRange = 2**self.wavFile.getBitsPerSample
        if self.amplitude_pixels > bitRange:
            self.amplitude_pixels = bitRange

        temp = downsample_time(self.samples, self.time_pixels)
        self.downsampled_samples = downsample_amplitude(
            temp,
            bitRange,
            self.amplitude_pixels)

        self.matrix = [[] for i in range(self.amplitude_pixels)]
        middle = int(self.amplitude_pixels / 2)

        for t, val in enumerate(self.downsampled_samples):
            for l in range(self.amplitude_pixels):
                if l >= middle - 0.5 * self.downsampled_samples[t] and \
                        l <= middle + 0.5 * self.downsampled_samples[t]:
                    self.matrix[l].append(BLACK)
                else:
                    self.matrix[l].append(WHITE)

    def paintEvent(self, event):

        painter = QPainter(self)

        black = qRgb(0, 0, 0)
        white = qRgb(255, 255, 255)

        image = QImage(self.time_pixels,
                       self.amplitude_pixels,
                       QImage.Format_RGB32)

        for y_position in range(self.amplitude_pixels):
            for x_position in range(self.time_pixels):
                try:
                    color = self.matrix[y_position][x_position]
                    colorQt = qRgb(color, color, color)
                    image.setPixel(x_position, y_position, colorQt)
                except:
                    pass

        pixmap = QPixmap(image)
        painter.drawPixmap(self.rect(), pixmap)


def downsample_time(list_object, max_val):
    # Compress the number of items in the list by scale_factor
    scale_factor = int(len(list_object) / max_val)
    unaccounted = len(list_object) % max_val
    log.info(f"scale_factor: {scale_factor}")
    log.info(f"unaccounted: {unaccounted}")

    new_list_object = []

    # queue holds value to be averaged
    queue = []

    for index, val in enumerate(list_object):
        queue.append(val)

        if len(queue) >= scale_factor:
            new_list_object.append(average(queue))
            queue = []
    new_list_object[-1] = average(queue + [new_list_object[-1]])

    return new_list_object


def downsample_amplitude(list_object, max_val_old, max_val_new):
    """
    :param list_object: object to scale
    :param max_val_old: maximum value for any item in list_object
    :param max_val_new: new maximum value for any item in list_object
    """
    # Scale the value of each item in the list
    for index, val in enumerate(list_object):
        list_object[index] = scale(val, max_val_old, max_val_new)

    return list_object


def average(list_object: list) -> int:
    log.debug(f"average this list: {list_object}")
    sum = 0
    for i in list_object:
        sum += i

    return int(sum / len(list_object))


def scale(
        x: int,
        x_max_val: int,
        new_range: int) -> int:
    """
    Scale a number into a new range.

    :param x: number to scale
    :param x_max_val: max value of number to normalize
    :param new_range: new wanted range
    """
    return int(x * new_range / x_max_val)


class InfoWidget(QWidget):
    def __init__(self, infoDict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout(self)

        left_widget = QWidget()
        layout_l = QVBoxLayout(self)
        layout_l.addWidget(QLabel("Huffman compression ratio"))
        layout_l.addWidget(QLabel("LZW compression ratio"))
        layout_l.addWidget(QLabel("Huffman-based LZW compression ratio"))
        layout_l.addWidget(QLabel("LZW-based Huffman compression ratio"))
        left_widget.setLayout(layout_l)

        right_widget = QWidget()
        layout_r = QVBoxLayout(self)
        layout_r.addWidget(QLabel(str(infoDict["Huffman"])))
        layout_r.addWidget(QLabel(str(infoDict["LZW"])))
        layout_r.addWidget(QLabel(str(infoDict["Huffman-LZW"])))
        layout_r.addWidget(QLabel(str(infoDict["LZW-Huffman"])))
        right_widget.setLayout(layout_r)

        layout.addWidget(left_widget)
        layout.addWidget(right_widget)
        self.setLayout(layout)
