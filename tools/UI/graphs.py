from PySide6.QtWidgets import (
QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem,
 QGraphicsScene, QGraphicsView
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QBrush, QPen, QColor, QPainter

# Errors


# TODO: functions parameter definition.
# TODO: control x and y of circles depend on graph screen.
# TODO: graph without root and goal node error.
# TODO: one node repeat twice error.

class NodeSignal(QObject):
    click = Signal(object)

class DoubleClickNodeSignal(QObject):
    click = Signal(object)

class GraphNode(QGraphicsEllipseItem):
    def __init__(self, name, x, y, radius=30):
        """
            used for adding nodes.
        :param name: name of node for detect unique parts
        :param x: x coordinate of node
        :param y: y coordinate of node
        :param radius: radius of node
        """
        # TODO: postion control, the positions shouldn't go out from scene
        super().__init__(-radius / 2, -radius / 2, radius, radius)

        self.name = str(name)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor("skyblue")))
        self.setPen(QPen(Qt.black, 2))

        # change flags to able move and select of node.
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

        self.text = QGraphicsTextItem(self.name, self)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setPos(-10, -10)

        self.connections = []
        self.connected_nodes = []

        self.signals = NodeSignal()
        self.doubleSignals = DoubleClickNodeSignal()

    def change_name(self,  new_name):
        """
            changing name of node.
        :param new_name: new name that user want to set for one node.
        :return:
        """
        self.name = new_name
        self.text = QGraphicsTextItem(new_name, self)
        self.text.setDefaultTextColor(Qt.black)
        self.text.setPos(-10, -10)

    def delete(self, scene):
        """
            used for deleting one node,
                first it will delete connections(edges) and after that the node.
        :param scene:
        :return:
        """
        # delete connections of one node.
        for line in self.connections:
            scene.removeItem(line)
        scene.removeItem(self)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.signals.click.emit(self)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.doubleSignals.click.emit(self)



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


        # connect two node.
        self.update_position()

    def update_position(self, color=Qt.darkGray):
        """
            update position of two node.
        :return:
        """
        # connect center of two node.
        self.setPen(QPen(color, 2))
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

    def search_edge_color_change(self, path):
        """
            change color of path of search.
        :param node1:
        :param node2:
        :return:
        """
        node1 = self.root_node
        for i in range(len(path) - 1):
            node2 = path[i + 1]
            for edge in node1.connections:
                if edge.node1.name == node2:
                    next_node = edge.node1
                    edge.update_position(color=Qt.red)
                    break
                elif edge.node2.name == node2:
                    next_node = edge.node2
                    edge.update_position(color=Qt.red)
                    break
            node1 = next_node

    def delete_edge(self, node1, node2):
        """
            ues for removing nodes between two node
        :param node1:
        :param node2:
        :return:
        """
        # find edge(if exist) between two node.
        # delete connection between two edge list of nodes.
        for edge in node1.connections:
            if edge.node2 == node2 or edge.node1 == node2:
                temp_edge = edge                                      # save connection
                node1.connections.remove(edge)
                node1.connected_nodes.remove(node2)
        for edge in node2.connections:
            if edge.node1 == node1 or edge.node2 == node1:
                node2.connections.remove(edge)
                node2.connected_nodes.remove(node1)

        # delete from scene.
        self.removeItem(temp_edge)

    def change_name(self, node, new_name):
        """
            remove name and add new name for one node.
        :param node: node that will change name
        :param new_name: new name that user want for one node.
        :return:
        """
        self.removeItem(node.text)
        node.change_name(new_name)

    def add_node(self, name, x, y):
        """
            add new node
        :param name: name of node
        :param x: x position of node
        :param y: y position of node
        :return:
        """
        # if name doesn't exist, add default.
        if name is None:
            name = str(self.node_counter)
            self.node_counter += 1
        node = GraphNode(name, x, y)    # creat new node.
        # add to collections
        self.addItem(node)
        self.nodes[name] = node
        return node

    def add_edges_from_list(self, source, target_ids):
        """
            we can give one node and connections of it to this functions and this will connect them
        :param source_id: id of node that edges will go out from it.
        :param target_ids: ids of nodes that will have connection with our source node.
        :return:
        """
        if not isinstance(source, GraphNode):
            source = self.nodes.get(source)     # read source node.
        # TODO: error for node not finding.
        for tid in target_ids:
            if not isinstance(tid, GraphNode):
                target = self.nodes.get(tid)
            else:
                target = tid    
            # TODO: error for node not finding.
            if target:
                edge = GraphEdge(source, target)
                # add edges to list of both node
                source.connections.append(edge)
                target.connections.append(edge)
                # add ids to list of connections of both node.
                source.connected_nodes.append(tid)
                target.connected_nodes.append(source)
                self.addItem(edge)

    def delete_node(self, node_name):
        """
            used for delete one node from scene
        :param node_id: id of node that we want to delete.
        :return:
        """
        # check one node in the collections.
        node = self.nodes.get(node_name)
        if node:    # if node exist.
            node.delete(self)
            del self.nodes[node_name]
        else:
            pass  # TODO: error for node not finding.

    def set_root_node(self, node_name):
        """
            setting root node
        :param node_name: id that we want to change it to root.
        :return:
        """
        if self.root_node:  # if another node is root, change it.
            # TODO: warning for changing the node.
            self.root_node.setBrush(QBrush(QColor("skyblue")))
        # checks for type.
        if isinstance(node_name, GraphNode) and node_name not in list(self.nodes.keys()):
            pass
            # TODO: error handling
        elif isinstance(node_name, str) and node_name not in self.nodes:
            pass
            # TODO: error handling
        else:
            pass
            # TODO: error handling

        # if name given, check from collection
        if isinstance(node_name, str):
            self.root_node = self.nodes[node_name]
        else:
            self.root_node = node_name

        # change color of node to green for setting root.
        self.root_node.setBrush(QBrush(QColor("green")))

    def delete_root_node(self):
        """
            delete root node and backtrack color of it.
        :return:
        """
        # if root not exist, return
        if self.root_node is not None:
            self.root_node.setBrush(QBrush(QColor("skyblue")))        # change color.
            self.root_node = None

    def add_goal_node(self, node_name):
        """
            add new goal node.
        :param node_name: id that we want to change it to goal
        :return:
        """
        # type checking.
        if isinstance(node_name, GraphNode) and node_name not in list(self.nodes.keys()):
            pass
            # TODO: error handling
        elif isinstance(node_name, str) and node_name not in self.nodes:
            pass
            # TODO: error handling
        else:
            pass
            # TODO: error handling
        # if user give node name, read it from collection.
        temp = self.nodes[node_name] if isinstance(node_name, str) else node_name
        temp.setBrush(QBrush(QColor("red")))               # change color of goal to red.
        self.goal_nodes.append(temp)                       # append to node list
        # TODO: delete if not exist node happen

    def delete_goal_node(self, node_id):
        """
            delete one goal node if exist
        :param node_id:
        :return:
        """
        # errors
        if node_id not in self.nodes:
            pass
        # TODO: error for node not exist

        if node_id not in self.goal_nodes:
            pass  # TODO: node id not in goal node error

        temp = self.nodes.get(node_id) if isinstance(node_id, str) else node_id
        temp.setBrush(QBrush(QColor("skyblue")))            # backtrack color to sky blue
        self.goal_nodes.remove(temp)                        # remove from list

    def update_edges(self):
        """
            update when node change position
        :return:
        """
        # for each edge for each node, update edge
        for node in self.nodes.values():
            for edge in node.connections:
                edge.update_position()


class GraphView(QGraphicsView):
    def __init__(self, scene, weight=400, height=700):
        """
            chnage position of nodes and edges when nodes move
        :param scene: scene that you set for view.
        """
        super().__init__(scene)
        self.setFixedSize(weight, height)
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(-300, -300, 600, 600)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.scene().update_edges()