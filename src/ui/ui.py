from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.codecs.wav import WavFile
import logging
from src.compression.compressor import SoundCompressor
from src.ui.audio import WaveformImage, InfoWidget
from src.ui.image import Image

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class MainWindowQ1(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.audio_file_path = None

        # Initialize all other params
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("WAV/BMP Compression")

        # Menu
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        self.file_menu = self.menu.addMenu("File")

        # Open File QAction
        open_action = QAction("Compress WAV file", self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Compress WAV file')
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
            vbox = QVBoxLayout(self)

            # The selected file is stored in fileName
            self.audio_file_path = dialog.selectedFiles()[0]
            wav_file = WavFile(self.audio_file_path)

            imageWidget = WaveformImage(wav_file)

            cps = SoundCompressor()
            cps.compress(wav_file)
            infoDict = {
                "Huffman": cps.get_huffman_compression_ratio(),
                "LZW": cps.get_LZW_compression_ratio(),
                "Huffman-LZW": cps.get_huffman_based_LZW_compression_rate(),
                "LZW-Huffman": cps.get_LZW_based_huffman_compression_rate()
            }

            infoWidget = InfoWidget(infoDict)

            vbox.addWidget(imageWidget)
            vbox.addWidget(infoWidget)

            central_widget = QWidget()
            central_widget.setLayout(vbox)
            self.setCentralWidget(central_widget)


class MainWindowQ2(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.audio_file_path = None

        # Initialize all other params
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("WAV/BMP Compression")

        # Menu
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        self.file_menu = self.menu.addMenu("File")

        # Open File QAction
        open_action = QAction("Compress WAV file", self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Compress WAV file')
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
            vbox = QVBoxLayout(self)

            # The selected file is stored in fileName
            self.audio_file_path = dialog.selectedFiles()[0]
            wav_file = WavFile(self.audio_file_path)

            imageWidget = WaveformImage(wav_file)

            cps = Compressor()
            cps.compress(wav_file)
            infoDict = {
                "Huffman": cps.get_huffman_compression_ratio(),
                "LZW": cps.get_LZW_compression_ratio(),
                "Huffman-LZW": cps.get_huffman_based_LZW_compression_rate(),
                "LZW-Huffman": cps.get_LZW_based_huffman_compression_rate()
            }

            infoWidget = InfoWidget(infoDict)

            vbox.addWidget(imageWidget)
            vbox.addWidget(infoWidget)

            central_widget = QWidget()
            central_widget.setLayout(vbox)
            self.setCentralWidget(central_widget)
