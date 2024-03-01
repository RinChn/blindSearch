import sys

from ComponOfTree.tree import Tree
from Strategies.dfs import dfs
from Strategies.dls import dls

if __name__ == '__main__':
    TREE = Tree()

    if len(sys.argv) == 3 and sys.argv[1] == '--dls':
        depth_limit = int(sys.argv[2])
        dls(depth_limit)
    elif len(sys.argv) == 2:
        if sys.argv[1] == '--dls':
            dls()  # Здесь задаем глубину поиска dls
        elif sys.argv[1] == '--dfs':
            dfs()
        elif sys.argv[1] == '-h':
            print(f"{sys.argv[0]} --dfs - deep-first search algorithm")
            print(f"{sys.argv[0]} --dls <depth_limit> - depth-first search algorithm with depth limit") 
        else:
            print(
                f"Ошибка! Неверный параметр. \nВведите {sys.argv[0]} -h  \n")
    else:
        print(
            f"Ошибка! Неверное кол-во параметров. \nВведите {sys.argv[0]} -h \n")
