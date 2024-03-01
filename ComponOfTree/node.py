class Node:
    ''' Класс представления узла '''
    current_state: list = None
    ''' Начальное состояние'''
    parent_node: "Node" = None
    ''' Указатель на родительский узел'''
    previous_action: str = None
    ''' Действие, которое было применено к родительскому узлу для формирования данного узла'''
    path_cost: int = 0
    ''' Стоимость пути от начального состояния до данного узла g(n)'''
    depth: int = 0
    ''' Количество этапов пути от начального состояния (глубина)'''
    node_id: int = 0

    nodes_count = 0

    def __init__(self, state: list, parent: "Node", action: str, cost: int, depth: int):
        self.current_state = state
        self.parent_node = parent
        self.previous_action = action
        self.path_cost = cost
        self.depth = depth
        self.node_id = Node.nodes_count
        Node.nodes_count += 1

    @classmethod
    def get_nodes_count(cls) -> int:
        ''' Статический метод класса, возвращающий количество узлов '''
        return cls.nodes_count + 1