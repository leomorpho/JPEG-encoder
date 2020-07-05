from src.ui import MainWindow
from PyQt5.QtGui import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
