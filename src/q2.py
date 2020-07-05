from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import List
import logging
import struct
import operator

BLACK = 0
WHITE = 255
LITTLE_ENDIAN = '< '
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class WavFile():
    def __init__(self, filename):
        """
        :param chunkID: Contains the letters "RIFF" in ASCII form: (0x52494646 big-endian form).
        :type  chunkID: 4 byte str

        :param chunkSize: This is the size of the rest of the chunk following this number.
        :type  chunkSize: 4 byte int

        :param format: Contains the letters "WAVE": (0x57415645 big-endian form).
        :type format: 4 byte str

        :param subchunk1ID: Contains the letters "fmt ": (0x666d7420 big-endian form).
        :type  subchunk1ID: 4 byte str

        :param subchunk1Size: 16 for PCM.  This is the size of the rest of the Subchunk which follows this number.
        :type  subchunk1Size: 4 byte int

        :param audioFormat: PCM = 1 (i.e. Linear quantization). Values other than 1 indicate some form of compression.
        :type  audioFormat: 2 byte int

        :param numChannels: Mono = 1, Stereo = 2, etc.
        :type  numChannels: 2 byte int

        :param samplesPerSec: 8000, 44100, etc.
        :type  samplesPerSec: 4 byte int

        :param avgBytePerSec: == samplesPerSec * NumChannels * BitsPerSample / 8
        :type  avgBytePerSec: 4 byte int

        :param blockAlign: == NumChannels * BitsPerSample / 8. The number of bytes for one sample including all channels.
        :type  blockAlign: 2 byte int

        :param bitsPerSample: 8 bits = 8, 16 bits = 16, etc.
        :type  bitsPerSample: 2 byte int

        :param subchunk2ID: Contains the letters "data": (0x64617461 big-endian form).
        :type  subchunk2ID: 4 byte str

        :param subchunk2Size: == NumSamples * NumChannels * BitsPerSample / 8. Number of bytes in the data following this field.
        :type  subchunk2Size: 2 byte int

        """
        self.chunkID = []
        self.chunkSize = []
        self.format = ""
        self.subchunk1ID = ""
        self.subchunk1Size = ""
        self.audioFormat = 0
        self.numChannels = 0
        self.samplesPerSec = 0
        self.avgBytePerSec = 0
        self.blockAlign = 0
        self.bitsPerSample = 0
        self.subchunk2ID = ""
        self.subchunk2Size = 0
        self.maxValInSamples = 0

        self.open_file(filename)

    def open_file(self, filename: str):
        """Read and construct WavFile object
        """
        with open(filename, "rb") as f:
            self.chunkID = f.read(4)
            self.chunkSize = self.unpack('I', f.read(4))
            self.format = f.read(4)
            self.subchunk1ID = f.read(4)
            self.subchunk1Size = self.unpack('I', f.read(4))
            self.audioFormat = self.unpack('H', f.read(2))
            self.numChannels = self.unpack('H', f.read(2))
            self.samplesPerSec = self.unpack('I', f.read(4))
            self.avgBytePerSec = self.unpack('I', f.read(4))
            self.blockAlign = self.unpack('H', f.read(2))
            self.bitsPerSample = self.unpack('H', f.read(2))
            self.subchunk2ID = f.read(4)
            self.subchunk2Size = self.unpack('H', f.read(2))
            self.maxValInSamples = 0
            self.data = self.load_data(f)

    def unpack(self, flag, byte_data: bytes):
        return struct.unpack(LITTLE_ENDIAN + flag, byte_data)[0]

    def load_data(self, f: str):
        """Read the actual data stored in the WAV file"""
        data = []
        bytesPerSample = int(self.bitsPerSample / 8)
        numSamples = int(self.subchunk2Size / bytesPerSample)

        flag = None
        if bytesPerSample == 1:
            flag = "B"
        elif bytesPerSample == 2:
            flag = "H"
        elif bytesPerSample == 4:
            flag = "I"
        else:
            raise Exception("No flag for this bytePerSample")

        for _ in range(numSamples):
            sample = self.unpack(flag, f.read(bytesPerSample))
            if sample > self.maxValInSamples:
                self.maxValInSamples = sample
            data.append(sample)
        return data

    def onResize(self, event):
        pass

    def __repr__(self):
        valDict = {
            "chunkID": self.chunkID,
            "chunkSize": self.chunkSize,
            "format": self.format,
            "subchunk1ID": self.subchunk1ID,
            "subchunk1Size": self.subchunk1Size,
            "audioFormat": self.audioFormat,
            "numChannels": self.numChannels,
            "samplesPerSec": self.samplesPerSec,
            "avgBytePerSec": self.avgBytePerSec,
            "blockAlign": self.blockAlign,
            "bitsPerSample": self.bitsPerSample,
            "subchunk2ID": self.subchunk2ID,
            "subchunk2Size": self.subchunk2Size,
            "maxValInSample": self.maxValInSamples
        }
        formatted_repr = "{"
        for key, val in valDict.items():
            formatted_repr += f"\t{key}: \t{val}\n"

        formatted_repr += "}"
        return formatted_repr

    @property
    def samples(self):
        return self.data

    @property
    def getBitsPerSample(self):
        return self.bitsPerSample

    @property
    def time_quantization(self):
        return self.subchunk2Size


class WavInfo(QWidget):
    def __init__(self, wavFile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wavFile = wavFile
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(f"{'max val in samples:': <25}{str(self.wavFile.maxValInSamples): >12}"))
        layout.addWidget(QLabel(
            f"{'total number of samples:': <25} {str(len(self.wavFile.samples)): >12}"))
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        layout.addWidget(QLabel("HEADER INFORMATION:"))
        layout.addWidget(
            QLabel(f"{'chunkID:': <25}{str(self.wavFile.chunkID): >12}"))
        layout.addWidget(
            QLabel(f"{'chunkSize:': <25}{str(self.wavFile.chunkSize): >12}"))
        layout.addWidget(
            QLabel(f"{'format:': <25}{str(self.wavFile.format): >12}"))
        layout.addWidget(
            QLabel(f"{'subchunk1ID:': <25}{str(self.wavFile.subchunk1ID): >12}"))
        layout.addWidget(
            QLabel(f"{'subchunk1Size:': <25}{str(self.wavFile.subchunk1Size): >12}"))
        layout.addWidget(
            QLabel(f"{'audioFormat:': <25}{str(self.wavFile.audioFormat): >12}"))
        layout.addWidget(
            QLabel(f"{'numChannels:': <25}{str(self.wavFile.numChannels): >12}"))
        layout.addWidget(
            QLabel(f"{'samplesPerSec:': <25} {str(self.wavFile.samplesPerSec): >12}"))

        layout.addWidget(
            QLabel(f"{'avgBytePerSec:': <25}{str(self.wavFile.avgBytePerSec): >12}"))
        layout.addWidget(
            QLabel(f"{'blockAlign:': <25}{str(self.wavFile.blockAlign): >12}"))
        layout.addWidget(
            QLabel(f"{'bitsPerSample:': <25}{str(self.wavFile.bitsPerSample): >12}"))
        layout.addWidget(
            QLabel(f"{'subchunk2ID:': <25}{str(self.wavFile.subchunk2ID): >12}"))
        layout.addWidget(
            QLabel(f"{'subchunk2Size:': <25}{str(self.wavFile.subchunk2Size): >12}"))


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


def fade_in_and_out(matrix):
    for i, row in enumerate(matrix):
        matrix[i] = fade_row(row)

    return matrix


def fade_row(row):
    end = len(row)
    middle = int(len(row) / 2)
    step = 256 / middle
    fade = 256

    # First half of list
    for i in range(middle):
        val = int(row[i] + fade)
        if val > 255:
            val = 255
        row[i] = val
        fade -= step

    # Second half of list
    for i in range(middle, end):
        val = int(row[i] + fade)
        if val > 255:
            val = 255
        row[i] = val
        fade += step

    return row


class WaveformImage(QWidget):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wavFile = WavFile(filename)
        self.samples: List[int] = self.wavFile.samples
        self.downsampled_samples = []
        self.setMinimumSize(1000, 600)

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
        temp = fade_in_and_out(self.matrix)
        self.matrix = temp

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


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.audio_file_path = None
        self.current_effect = None

        # Initialize all other params
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("WAV Waveform Viewer")

        # Menu
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        self.file_menu = self.menu.addMenu("File")

        # Open File QAction
        open_action = QAction("Open WAV file", self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open WAV image')
        open_action.triggered.connect(self.openFileDialogueBox)
        self.file_menu.addAction(open_action)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)

        if not self.audio_file_path:
            self.openFileDialogueBox()
        else:
            self.setCentralWidget(central_widget)

    def openFileDialogueBox(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.List)
        if dialog.exec_():
            # Display image with info pane
            hbox = QHBoxLayout(self)

            # The selected file is stored in fileName
            self.audio_file_path = dialog.selectedFiles()[0]
            imageWidget = WaveformImage(self.audio_file_path)
            imageInfo = WavInfo(imageWidget.getWavFile)

            hbox.addWidget(imageWidget)
            hbox.addWidget(imageInfo)

            central_widget = QWidget()
            central_widget.setLayout(hbox)
            self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
