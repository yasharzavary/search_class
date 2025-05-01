from tools.algorithms.Node import Node
import json
import random
from string import ascii_lowercase


class File:
    def __init__(self):
        pass

    @staticmethod
    def save(start_node: Node, goals, file_path=None):
        node_list = list()
        connection_dict = dict()
        fronteir = [start_node]
        while fronteir:
            node = fronteir.pop()
            fronteir += node.children
            node_list.append(node.name)
            connection_dict[node.name] = list()
            for child in node.children:
                connection_dict[node.name].append(child.name)

        final = {
            'nodes': node_list,
            'connections': connection_dict,
            'start_node': start_node,
            'goals': goals
        }
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(final, file, indent=4)
            print(file_path)
            print('done!')
        else:
            with open(f'{''.join([random.choice(ascii_lowercase) for _ in range(10)])}.json', 'w') as file:
                json.dump(final, file, indent=4)

