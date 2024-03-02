from time import process_time

from ComponOfTree.node import Node
from ComponOfTree.tree import get_initial_state
from basic_operations import print_info, check_final, state_hash, get_followers


def dls(depth_limit: int):
    """
    Ограниченный поиск в глубину.
    :param depth_limit: Ограничение на глубину.
    """
    start_node = Node(get_initial_state(), None, None, 0, 0)
    visited_states = set()  # Множество посещенных состояний
    START_TIME = process_time()
    result_node, iterations = dls_iteration(start_node, depth_limit, visited_states, iteration_count=1)

    if result_node is not None:
        print("Решение найдено!")
        TIME_STOP = process_time()
        print_info(iterations=iterations, time=TIME_STOP - START_TIME)
    else:
        print("Решение не найдено.")


def dls_iteration(node: Node, depth_limit: int, visited_states: set, iteration_count: int):
    """
    Итерация ограниченного поиска в глубину.
    :param node: Текущий узел дерева решения.
    :param depth_limit: Ограничение для поиска.
    :param visited_states: Множество посещённых состояний.
    :param iteration_count: Количество прошедших операций на момент вызова функции.
    :return: Узел конечного состояния и количество операций.
    """
    # Проверка на то, достигнуто ли ограничение.
    if node.depth > depth_limit:
        return None, iteration_count

    # Проверка на то, хранится ли в текущем узле финальное состояние
    if check_final(node.current_state):
        return node, iteration_count

    # Проверка, является ли состояние посещённым
    state_hash_value = state_hash(node.current_state)
    if state_hash_value in visited_states:
        return None, iteration_count

    visited_states.add(state_hash_value)  # Добавление текущего состояния в множество посещенных состояний

    # Получение последователей и создание узлов для последователей
    followers = get_followers(node.current_state)
    for action, state in followers.items():
        node_child = Node(state, node, action, node.path_cost + 1, node.depth + 1)
        result, iteration_count = dls_iteration(node_child, depth_limit, visited_states, iteration_count + 1)
        # Для поиска последующих потомков.
        if result is not None:
            return result, iteration_count

    return None, iteration_count + 1  # Не удалось найти решение
