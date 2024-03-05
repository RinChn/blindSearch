import sys
from time import process_time

from node import Node
from basic_operations import print_info, check_final, state_hash, \
    get_followers, print_node, print_state, MOVES, \
    print_path, get_initial_state, get_action_name

sys.setrecursionlimit(1000000)  # Предел рекурсии
global DEBUG


def dfs(debug_flag: int, depth_limit: int = None):
    """
    Поиск в глубину.
    :param debug_flag:
    :param depth_limit: Ограничение для поиска с ограничением глубины.
    """


    DEBUG = debug_flag
    # Выводим сообщение о начале алгоритма DLS
    print("ПОИСК В ГЛУБИНУ С ОГРАНИЧЕНИЕМ DLS - Deep-Limited Search.")
    start_node = Node(get_initial_state(), None, None, 0, 0)  # Начальный узел
    visited_states = set()  # Множество посещенных состояний
    stack = [start_node]  # Стек для хранения узлов
    result_node = None  # Переменная для хранения результата
    iterations = 0  # Счетчик итераций
    # dls.limit_reached = False

    START_TIME = process_time()
    # Основной цикл алгоритма
    while stack:
        result_node, iterations = dls(stack.pop(), visited_states, stack, iterations, depth_limit)
        if result_node is not None:
            break

    if result_node is not None:
        print("\n---Конечное состояние достигнуто!---")
        TIME_STOP = process_time()
        print_path(result_node)
        print("\nКонечное состояние достигнуто!")
        print_info(iterations=iterations, time=TIME_STOP - START_TIME, visited_states=len(visited_states),
                   path_cost=result_node.path_cost)
    else:
        print("\nПуть к конечному состоянию не найден.")

    if not visited_states:
        print("\nВсе состояния были исследованы, но решение не было найдено.")


def dls(current_node: "Node", visited_states: set,
        stack: list, iterations: int, depth_limit: int = None):
    """
    Рекурсивная часть алгоритма поиска в глубину.
    :param current_node: Текущий обрабатываемый узел.
    :param visited_states: Список посещённых состояний.
    :param stack: Стек, в котором хранятся пройденные узлы.
    :param iterations: Количество прошедших итераций.
    :param depth_limit: Ограничение в глубину для поиска с ограничением.
    :return: Найденное конечное состояние и затраченное для этого количество итераций.
    """
    iterations += 1  # Увеличиваем счетчик итераций

    # Проверяем, достигнуто ли конечное состояние
    if check_final(current_node.current_state):
        return current_node, iterations

    # Хэшируем текущее состояние для проверки посещенных состояний
    state_hash_value = state_hash(current_node.current_state)

    # Если состояние уже посещалось, пропускаем его
    if state_hash_value in visited_states:
        return None, iterations

    # Добавляем текущее состояние в множество посещенных
    visited_states.add(state_hash_value)

    # Если установлено ограничение глубины и текущая глубина превышает лимит, выводим сообщение и прекращаем поиск
    if depth_limit is not None and current_node.depth >= depth_limit:
        if not dls_recursive_with_stack.limit_reached:
            print("\nДостигнуто ограничение глубины!")
            stack.clear() # Очищаем очередь
            dls_recursive_with_stack.limit_reached = True # Меняем флаг достижения глубины
        return None, iterations

    # Получаем новые состояния из текущего узла
    new_states_dict = get_new_states(current_node.current_state)
    
    # Отладочный вывод текущего узла и всех его потомков по шагам
    if DEBUG:
        print(f"----------------Шаг: {iterations}.---------------- \n")
        print("Текущий узел:", end=' ')
        if iterations == 1:
            print("Корень дерева")
        print_node(current_node)
        print("Потомки:")
                
    # Рекурсивно исследуем каждого потомка
    for child_action, child_state in new_states_dict.items():
        child_hash_value = state_hash(child_state) 
        if DEBUG: # При отладке создаем каждого потомка
            child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1, current_node.depth + 1)
        if child_hash_value not in visited_states:
            if not DEBUG: # Иначе - только потомков с уникальными состояниями
                child_node = Node(child_state, current_node, child_action, current_node.path_cost + 1, current_node.depth + 1)
            else:
                print_node(child_node) # Выводим потомков с уникальными состояниями при отладке
            stack.append(child_node) # Помещаем узел в очередь
        else:
            if DEBUG:
                print_node(child_node, is_duplicate=True) # Выводим потомков с повторными состояниями при отладке
    if DEBUG:
        input("Нажмите 'Enter' для продолжения...")
                
    # Обработка потомков
    while stack:
        next_node = stack.pop()
        result_node, iterations = dls_recursive_with_stack(next_node, visited_states, stack, iterations, depth_limit)
        if result_node is not None:
            return result_node, iterations

    return None, iterations
