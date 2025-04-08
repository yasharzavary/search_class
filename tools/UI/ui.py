import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                                QVBoxLayout, QWidget, QLabel,
                                QPushButton)
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap

from .graphs import *

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # information of page
        self.setWindowTitle("Graph")
        self.setGeometry(200, 150, 600, 700)
        cenral_widget = QWidget()
        self.setCentralWidget(cenral_widget)


        # main layout
        main_layout = QHBoxLayout(cenral_widget)


        # graphic scene details
        self.scene = GraphScene()
        self.view = GraphView(self.scene)
        self.scene.add_node('x', 0, 0)

        # tools layout
        tool_layout = QVBoxLayout()
        change_button = QPushButton('Change')
        exit_button = QPushButton('Exit')

        tool_layout.addWidget(change_button, alignment=Qt.AlignTop)
        tool_layout.addWidget(exit_button, alignment=Qt.AlignBottom)

        # adding to main layout
        main_layout.addWidget(self.view)
        main_layout.addLayout(tool_layout)


