from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from src.codecs.wav import WavFile
from src.codecs.image import BmpFile
import logging
from src.compression.compressor import SoundCompressor
from src.ui.audio import WaveformImage, InfoWidget
from src.ui.image import Image

log = logging.getLogger()
log.setLevel(logging.DEBUG)

img_format = "img"
bmp_format = "bmp"


class MainWindowQ1(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.audio_file_path = None

        # Initialize all other params
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("WAV Compression")

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

            self.audio_file_path = dialog.selectedFiles()[0]
            wav_file = WavFile(self.audio_file_path)

            imageWidget = WaveformImage(wav_file)

            cps = SoundCompressor()
            cps.compress(wav_file)
            infoDict = {
                "Huffman": cps.get_huffman_compression_ratio(),
                "LZW": cps.get_LZW_compression_ratio(),
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
        self.image_file_path = None

        # Initialize all other params
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("BMP Compression")

        # Menu
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        self.file_menu = self.menu.addMenu("File")

        # Open File QAction
        open_action = QAction("Compress BMP file", self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Compress BMP file')
        open_action.triggered.connect(self.openFileDialogueBox)
        self.file_menu.addAction(open_action)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)

        if not self.image_file_path:
            self.openFileDialogueBox()
        else:
            self.setCentralWidget(central_widget)

        # self.showMaximized()

    def openFileDialogueBox(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.List)
        if dialog.exec_():
            # Display image with info pane
            hbox = QHBoxLayout(self)

            self.image_file_path = dialog.selectedFiles()[0]

            file_extension = self.image_file_path.split(".")[-1]

            if file_extension.lower() == img_format:
                image_widget = Image(self.image_file_path)
                hbox.addWidget(image_widget)
            elif file_extension.lower() == bmp_format:
                # TODO: toolbar is not working correctly
                # self.add_toolbar()
                self.original_image_widget = Image(self.image_file_path)
                self.compressed_image_widget = Image(
                    self.image_file_path, compression=50)
                print(
                    f"Original:   {self.original_image_widget.bytes_size} bytes")
                print(
                    f"Compressed: {self.compressed_image_widget.bytes_size} bytes")
                print(
                    f"Compression time: {self.compressed_image_widget.compression_time}"
                )
                print(
                    f"Decompression time: {self.compressed_image_widget.decompression_time}"
                )

                print(
                    f"PSNR: {self.compressed_image_widget.psnr}"
                )
                # To hold compression information
                vbox = QVBoxLayout()
                qr = self.original_image_widget.bytes_size / \
                    self.compressed_image_widget.bytes_size
                compression_ratio = QLabel(f"Compression ratio: {round(qr, 2)}")
                size_original = QLabel(
                    f"Original:   {self.original_image_widget.bytes_size} bytes")
                size_compressed = QLabel(
                    f"Compressed: {self.compressed_image_widget.bytes_size} bytes")
                compression_time = QLabel(
                    f"Compression time: {round(self.compressed_image_widget.compression_time, 2)}s")
                decompression_time = QLabel(
                    f"Decompression time: {round(self.compressed_image_widget.decompression_time, 2)}s")
                psnr = QLabel(
                    f"PSNR: {round(self.compressed_image_widget.psnr, 2)}dB")

                vbox.addWidget(compression_ratio)
                vbox.addWidget(size_original)
                vbox.addWidget(size_compressed)
                vbox.addWidget(compression_time)
                vbox.addWidget(decompression_time)
                vbox.addWidget(psnr)

                info_widget = QWidget()
                info_widget.setLayout(vbox)

                hbox.addWidget(self.original_image_widget)
                hbox.addWidget(self.compressed_image_widget)
                hbox.addWidget(info_widget)
            else:
                raise NotImplementedError("Filetype not supported")

            central_widget = QWidget()
            central_widget.setLayout(hbox)
            self.setCentralWidget(central_widget)

    def compress_90(self):
        """
        Apply 90% compression to original image
        """
        self.change_compression(90)

    def compress_50(self):
        """
        Apply 50% compression to original image
        """
        self.change_compression(50)

    def compress_10(self):
        """
        Apply 10% compression to original image
        """
        self.change_compression(10)

    def change_compression(self, level):
        """
        Change compression level and update UI
        """
        self.compressed_image_widget.update_image(level)
        print(f"Original:   {self.original_image_widget.bytes_size} bytes")
        print(
            f"Compressed: {self.compressed_image_widget.bytes_size} bytes")

    def add_toolbar(self):
        # Change JPEG levels
        # 90%
        ninety = QAction("Q90", self)
        ninety.setStatusTip("90% compression")
        ninety.triggered.connect(self.compress_90)

        # 50%
        fifty = QAction("Q50", self)
        fifty.setStatusTip("50% compression")
        fifty.triggered.connect(self.compress_50)

        # 10%
        ten = QAction("Q10", self)
        ten.setStatusTip("10% compression")
        ten.triggered.connect(self.compress_10)

        self.toolbar = self.addToolBar('90%')
        self.toolbar.addAction(ninety)
        self.toolbar = self.addToolBar('50%')
        self.toolbar.addAction(fifty)
        self.toolbar = self.addToolBar('10%')
        self.toolbar.addAction(ten)
