import os

import psutil

from ComponOfTree.node import Node
from ComponOfTree.tree import get_finish_state

TREE = None  # дерево решения
START_TIME = 0  # время запуска программы
TIME_STOP = 0  # время окончания программы


def check_final(current_state: list) -> bool:
    ''' Проверка, является ли данное состояние конечным '''
    return current_state == get_finish_state()


def state_swap(new_states: dict, current_state: list, move: tuple):
    ''' Обменивает пустую ячейку с соседней ячейкой в соответствии с передвижением '''
    state = [row[:] for row in current_state]  # Создаем копию состояния, чтобы не изменять оригинальное
    pos_i, pos_j = None, None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                pos_i, pos_j = i, j
                break
    new_pos_i = pos_i + move[0]
    new_pos_j = pos_j + move[1]
    if 0 <= new_pos_i < 3 and 0 <= new_pos_j < 3:
        state[pos_i][pos_j], state[new_pos_i][new_pos_j] = state[new_pos_i][new_pos_j], state[pos_i][pos_j]
        new_states[move] = state


def get_new_states(current_state: list) -> dict[tuple, list[Node]]:
    ''' Получение новых состояний поля '''
    new_states = {}
    MOVES = {
        "UP": (-1, 0),    # Вверх
        "DOWN": (1, 0),    # Вниз
        "LEFT": (0, -1),   # Влево
        "RIGHT": (0, 1)    # Вправо
    }
    for action, move in MOVES.items():
        state_swap(new_states, current_state, move)
    return new_states


def print_info(iterations: int, time: float):
    print(f"Итого узлов: {Node.get_nodes_count()}")
    print(f"Итого итераций: {iterations}")
    print(f"Потраченное время процессора: {time*1000} миллисекунд")
    print(f"Памяти использовано: {psutil.Process(os.getpid()).memory_info().rss} байтов")


def state_hash(state: list) -> int:
    ''' Хэширование состояния (листа)'''
    return hash(tuple(map(tuple, state)))