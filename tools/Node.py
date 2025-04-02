from string import ascii_uppercase, ascii_lowercase, digits
from random import choice

# built-in Errors



# main class
class Node:
    def __init__(self, name: str = ''.join([choice(ascii_uppercase + ascii_lowercase + digits) for _ in range(10)]),
                 child_list: list = None,
                 Goal: bool = False,
                 start: bool = False):

        self.__name = name           # this Node name that we can use in search.
        self.__children = list()     # empty child list.
        if child_list is not None:
            pass  # add children if it isn't None.

        # what is bool detail of this node.
        self.__goal = Goal
        self.__start = start

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

    @property
    def goal(self):
        return self.__goal

    @goal.setter
    def goal(self, goal):
        self.__goal = goal

    @property
    def start(self):
        return self.__start


    @start.setter
    def start(self, start):
        self.__start = start

