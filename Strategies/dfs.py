from ComponOfTree.node import Node
from ComponOfTree.tree import get_initial_state
from time import process_time

from basic_operations import print_info, check_final, state_hash, get_new_states


def dfs():
    ''' Поиск в глубину без ограничения глубины '''
    start_node = Node(get_initial_state(), None, None, 0, 0)
    visited_states = set()  # Множество посещенных состояний
    stack = [start_node]  # Стек для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций

    START_TIME = process_time()
    while stack:
        current_node = stack.pop()
        iterations += 1

        if check_final(current_node.current_state):
            result_node = current_node
            break

        state_hash_value = state_hash(current_node.current_state)
        if state_hash_value in visited_states:
            continue  # Пропускаем уже посещенные состояния

        visited_states.add(state_hash_value)  # Добавляем текущее состояние в множество посещенных состояний

        new_states_dict = get_new_states(current_node.current_state)

        for new_action in new_states_dict:
            new_state = new_states_dict[new_action]
            new_node = Node(new_state, current_node, new_action, current_node.path_cost + 1, current_node.depth + 1)
            stack.append(new_node)

    if result_node is not None:
        print("Решение найдено!")
        TIME_STOP = process_time()
        print_info(iterations=iterations, time=TIME_STOP - START_TIME)
    else:
        print("Решение не найдено.")

    # Выводим информацию о процессе поиска
    print("Процесс поиска:")
    print(f"Пройдено состояний: {len(visited_states)}")
    print(f"Итераций: {iterations}")
    print_info(iterations=iterations, time=TIME_STOP - START_TIME)

    # Проверяем, было ли найдено хотя бы одно состояние
    if not visited_states:
        print("Все состояния были исследованы, но решение не было найдено.")




