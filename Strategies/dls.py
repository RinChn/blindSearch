from time import process_time

from node import Node
from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_node, print_state, MOVES, \
    print_path, get_initial_state


def dls(depth_limit: int = None, DEBUG: bool = False):
    """
    Поиск с ограничением в глубину.
    :param depth_limit: ограничение
    :param DEBUG: флаг на поэтапный вывод.
    """
    # Выводим сообщение о начале алгоритма DLS
    print("ПОИСК В ГЛУБИНУ С ОГРАНИЧЕНИЕМ DLS - Deep-Limited Search.")
    start_node = Node(get_initial_state(), None, None, 0, 0)  # Начальный узел
    visited_states = set()  # Множество посещенных состояний
    stack = [start_node]  # Стек для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций

    START_TIME = process_time()
    # Основной цикл алгоритма
    while stack:
        current_node = stack.pop()  # Извлекаем текущий узел из стека
        iterations += 1  # Увеличиваем счетчик итераций на 1

        # Проверка на то, является ли состояние в узле финальным
        if check_final(current_node.current_state):
            result_node = current_node
            break

        # Преобразуем состояние в хэш-таблицу, проверяем, было ли оно посещено ранее
        state_hash_value = state_hash(current_node.current_state)
        if state_hash_value in visited_states:
            continue

        visited_states.add(state_hash_value)
        new_states_dict = get_followers(current_node.current_state)

        # Вывод информации о текущем узле и его потомках, если установлен режим отладки
        if DEBUG:
            print(f"----------------Шаг: {iterations}.---------------- \n")
            print("Текущий узел:", end=' ')
            if iterations == 1:
                print("Корень дерева")
            print_node(current_node)
            print("Потомки:")
            for child_action, child_state in new_states_dict.items():
                child_hash_value = state_hash(child_state)
                if child_hash_value not in visited_states:
                    # Создаем новый узел для потомка и добавляем его в стек
                    child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1,
                                      current_node.depth + 1)
                    print_node(child_node)
                    stack.append(child_node)  # Добавляем потомка в стек
                else:
                    # Если потомок уже был посещен, выводим информацию о нем
                    print("Повторное состояние:")
                    print(f"Action = {MOVES.keys()[MOVES.values().index(child_action)]}, \nDepth = {current_node.depth + 1}, " +
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

        # Если установлено ограничение глубины и текущая глубина превышает лимит, прекратить поиск
        if depth_limit is not None and current_node.depth >= depth_limit:
            print("\nДостигнуто ограничение глубины.")
            break

    # Вывод результатов алгоритма
    if result_node is not None:
        print("\nКонечное состояние достигнуто!")
        print_path(result_node)
        TIME_STOP = process_time()
        # Вызов функции для вывода информации о поиске
        print_info(iterations=iterations, time=TIME_STOP - START_TIME, visited_states=len(visited_states),
                   path_cost=result_node.path_cost)
    else:
        print("\nПуть к конечному состоянию не найден.")

    # Проверяем, было ли найдено хотя бы одно состояние
    if not visited_states:
        print("\nВсе состояния были исследованы, но решение не было найдено.")
