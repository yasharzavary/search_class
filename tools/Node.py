"""
Node.py - manage nodes of all node-structured systems like tree, graph and etc.
you can control the name of nodes, children of them and other.

author: yashar zavary rezaie
Email: zavaryyashar009@gmail.com
last update: April 2, 2025

I will appreciate for your suggestions about this class.
"""
from string import ascii_uppercase, ascii_lowercase, digits
from random import choice

# built-in Errors


# main class
class Node:
    def __init__(self, name: str = ''.join([choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(10)]),
                 child_list: list = None,
                 ):
        """
        Node class.

        Attributes:
            name(str): name of this node.
                default: one random name created by upper & lower case ascii and digits.
            child_list(list): list of child nodes created by this node.
                NOTE: they must be Node type.
                default: one empty list.


        :param name: name of Node.
        :param child_list: children of this Node.
        """

        self.__name = name           # this Node name that we can use in search.
        self.__children = list()     # empty child list.
        if child_list is not None:
            self.__children = child_list  # add children if it isn't None.


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

