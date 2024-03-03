import os
import psutil

from node import Node


MOVES = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

ACTIONS_MAP = {
        (0, 1): "right",
        (0, -1): "left",
        (-1, 0): "up",
        (1, 0): "down"
}


def get_initial_state() -> list:
    """
    Получение начального состояния.
    :return: Начальное состояние.
    """
    return [
        [5, 6, 4],
        [2, 3, 8],
        [7, 1, 0]
    ]


def get_finish_state() -> list:
    """
    Получение конечного состояния.
    :return: Конечное состояние.
    """
    return [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]


def print_path(node: "Node", isReversed=False):
    """
    Вывод полного пути от начального до конечного состояния в консоль.
    :param node: Конечный узел выводимого пути.
    :param isReversed: Флаг, необходимо ли выводить в обратную сторону.
    """
    path = []
    current_node = node

    while current_node.parent_node:
        path.append(current_node)
        current_node = current_node.parent_node
    path.append(current_node)

    if isReversed:
        path = path[::-1]

    for path_node in path:
        print_node(path_node)
        print("^\n:\n:\n_\n")


def print_node(node: "Node"):
    """
    Вывод информации об узле на экран.
    :param node: Узел, информация о котором выводится.
    """
    parent_id = 0
    if node.parent_node:
        parent_id = node.parent_node.node_id
    node_prev_action = None

    if node.previous_action:
        node_prev_action = ACTIONS_MAP[node.previous_action]
    print(f"ID = {node.node_id}, ParentID = {parent_id}, " +
          f"Action = {node_prev_action}, \nDepth = {node.depth}, " +
          f"Cost = {node.path_cost}, \nState: ")
    print_state(node.current_state)
    print("")


def print_state(state: list):
    """
    Вывод состояния матрицей.
    :param state: Двумерный список-состояние.
    """
    for row in state:
        print(" ".join(str(cell) if cell != 0 else " " for cell in row))


def check_final(current_state: list) -> bool:
    """
    Проверка состояния на то, является ли оно конечным.
    :param current_state: проверяемое состояние.
    :return: True, если состояние конечное; False иначе.
    """
    return current_state == get_finish_state()


def state_swap(descendant: dict, current_state: list, move: tuple, pos_i: int, pos_j: int):
    """
    Перемещение ячейки
    :param descendant: словарь наследников
    :param current_state: состояние-родитель
    :param move: передвижение, совершаемое "пустой ячейкой"
    :param pos_i: Координата пустой ячейки по оси Y
    :param pos_j: Координата пустой ячейки по оси X
    """
    new_state = [row[:] for row in current_state]
    new_pos_i = pos_i + move[0]
    new_pos_j = pos_j + move[1]

    if 0 <= new_pos_i <= 2 and 0 <= new_pos_j <= 2:
        new_state[pos_i][pos_j], new_state[new_pos_i][new_pos_j] = new_state[new_pos_i][new_pos_j], \
                                                                   new_state[pos_i][pos_j]
        descendant[move] = new_state


def get_empty_cell(state: list):
    """
    Получение координат пустой ячейки
    :param state: Состояние для поиска
    :return: Координаты пустой ячейки
    """
    pos_i, pos_j = None, None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                pos_i, pos_j = i, j
                break
    return pos_i, pos_j


def get_followers(current_state: list) -> dict[tuple, list[Node]]:
    """
    Функция последователей.
    :param current_state: состояние, последователей которого необходимо получить.
    :return: Последователи.
    """
    new_states = {}
    pos_i, pos_j = get_empty_cell(current_state)
    for action, move in MOVES.items():
        state_swap(new_states, current_state, move, pos_i, pos_j)
    return new_states


def print_info(iterations: int, time: float, visited_states: int, path_cost: int):
    """

    :param iterations:
    :param time:
    :param visited_states:
    :param path_cost:
    :return:
    """
    print(f"\nКоличество УЗЛОВ в дереве: {Node.get_nodes_count()}")
    print(f"Количество ИТЕРАЦИЙ в поиске: {iterations}")
    print(f"Количество пройденных СОСТОЯНИЙ: {visited_states}")
    print(f"Затраченное ВРЕМЯ: {time * 1000} мс")
    print(f"Затраченная ПАМЯТЬ: {psutil.Process(os.getpid()).memory_info().rss} байт")
    print(f"СТОИМОСТЬ найденного пути: {path_cost}")


def state_hash(state: list) -> int:
    """
    Хэширование состояния.
    :param state: Состояние.
    :return: Хэш-таблица состояния.
    """
    return hash(tuple(map(tuple, state)))
