"""
Node.py - manage nodes of all node-structured systems like tree, graph and etc.
you can control the name of nodes, children of them and other.

author: yashar zavary rezaie
Email: zavaryyashar009@gmail.com
last update: April 2, 2025

I will appreciate for your suggestions about this class.
"""

import warnings

# built-in Errors

class childPriceLenghtLen(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

# main class
class Node:
    node_number = 0
    def __init__(self, name: str = None,
                 child_list: list = None,
                 price_list: list = None,
                 info: dict = None,
                 ):
        """
        Node class.

        Attributes:
            name(str): name of this node.
                default: one random name created by upper & lower case ascii and digits.
                WARNING: I suggest to add one name because tree class will detect same names and it can raise error.
            child_list(list): list of child nodes created by this node.
                NOTE: they must be Node type.
                default: one empty list.



        :param name: name of Node.
        :param child_list: children of this Node.
        """
        if name is None:
            name = f'Node{Node.node_number}'
            Node.node_number += 1
        self.__name = name           # this Node name that we can use in search.
        self.__children = list()
        self.__price_list = list()
        if child_list is not None:
            self.__children = child_list  # add children if it isn't None.
        if price_list is not None:
            # if two list doesn't have same length, raise error.
            if len(price_list) != len(child_list): raise childPriceLenghtLen('child and price list must have same length')
            self.__price_list = price_list
        else:
            self.__price_list = [1 for _ in range(len(child_list))]  # set default cost 1

        # create info dict for Node.
        if info is not None and not isinstance(info, dict): raise TypeError('info must be a dict')
        self.__info = info if info is not None else dict()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, children):
        for child in children:
            if not isinstance(child, Node):             # if one child no Node type, raise error.
                raise TypeError(f'child of one Node must be a Node({child})')
            self.__children.append(child)

