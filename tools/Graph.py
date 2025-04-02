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

    def __init__(self, start_node: Node, goal_nodes: list):
        self.__control(start_node)
        self.__control(goal_nodes)

        self.__startRoot = start_node
        self.__goalRoot = goal_nodes


    def __control(self, nodes: [Node, list]):
        if isinstance(nodes, list):
            for node in nodes:
                if not isinstance(node, Node): raise TypeError(f'Nodes must be {type(Node)}, {node} is not!')
        elif not isinstance(nodes, Node):
            raise TypeError(f'Nodes must be {type(Node)}, {nodes} is not!')
        else:
            raise TypeError(f'Nodes must be {type(Node)}.')








