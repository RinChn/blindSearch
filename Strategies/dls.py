from time import process_time
from basic_operations import START_TIME

from ComponOfTree.node import Node
from ComponOfTree.tree import get_initial_state
from basic_operations import print_info, check_final, state_hash, get_new_states


def dls(depth_limit: int):
    ''' Поиск в глубину с ограничением глубины '''
    start_node = Node(get_initial_state(), None, None, 0, 0)
    visited_states = set()  # Множество посещенных состояний
    START_TIME = process_time()
    result_node, iterations = dls_with_limit(start_node, depth_limit, visited_states, iteration_count=1)

    if result_node is not None:
        print("Решение найдено!")
        #TREE.print_path(result_node)
        TIME_STOP = process_time()
        print_info(iterations=iterations, time=TIME_STOP - START_TIME)
    else:
        print("Решение не найдено.")


def dls_with_limit(node: Node, depth_limit: int, visited_states: set, iteration_count: int):
    ''' Рекурсивная функция поиска в глубину с ограничением глубины и проверкой повторяющихся состояний '''
    if node.depth > depth_limit:
        return None, iteration_count  # Если достигнут лимит глубины, прекратить поиск
    if check_final(node.current_state):
        return node, iteration_count  # Если достигнуто конечное состояние, вернуть узел

    state_hash_value = state_hash(node.current_state)
    if state_hash_value in visited_states:
        return None, iteration_count  # Если состояние уже посещено, прекратить поиск

    visited_states.add(state_hash_value)  # Добавить текущее состояние в множество посещенных состояний

    new_states_dict = get_new_states(node.current_state)
    for new_action in new_states_dict:
        new_state = new_states_dict[new_action]
        new_node = Node(new_state, node, new_action, node.path_cost + 1, node.depth + 1)
        result, iteration_count = dls_with_limit(new_node, depth_limit, visited_states, iteration_count + 1)
        if result is not None:
            return result, iteration_count

    return None, iteration_count + 1  # Если не удалось найти решение в данной ветви, вернуть None
