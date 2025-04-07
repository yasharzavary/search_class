from PySide6.QtWidgets import (
QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QPen, QColor




class GraphNode(QGraphicsEllipseItem):
    def __init__(self, id, x, y, radius=30):
        """
            used for adding nodes.
        :param id: id of node for detect unique parts
        :param x: x coordinate of node
        :param y: y coordinate of node
        :param radius: radius of node
        """
        super().__init__(-radius / 2, -radius / 2, radius, radius)

        self.id = id
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
        for line in self.connections:
            scene.removeItem(line)
        scene.removeItem(self)


class GraphEdge(QGraphicsLineItem):
    def __init__(self, node1, node2):
        super().__init__()

        self.node1 = node1
        self.node2 = node2
        self.setPen(QPen(Qt.darkGray, 2))

        # connect two node.
        self.update_position()

    def update_position(self):
        # connect center of two node.
        p1 = self.node1.scenePos()
        p2 = self.node2.scenePos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
