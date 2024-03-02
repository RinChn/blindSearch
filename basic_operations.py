import os
import psutil

from ComponOfTree.node import Node
from ComponOfTree.tree import get_finish_state


def check_final(current_state: list) -> bool:
    """
    Проверка состояния на то, является ли оно конечным
    :param current_state: проверяемое состояние
    :return: True, если состояние конечное; False иначе
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
    MOVES = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "LEFT": (0, -1),
        "RIGHT": (0, 1)
    }
    pos_i, pos_j = get_empty_cell(current_state)
    for action, move in MOVES.items():
        state_swap(new_states, current_state, move, pos_i, pos_j)
    return new_states


def print_info(iterations: int, time: float):
    """
    Результирующий вывод информации о процессе выполнения стратегии.
    :param iterations: Количество итераций, совершённых в процессе поиска.
    :param time: Время поиска в секундах.
    """
    print(f"Итого узлов: {Node.get_nodes_count()}")
    print(f"Итого итераций: {iterations}")
    print(f"Потраченное время процессора: {time*1000} миллисекунд")
    print(f"Памяти использовано: {psutil.Process(os.getpid()).memory_info().rss} байтов")


def state_hash(state: list) -> int:
    """
    Хэширование состояния.
    :param state: Состояние.
    :return: Хэш-таблица состояния.
    """
    return hash(tuple(map(tuple, state)))