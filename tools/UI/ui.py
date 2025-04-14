import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                                QVBoxLayout, QWidget, QLineEdit,
                                QPushButton, QLineEdit, QLabel, QCheckBox, QScrollArea)
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap

from .graphs import *


# TODO: message box in bottom of window.


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # information of page
        self.setWindowTitle("Graph")
        self.setGeometry(200, 100, 600, 700)
        cenral_widget = QWidget()
        self.setCentralWidget(cenral_widget)
        self.edge_mode = False
        self.source_node: [None, GraphNode] = None

        # main layout
        main_box = QVBoxLayout(cenral_widget)

        # temperory boxs
        main_layout = QHBoxLayout()
        self.message_control_layout = QHBoxLayout()

        main_box.addLayout(main_layout)
        main_box.addLayout(self.message_control_layout)

        # message control part
        self.message_control_layout.addWidget(QLabel('messages will appear here'))


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

        # button connections
        back_button.clicked.connect(self.__add_main_buttons)
        add_note.clicked.connect(self.__input_control)

        # adding to layout
        self.tool_layout.addWidget(add_note, alignment = Qt.AlignTop)
        self.tool_layout.addStretch(0)
        self.tool_layout.addWidget(back_button, alignment=Qt.AlignBottom)


    def __add_main_buttons(self):
        """
            this functino will add main buttons like change, search to the main layout
        """
        self.__remove_widgets(self.tool_layout)                 # remove widgets from too layout for adding new section
        # buttons for control main part.
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



    def __remove_widgets(self, layout, labels=[]):
        """
            this function is responsible to delete all widgets in one layout

            :param layout: layout that we want to delete widgets of it
        """
        # delete all widgets from the layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # add labels to deleted layout
        for label in labels:
            layout.addWidget(label)

        # control edge mode
        self.edge_mode = False

    def __input_control(self):
        """
            new nodes name control
        :return:
        """
        # name input
        self.node_name_input = QLineEdit()
        self.node_name_input.setPlaceholderText('Node name')
        self.node_name_input.setMaxLength(3)

        # buttons
        add_btn = QPushButton('Add')

        # button connections
        add_btn.clicked.connect(self.__add_node)

        # remove widgets from message section
        self.__remove_widgets(self.message_control_layout)

        # add name input widgets
        self.message_control_layout.addWidget(self.node_name_input)
        self.message_control_layout.addWidget(add_btn)


    def __add_node(self):
        """
            add new node to graph scene
        :return:
        """
        name = self.node_name_input.text().strip()                   # read name from input
        node = self.scene.add_node(name, -150, -150)                 # create new node and add to scene
        node.signals.click.connect(self.__node_section)              # connect node mouse event
        # delete message section and add default label.
        self.__remove_widgets(self.message_control_layout, [QLabel('messages will apeear here')])
    
    def __node_section(self, node):
        """
            control nodes
        :param node: user's selected node
        :return:
        """
        if self.edge_mode:
            if self.source_node == node: return
            if node in self.source_node.connected_nodes:
                self.scene.delete_edge(self.source_node, node)
            else:
                self.scene.add_edges_from_list(self.source_node, [node])
            self.__add_connected_nodes_labels(self.source_node)
        else:
            self.source_node = node
            self.__remove_widgets(self.tool_layout)

            # input definition
            # node name
            self.node_name_input = QLineEdit(node.name)
            self.node_name_input.setPlaceholderText('Node name')
            self.node_name_input.setMaxLength(3)

            # check boxs
            self.root_node = QCheckBox("Root Node")
            if node == self.scene.root_node:
                self.root_node.setChecked(True)
            self.goal_node = QCheckBox("Goal Node")
            if node in self.scene.goal_nodes:
                self.goal_node.setChecked(True)

            # button definition
            self.change_btn = QPushButton('Apply changes')
            self.unselect_btn = QPushButton('Unselect')
            self.edge_control = QPushButton('Edge control')



            # actions
            self.unselect_btn.clicked.connect(self.__add_main_buttons)
            self.edge_control.clicked.connect(self.__add_edge)
            self.change_btn.clicked.connect(self.__apply_changes)

            # add to layout
            self.tool_layout.addWidget(self.node_name_input, alignment=Qt.AlignTop)
            self.tool_layout.addWidget(self.edge_control, alignment=Qt.AlignTop)
            self.tool_layout.addWidget(self.root_node, alignment=Qt.AlignTop)
            self.tool_layout.addWidget(self.goal_node, alignment=Qt.AlignTop)
            self.tool_layout.addStretch(0)
            self.tool_layout.addWidget(self.change_btn, alignment=Qt.AlignBottom)
            self.tool_layout.addWidget(self.unselect_btn, alignment=Qt.AlignBottom)


    def __apply_changes(self):
        if self.root_node.isChecked() and self.source_node != self.scene.root_node:
            self.scene.set_root_node(self.source_node)
        elif not self.root_node.isChecked() and self.source_node == self.scene.root_node:
            self.scene.delete_root_node()
        if self.goal_node.isChecked() and self.source_node not in self.scene.goal_nodes:
            self.scene.add_goal_node(self.source_node)
        elif not self.goal_node.isChecked() and self.source_node  in self.scene.goal_nodes:
            self.scene.delete_goal_node(self.source_node)


    def __add_connected_nodes_labels(self, node: GraphNode):
        self.__remove_widgets(self.label_layout)
        self.edge_mode = True
        connection_names = [connected_node.name for connected_node in node.connected_nodes]
        for name in connection_names:
            temp_name_label = QLabel(name)
            self.label_layout.addWidget(temp_name_label)

    def __add_edge(self):

        # labels
        definition_label = QLabel('connected Labels: ')

        # scroll area
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(100)


        # Container for labels
        self.label_container = QWidget()
        self.label_layout = QVBoxLayout(self.label_container)

        # add nodes to layout
        self.__add_connected_nodes_labels(self.source_node)

        # Configure scroll area
        scroll.setWidget(self.label_container)


        # button definitions
        back_btn = QPushButton('Back')

        # button connections
        back_btn.clicked.connect(self.__add_main_buttons)

        self.__remove_widgets(self.tool_layout)                 # delete all widgets from main layout of tools.

        self.edge_mode = True                                   # control edge mode for next time

        # add to layout
        self.tool_layout.addWidget(definition_label, alignment=Qt.AlignTop)
        self.tool_layout.addWidget(scroll, alignment=Qt.AlignTop)
        self.tool_layout.addStretch(0)
        self.tool_layout.addWidget(back_btn, alignment=Qt.AlignBottom)







