import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout,
                                QVBoxLayout, QWidget, QLineEdit, QPushButton, QCheckBox,
                               QLabel, QScrollArea, QComboBox, QProgressBar, QFileDialog)

from .graphs import *
from tools.algorithms.Node import Node
from tools.algorithms.Graph import Graph
from tools.UI.file_protocol import File

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
        self.node_number = 0

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
        save_button = QPushButton('Save')
        exit_button = QPushButton('Exit')

        # trigger button to functions
        save_button.clicked.connect(self.save_file)
        exit_button.clicked.connect(self.__exit)
        change_button.clicked.connect(self.__change)
        search_button.clicked.connect(self.__search_controller)

        # tool_layout.setSpacing(0)
        # tool_layout.setContentsMargins(0,0,0,0)
        self.tool_layout.addWidget(change_button, alignment=Qt.AlignTop)
        self.tool_layout.addWidget(search_button, alignment=Qt.AlignTop)
        self.tool_layout.addStretch(0)
        self.tool_layout.addWidget(save_button, alignment=Qt.AlignBottom)
        self.tool_layout.addWidget(exit_button, alignment=Qt.AlignBottom)

    def __search_controller(self):
        """
            used for search with methods.
        :return:
        """
        self.__remove_widgets(self.tool_layout)
        self.algorithm_box = QComboBox()
        self.algorithm_box.addItem('DFS')
        self.algorithm_box.addItem('IDS')
        self.algorithm_box.addItem('BFS')
        self.algorithm_box.addItem('DLS')
        self.algorithm_box.addItem('bidirectional')

        # buttons definitions
        back_button = QPushButton('Back')
        search_button = QPushButton('start')


        # button connections
        back_button.clicked.connect(self.__add_main_buttons)
        search_button.clicked.connect(self.__search_start)


        self.tool_layout.addWidget(self.algorithm_box, alignment=Qt.AlignTop)
        self.tool_layout.addWidget(search_button, alignment=Qt.AlignTop)
        self.tool_layout.addStretch(0)
        self.tool_layout.addWidget(back_button, alignment=Qt.AlignBottom)

    def __graph_creation(self):
        # update progress bar settings.
        self.__remove_widgets(self.message_control_layout)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.node_number)  # From 0 to 100
        self.message_control_layout.addWidget(QLabel('Nodes collecting.'))
        self.message_control_layout.addWidget(self.progress_bar)

        # variables for my main loop
        front = [self.scene.root_node]
        visited = []
        self.progress_bar.setValue(0)
        child_map = dict()
        node_map = dict()
        goals = set()

        # find nodes
        while front:
            temp = front.pop()
            visited.append(temp)
            self.progress_bar.setValue(self.progress_bar.value() + 1)
            node_map[temp.name] = Node(temp.name)
            child_map[temp.name] = [i.name for i in temp.connected_nodes]
            front += [i for i in temp.connected_nodes if i not in visited]
            if temp == self.scene.root_node: start_node = temp.name
            elif temp in self.scene.goal_nodes: goals.add(temp.name)

        self.__remove_widgets(self.message_control_layout)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, self.node_number)  # From 0 to 100
        self.message_control_layout.addWidget(QLabel('Graph creating.'))
        self.message_control_layout.addWidget(self.progress_bar)
        self.progress_bar.setValue(0)

        for key, value in child_map.items():
            self.progress_bar.setValue(self.progress_bar.value() + 1)
            node_map[key].children = [node_map[i] for i in value]
            print(key, ' done!')

        return start_node, goals, node_map

    def __search_start(self):
        # TODO: start node not selected Error.
        # TODO: goal node not allocated Error.
        # TODO: graph doesn't exist error.

        start_node, goals, node_map = self.__graph_creation()

        start_node = node_map[start_node]
        goals = [node_map[i] for i in goals]

        self.__remove_widgets(self.message_control_layout)
        self.message_control_layout.addWidget(QLabel('Searching...'))


        agent = Graph(start_node=start_node, goal_nodes=goals)



        if self.algorithm_box.currentIndex() == 0:
            result = agent.DFS_search()
        elif self.algorithm_box.currentIndex() == 1:
            result = agent.DFS_search(algorithm='IDS')
        elif self.algorithm_box.currentIndex() == 2:
            result = agent.BFS_search()
        elif self.algorithm_box.currentIndex() == 3:
            result = agent.DFS_search(algorithm='DLS', deth_limit=0)
        elif self.algorithm_box.currentIndex() == 4:
            result = agent.bidirectional_search()

        path = list(result[0].split(' -> '))
        if path:
            self.scene.search_edge_color_change(path)
        else:
            self.__remove_widgets(self.message_control_layout)
            self.message_control_layout.addWidget(QLabel('Path from root to goals not founded.'))


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
        self.node_number += 1
        node.signals.click.connect(self.__node_section)              # connect node mouse event
        node.doubleSignals.click.connect(self.delete_node_from_scene)
        # delete message section and add default label.
        self.__remove_widgets(self.message_control_layout, [QLabel('messages will apeear here')])

    def delete_node_from_scene(self, node):
        self.scene.delete_node(node.name)
        self.__add_main_buttons()

    def __node_section(self, node):
        """
            control nodes
        :param node: user's selected node
        :return:
        """
        # if before this, one node selected, we do connection rules.
        if self.edge_mode:
            if self.source_node == node: return
            if node in self.source_node.connected_nodes:
                self.scene.delete_edge(self.source_node, node)
            else:
                self.scene.add_edges_from_list(self.source_node, [node])
            self.__add_connected_nodes_labels(self.source_node)
        # main node selection section
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
        """
            apply changes of graph and show on scene.
        :return:
        """
        # check root and goal check box for changing the graph's detais.
        if self.root_node.isChecked() and self.source_node != self.scene.root_node:
            self.scene.set_root_node(self.source_node)
        elif not self.root_node.isChecked() and self.source_node == self.scene.root_node:
            self.scene.delete_root_node()
        if self.goal_node.isChecked() and self.source_node not in self.scene.goal_nodes:
            self.scene.add_goal_node(self.source_node)
        elif not self.goal_node.isChecked() and self.source_node  in self.scene.goal_nodes:
            self.scene.delete_goal_node(self.source_node)

        # change name of node.
        candidate_name = self.node_name_input.text().strip()
        if candidate_name != self.source_node.name:
            self.scene.change_name(self.source_node, candidate_name)


    def __add_connected_nodes_labels(self, node: GraphNode):
        """
            added user's connection candidates if it possible
            or delete the connection.
        :param node:
        :return:
        """
        # add connection labels to the edge section of one node.
        self.__remove_widgets(self.label_layout)
        self.edge_mode = True
        connection_names = [connected_node.name for connected_node in node.connected_nodes]
        for name in connection_names:
            temp_name_label = QLabel(name)
            self.label_layout.addWidget(temp_name_label)

    def __add_edge(self):
        """
            add edge name to node's edge show part.
        :return:
        """

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

    def save_file(self):
        start_node, goals, node_map = self.__graph_creation()
        # Create file dialog
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save Graph")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)  # Save mode
        file_dialog.setFileMode(QFileDialog.AnyFile)

        # Set default filename and filter
        file_dialog.selectFile("test.json")  # Default filename
        file_dialog.setNameFilter("Text Files (*.json);;All Files (*)")

        # Execute dialog
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]

                # Here you would actually save your file
                try:
                    File.save(node_map[start_node], [node_map[i] for i in goals], file_path)
                except Exception as e:
                    print(e)