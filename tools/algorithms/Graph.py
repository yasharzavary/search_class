"""
Graph.py - structure of graph.

author: yashar zavary rezaie
Email: zavaryyashar009@gmail.com
last update: April 2, 2025

I will appreciate for your suggestions about this class.
"""
from .Node import Node


# built-in errors.
class FalseSearchMode(Exception):
    def __init__(self, message):
        self.__mess = message

    def __str__(self):
        return self.__mess

# main class
class Graph:

    def __init__(self, start_node: Node, goal_nodes: [list, str]):
        """
            you can create graphs and use tools of it for explore your structure.
        :param start_node:
        :param goal_nodes:
        """

        # check inputs
        self.__control(start_node)
        self.__control(goal_nodes)

        self.__startRoot = start_node
        self.__goalRoot = [goal_nodes] if isinstance(goal_nodes, Node) else goal_nodes


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



    def DFS_search(self, mode: str = 'check'):
        """
            DFS search manager, use classic way for finding path and exist check of one node from your given graph
            Attributes:
                mode: if you want just checking one node, use this
                      if you want to get path for reach node, use this
                NOTICE: using path mode, increase space usage and slower speed...so if you need use it.
                DEFAULT: default value is check.
        :param mode: checking one node or finding path.
        :return:
        """
        if mode not in ['check', 'path']: raise FalseSearchMode('search mode must be path or check')
        frontier = [self.__startRoot]
        visited = list()
        if mode == 'path':
            way = list()
            while frontier:
                now = frontier.pop(0)
                if now == '!!':
                    way.pop()
                    continue
                elif now in visited: continue             # if we check this node before this, continue to next node
                for goal in self.__goalRoot:
                    if now == goal:
                        return f'Find, node: {now}' if mode == 'check' else ' -> '.join(
                            [node.name for node in way] + [goal.name]
                        ), now    # return result if find

                # add controling units.
                visited.append(now)
                way.append(now)
                frontier = now.children + ['!!'] + frontier
        else:
            while frontier:
                now = frontier.pop(0)
                if now in visited:
                    continue  # if we check this node before this, continue to next node
                elif now == self.__goalRoot:
                    return f'goal node find', now

                # add controling units.
                visited.append(now)
                frontier = now.children + frontier

        return 'goal node doesn\'t exist'

    def BFS_search(self, mode: str = 'check'):
        """
            BFS search manager, it can find you optimal path for reaching you goal or just checking one node.
                Attributes:
                - mode: if you want just checking one node, use this
                if you want to get path for reach node, use this
                NOTICE: using path mode, increase space usage and slower speed...so if you need use it.
                DEFAULT: default value is check.
        :param mode: checking one node or finding path.
        :return:
        """
        if mode not in ['check', 'path']: raise FalseSearchMode('search mode must be path')
        frontier = [self.__startRoot]
        visited = list()
        if mode == 'path':
            parents = dict()
            while frontier:
                now = frontier.pop(0)
                visited.append(now)
                if now in self.__goalRoot:
                    temp = now
                    path = [now.name]
                    while temp.name != '0':
                        temp = parents[temp]
                        path.insert(0, temp.name)
                    return f'node exist, path: {' -> '.join(path)}', now

                # analyze and add new children.
                for child in now.children:
                    if child not in visited:
                        frontier.append(child)
                        parents[child] = now
        else:
            while frontier:
                now = frontier.pop(0)
                visited.append(now)
                if now in self.__goalRoot:
                    return 'node exist', now

                # analyze and add new children.
                for child in now.children:
                    if child not in visited:
                        frontier.append(child)









