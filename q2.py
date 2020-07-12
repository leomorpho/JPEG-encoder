from src.ui.ui import MainWindowQ2
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowQ2()
    window.show()
    app.exec_()
