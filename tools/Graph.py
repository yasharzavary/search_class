"""
Graph.py - structure of graph.

author: yashar zavary rezaie
Email: zavaryyashar009@gmail.com
last update: April 2, 2025

I will appreciate for your suggestions about this class.
"""
from Node import Node


# built-in errors.


# main class
class Graph:
    have_start = False
    have_end = False

    def __init__(self, root_node: [str, Node] = None,
                 start: bool = False,
                 end: bool = False):
        # control root node details.
        if isinstance(root_node, str):
            if root_node is None:
                self.__root = Node()
            else:
                self.__root = Node(root_node)
        elif isinstance(root_node, Node):
            self.__root = root_node
        else:
            raise TypeError(f'node should be {type(Node)} or string -name- type')     # if it isn't node type, raise.

        # graph start and end control info.
        self.__graph_start = True
        if start:
            self.have_start = True
            self.__graph_start = True

        self.__graph_end = True
        if end:
            self.have_end = True
            self.__graph_end = True









