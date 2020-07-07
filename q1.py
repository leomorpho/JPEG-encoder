from src.ui.ui import MainWindowQ1
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindowQ1()
    window.show()
    app.exec_()
