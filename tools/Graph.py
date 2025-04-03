"""
Graph.py - structure of graph.

author: yashar zavary rezaie
Email: zavaryyashar009@gmail.com
last update: April 2, 2025

I will appreciate for your suggestions about this class.
"""
from Node import Node


# built-in errors.
class FalseSearchMode(Exception):
    def __init__(self, message):
        self.__mess = message

    def __str__(self):
        return self.__mess

# main class
class Graph:

    def __init__(self, start_node: Node, goal_nodes: list):
        """
            you can create graphs and use tools of it for explore your structure.
        :param start_node:
        :param goal_nodes:
        """
        # check inputs
        self.__control(start_node)
        self.__control(goal_nodes)

        self.__startRoot = start_node
        self.__goalRoot = goal_nodes


    def __control(self, nodes: [Node, list]):
        """
            control start and goal nodes for possible value errors.
        :param nodes: a list of node or one node that user give to the class.ß
        :return:
        """
        # check depend on different type of inputs.
        if isinstance(nodes, list):
            for node in nodes:
                if not isinstance(node, Node): raise TypeError(f'Nodes must be {type(Node)}, {node} is not!')
        elif not isinstance(nodes, Node):
            raise TypeError(f'Nodes must be {type(Node)}, {nodes} is not!')
        else:
            raise TypeError(f'Nodes must be {type(Node)}.')


    def DFS_search(self, mode: str = 'check'):
        if mode not in ['check', 'way']: raise FalseSearchMode('search mode must be way or check')
        frontier = [self.__startRoot]
        visited = list()
        way = list()
        while frontier:
            now = frontier.pop(0)
            if now == '!!':
                way.pop()
                continue
            elif now in visited: continue             # if we check this node before this, continue to next node
            elif now == self.__goalRoot:
                return f'Find, node: {now}' if mode == 'check' else ' -> '.join(way)     # return result if find

            # add controling units.
            visited.append(now)
            way.append(now)
            frontier = now.children + ['!!'] + frontier













