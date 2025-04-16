"""
Graph.py - structure of graph.

author: yashar zavary rezaie
Email: zavaryyashar009@gmail.com
last update: April 2, 2025

I will appreciate for your suggestions about this class.
"""
from .Node import Node
import threading

# built-in errors.


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


    @property
    def start_node(self):
        return self.__startRoot

    @property
    def goal_node(self):
        return self.__goalRoot


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

    def DFS_search(self, algorithm: str = 'DFS', deth_limit = -1):
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
        if algorithm not in ['DFS', 'IDS', 'DLS']: pass    # TODO: FalseAlgorithmChoice error for this part.
        if algorithm =='DLS' and deth_limit == -1: pass # TODO: DethLimitNotAssociated error for this part.
        # some info we need for searching.
        loop = True
        d_limit = 0 if algorithm == 'IDS' else deth_limit
        while loop:
            way = list()
            visited = list()
            frontier = [self.__startRoot]
            loop = False
            depth = 0
            end = True
            while frontier:
                now = frontier.pop(0)
                if now == '!!':
                    way.pop()
                    depth -= 1
                    continue
                elif now in visited: continue             # if we check this node before this, continue to next node
                if algorithm in ['DLS', 'IDS'] and depth > d_limit:
                    end = False
                    continue
                depth += 1
                for goal in self.__goalRoot:
                    if now == goal:
                        return ' -> '.join(
                            [node.name for node in way] + [goal.name]
                        ), now, [node.name for node in way]    # return result if find
                # add controling units.
                visited.append(now)
                way.append(now)
                frontier = now.children + ['!!'] + frontier                     # add child to the front
            if not end and algorithm == 'IDS':
                loop = True
                d_limit += 1
        return None, 'goal node doesn\'t exist'

    def BFS_search(self):
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
        frontier = [self.__startRoot]
        visited = list()
        parents = dict()
        while frontier:
            now = frontier.pop(0)
            visited.append(now)
            if now in self.__goalRoot:
                temp = now
                path = [now.name]
                while temp.name != self.__startRoot.name:
                    temp = parents[temp]
                    path.insert(0, temp.name)
                return ' -> '.join(path), now, path

            # analyze and add new children.
            for child in now.children:
                if child not in visited and child not in frontier:
                    frontier.append(child)
                    parents[child] = now


        return None, 'goal node doesn\'t exist'

    def bidirectional_search(self):
        """
            Implement bidirectional search using threading with BFS from start and DFS from goal
        Returns:
            tuple: (path, meeting_node, path_list) if found
            tuple: (None, error_message) if not found
        """

        if len(self.__goalRoot) != 1:
            pass
            # TODO: GaolShouldBeOneNode error for this part.

        # some memory for thread talk
        shared_frontier = {'start_side': set(), 'goal_side': set()}
        shared_visited = {'start_side': set(), 'goal_side': set()}
        shared_parents = {'start_side': {}, 'goal_side': {}}
        meeting_node = [None]
        lock = threading.Lock()
        event = threading.Event()               # when one thread find one shared node, event trigger.

        # agent for second chaeck.
        DFS_agent = Graph(start_node=self.__goalRoot[0], goal_nodes=[self.__startRoot])

        def bfs_from_start():
            """
                BFS thread function for run BFS search.
            :return:
            """
            frontier = [self.__startRoot]
            visited = set()
            parents = {}

            while frontier and not event.is_set():
                now = frontier.pop(0)
                visited.add(now)

                # Check if this node was visited by the other thread
                with lock:
                    if now in shared_visited['goal_side']:
                        meeting_node[0] = now
                        event.set()      # we find, search done.
                        break
                    # add to shared one for another thread.
                    shared_visited['start_side'].add(now)
                    shared_frontier['start_side'].add(now)

                # Explore children
                for child in now.children:
                    if child not in visited and child not in frontier:
                        frontier.append(child)
                        parents[child] = now
                        with lock:
                            shared_parents['start_side'][child] = now

        def dfs_from_goal():
            """
                DFS search function for run DFS search.
            :return:
            """
            frontier = [DFS_agent.start_node]
            visited = set()
            parents = {}

            while frontier and not event.is_set():
                now = frontier.pop(0)
                visited.add(now)

                # Check if this node was visited by the other thread
                with lock:
                    if now in shared_visited['start_side']:
                        meeting_node[0] = now
                        event.set()
                        break
                    shared_visited['goal_side'].add(now)
                    shared_frontier['goal_side'].add(now)

                # Explore children (DFS)
                new_nodes = []
                for child in now.children:
                    if child not in visited and child not in frontier:
                        new_nodes.append(child)
                        parents[child] = now
                        with lock:
                            shared_parents['goal_side'][child] = now
                frontier = new_nodes + frontier

        # Create and start threads
        start_thread = threading.Thread(target=bfs_from_start)
        goal_thread = threading.Thread(target=dfs_from_goal)

        start_thread.start()
        goal_thread.start()

        # Wait for threads to complete
        start_thread.join()
        goal_thread.join()

        # Check if we found a meeting point
        if meeting_node[0] is None:
            return None, "No path exists between start and goal"

        # Reconstruct the path
        path = []
        # Build path from start to meeting node
        node = meeting_node[0]
        while node != self.__startRoot:
            path.insert(0, node.name)
            node = shared_parents['start_side'].get(node)

        path.insert(0, self.__startRoot.name)

        # Build path from meeting node to goal
        node = meeting_node[0]
        reverse_path = []
        while node != DFS_agent.start_node:
            reverse_path.append(node.name)
            node = shared_parents['goal_side'].get(node, None)
            if node is None:  # Shouldn't happen if search was successful
                break

        reverse_path.append(DFS_agent.start_node.name)

        full_path = path + reverse_path[1:]  # Skip duplicate meeting node

        return ' -> '.join(full_path), meeting_node[0], full_path

