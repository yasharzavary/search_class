import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # information of page
        self.setWindowTitle("Graph")
        self.setGeometry(200, 150, 600, 700)

        main_layout = QHBoxLayout()




