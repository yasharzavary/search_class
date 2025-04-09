import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                                QVBoxLayout, QWidget, QLabel,
                                QPushButton)
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap

from .graphs import *


# TODO: message box in bottom of window.


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

        # tools layout
        self.tool_layout = QVBoxLayout()
        self.__add_main_buttons()

        # adding to main layout
        main_layout.addWidget(self.view)
        main_layout.addLayout(self.tool_layout)

    def __exit(self):
        self.close()
    
    def __change(self):
        """
            when user want to change the graph, this function will trigger
        """
        self.__remove_widgets(self.tool_layout)
        # buttons definition
        add_note = QPushButton('Add Node')
        back_button = QPushButton('Back')

        back_button.clicked.connect(self.__add_main_buttons)
        add_note.clicked.connect(self.__add_node)

        self.tool_layout.addWidget(add_note, alignment = Qt.AlignTop)
        self.tool_layout.addStretch(0)
        self.tool_layout.addWidget(back_button, alignment=Qt.AlignBottom)


    def __add_main_buttons(self):
        """
            this functino will add main buttons like change, search to the main layout
        """
        self.__remove_widgets(self.tool_layout)
        change_button = QPushButton('Change')
        search_button = QPushButton('Search')
        exit_button = QPushButton('Exit')

        # trigger button to functions
        exit_button.clicked.connect(self.__exit)
        change_button.clicked.connect(self.__change)

        # tool_layout.setSpacing(0)
        # tool_layout.setContentsMargins(0,0,0,0)
        self.tool_layout.addWidget(change_button, alignment=Qt.AlignTop)
        self.tool_layout.addWidget(search_button, alignment=Qt.AlignTop)
        self.tool_layout.addStretch(0)
        self.tool_layout.addWidget(exit_button, alignment=Qt.AlignBottom)



    def __remove_widgets(self, layout):
        """
            this function is responsible to delete all widgets in one layout

            :param layout: layout that we want to delete widgets of it
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    
    def __add_node(self):
        node = self.scene.add_node('x', -150, -270)
        node.signals.click.connect(self.__node_section)
    
    def __node_section(self, node):
        print('node clicked, name of node is ', node.name)

