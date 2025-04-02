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
    def __init__(self, node: [str, Node] = None):
        if isinstance(node, str):
            if node is None:
                self.__root = Node()
            else:
                self.__root = Node(node)
        elif isinstance(node, Node):
            self.__root = node
        else:
            raise TypeError(f'node should be {Node} or string -name- type')






