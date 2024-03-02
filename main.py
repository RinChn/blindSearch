import subprocess
import sys

from tabulate import tabulate

from ComponOfTree.tree import Tree
from Strategies.dfs import dfs
from Strategies.dls import dls

if __name__ == '__main__':
    TREE = Tree()

    mode = input("Выберите стратегию:\n" +
                 tabulate(
                     [["1", "DFS"], ["2", "DLS"], ["3", "Вывести\nсправку"]],
                     headers=["№", "Стратегия"],
                     tablefmt="grid")
                 + '\n> ')

    match mode:
        case '2':
            depth_limit = int(input("Введите ограничение на глубину:\n> "))
            dls(depth_limit)
        case '1':
            dfs()
        case _:
            print("Некорректный ввод")
