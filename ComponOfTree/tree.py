from ComponOfTree.node import Node


class Tree:
    ''' Класс представления дерева '''
    # Все его методы - статические, т.к. дерево - единственное
    __nodes = None
    '''Все узлы'''

    # Mapping actions to their corresponding words
    ACTIONS_MAP = {
        (0, 1): "right",
        (0, -1): "left",
        (-1, 0): "up",
        (1, 0): "down"
    }

    def __init__(self):
        self.__nodes = {0: [Node(get_initial_state(), None, None, 0, 0)]}

    def add_node(self, level: int, new_node: "Node"):
        ''' Добавить узел в дерево '''
        if level not in self.__nodes:
            self.__nodes[level] = [new_node]
        else:
            self.__nodes[level].append(new_node)

    def getNode(self, node: int) -> list["Node"]:
        '''Получить список узлов по глубине'''
        return list(self.__nodes[node])

    def print_node(self, node: "Node"):
        ''' Вывод узла на экран '''
        parent_id: int = 0
        if(node.parent_node):
            parent_id = node.parent_node.node_id
        node_prev_action: str = None
        if (node.previous_action):
            node_prev_action = self.ACTIONS_MAP[node.previous_action]
        print(f"id = {node.node_id}, parent_id = {parent_id}, " +
            f"action = {node_prev_action}, \ndepth = {node.depth}, " +
            f"cost = {node.path_cost}, state: ")
        self.print_state(node.current_state)
        print("")

    def print_state(self, state: list):
        ''' Вывод состояния в три ряда'''
        for row in state:
            print(" ".join(str(cell) if cell != 0 else " " for cell in row))

    def print_path(self, node: "Node", isReversed=False):
        ''' Вывод пути на экран '''
        path = []
        current_node = node

        while current_node.parent_node:
            path.append(current_node)
            current_node = current_node.parent_node
        path.append(current_node)
        if isReversed:
            path = path[::-1]
        for path_node in path:
            self.print_node(path_node)
            print("\t^\n\t|\n")


def get_initial_state() -> list:
    ''' Получение начального состояния игры (Вариант 7) '''
    return [
    [5, 6, 4],
    [2, 3, 8],
    [7, 1, 0]
    ]


def get_finish_state() -> list:
    ''' Получение конечного состояния игры (Вариант 7) '''
    return [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]