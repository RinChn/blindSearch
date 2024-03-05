from main import debug_flag
from node import Node
from time import process_time

from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_state, print_node, print_path, MOVES, get_initial_state


def dfs():
    """
    Поиск в глубину.
    """

    print("ПОИСК В ГЛУБИНУ DFS - Deep-First Search.")

    start_node = Node(get_initial_state(), None, None, 0, 0)  # Начальный узел
    visited_states = set()  # Множество для хранения посещенных состояний
    stack = [start_node]  # Стек для хранения узлов, которые нужно посетить
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций

    START_TIME = process_time()

    while stack:
        current_node = stack.pop()
        iterations += 1

        # Проверяем, достигнуто ли конечное состояние
        if check_final(current_node.current_state):
            result_node = current_node
            break

        # Преобразуем состояние в хэш-таблицу, проверяем, было ли оно посещено ранее
        state_hash_value = state_hash(current_node.current_state)
        if state_hash_value in visited_states:
            continue

        visited_states.add(state_hash_value)
        new_states_dict = get_followers(current_node.current_state)

        # Отладочный вывод текущего узла и его потомков
        if debug_flag:
            print(f"----------------Шаг: {iterations}.---------------- \n")
            print("Текущий узел:", end=' ')
            if iterations == 1:
                print("Корень дерева")
            print_node(current_node)
            print("Потомки:")
            for child_action, child_state in new_states_dict.items():
                child_hash_value = state_hash(child_state)
                if child_hash_value not in visited_states:
                    # Создаем новый узел для каждого дочернего состояния
                    child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1,
                                      current_node.depth + 1)
                    print_node(child_node)  # Вывод информации о новом узле
                    stack.append(child_node)  # Добавление нового узла в стек для дальнейшего исследования
                else:
                    # Выводим сообщение о повторном состоянии
                    print("Повторное состояние:")
                    print(f"Action = {MOVES.keys()[MOVES.values().index(child_action)] }, "
                          f"\nDepth = {current_node.depth + 1}, " +
                          f"Cost = {current_node.path_cost + 1}, \nState: ")
                    print_state(child_state)

            input("Нажмите 'Enter' для продолжения...")
        else:
            # Добавление всех потомков текущего узла в стек
            stack.extend(
                Node(child_state, current_node, child_action, current_node.path_cost + 1, current_node.depth + 1)
                for child_action, child_state in new_states_dict.items()
                if state_hash(child_state) not in visited_states
            )

    # Проверяем, было ли найдено конечное состояние
    if result_node is not None:
        print("\n---Конечное состояние достигнуто!---")
        print_path(result_node)  # Выводим путь к достижению конечного состояния
        TIME_STOP = process_time()
        print_info(iterations=iterations, time=TIME_STOP - START_TIME, visited_states=len(visited_states),
                   path_cost=result_node.path_cost)
    else:
        print("\nПуть к конечному состоянию не найден.")

    # Проверяем, было ли найдено хотя бы одно состояние
    if not visited_states:
        print("\nВсе состояния были исследованы, но решение не было найдено.")
