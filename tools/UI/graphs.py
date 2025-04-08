from PySide6.QtWidgets import (
QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsScene, QGraphicsView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPen, QColor, QPainter



# TODO: functions parameter definition
# TODO: control x and y of circles depend on graph screen

class GraphNode(QGraphicsEllipseItem):
    def __init__(self, name, x, y, radius=30):
        """
            used for adding nodes.
        :param id: id of node for detect unique parts
        :param x: x coordinate of node
        :param y: y coordinate of node
        :param radius: radius of node
        """
        # TODO: postion control, the positions shouldn't go out from scene
        super().__init__(-radius / 2, -radius / 2, radius, radius)

        self.name = name
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("skyblue")))
        self.setPen(QPen(Qt.black, 2))

        # change flags to able move and select of node.
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        self.text = QGraphicsTextItem(str(id), self)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setPos(-10, -10)

        self.connections = []
        self.connected_nodes = []

    def delete(self, scene):
        """
            used for deleting one node,
                first it will delete connections(edges) and after that the node.
        :param scene:
        :return:
        """
        for line in self.connections:
            scene.removeItem(line)
        scene.removeItem(self)


class GraphEdge(QGraphicsLineItem):
    def __init__(self, node1, node2):
        """
            graph edge control class
        :param node1: first node
        :param node2: second node
        """
        super().__init__()

        self.node1 = node1
        self.node2 = node2
        self.setPen(QPen(Qt.darkGray, 2))

        # connect two node.
        self.update_position()

    def update_position(self):
        """
            update position of two node.
        :return:
        """
        # connect center of two node.
        p1 = self.node1.scenePos()
        p2 = self.node2.scenePos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())


class GraphScene(QGraphicsScene):
    def __init__(self):
        """
            our nodes and edges set on this scene and this class can control them
        """
        super().__init__()
        self.nodes: dict = dict()             # store node_name:node for next usage
        self.node_counter: int = 0            # for nodes that don't have any name
        self.root_node: [GraphNode, None] = None
        self.goal_nodes: list = list()

    def add_node(self, name, x, y):
        """
            add new node
        :param name: name of node
        :param x: x position of node
        :param y: y position of node
        :return:
        """
        if name is None:
            name = str(self.node_counter)
            self.node_counter += 1
        node = GraphNode(name, x, y)    # creat new node.
        self.addItem(node)
        self.nodes[name] = node
        return node

    def add_edges_from_list(self, source_name, target_ids):
        """
            we can give one node and connections of it to this functions and this will connect them
        :param source_id: id of node that edges will go out from it.
        :param target_ids: ids of nodes that will have connection with our source node.
        :return:
        """
        source = self.nodes.get(source_name)     # read source node.
        # TODO: error for node not finding.
        for tid in target_ids:
            target = self.nodes.get(tid)
            # TODO: error for node not finding.
            if target:
                edge = GraphEdge(source, target)
                # add edges to list of both node
                source.connections.append(edge)
                target.connections.append(edge)
                # add ids to list of connections of both node.
                source.connected_nodes.append(tid)
                target.connected_nodes.append(source_name)
                self.addItem(edge)

    def delete_node(self, node_name):
        """
            used for delete one node from scene
        :param node_id: id of node that we want to delete.
        :return:
        """
        node = self.nodes.get(node_name)
        if node:
            node.delete(self)
            del self.nodes[node_name]
        else:
            pass  # TODO: error for node not finding.

    def set_root_node(self, node_name):
        """
            setting root node
        :param node_id: id that we want to change it to root.
        :return:
        """
        if node_name in self.nodes:
            if self.root_node:       # if another node is root, change it.
                # TODO: warning for changing the node.
                self.root_node.setBrush(QBrush(QColor("skyblue")))
            self.root_node = self.nodes[node_name]
            self.root_node.setBrush(QBrush(QColor("green")))
        # TODO: error for not exist node.

    def add_goal_node(self, node_name):
        """
            add new goal node.
        :param node_id: id that we want to change it to goal
        :return:
        """
        if node_name not in self.nodes:
            pass
        temp = self.nodes[node_name]
        temp.setBrush(QBrush(QColor("red")))
        self.goal_nodes.append(temp)
        # TODO: delete if not exist node happen

    def delete_goal_node(self, node_id):
        """
            delete one goal node if exist
        :param node_id:
        :return:
        """
        if node_id not in self.nodes:
            pass
        # TODO: error for node not exist

        if node_id not in self.goal_nodes:
            pass  # TODO: node id not in goal node error

        self.goal_nodes.remove(node_id)
        temp = self.nodes.get(node_id)
        temp.delete()


    def update_edges(self):
        """
            update when node change position
        :return:
        """
        for node in self.nodes.values():
            for edge in node.connections:
                edge.update_position()


class GraphView(QGraphicsView):
    def __init__(self, scene):
        """
            chnage position of nodes and edges when nodes move
        :param scene:
        """
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(-300, -300, 600, 600)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.scene().update_edges()