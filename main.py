from graphics import Window
from maze import Maze
import sys
import time


def main():
    row_inpt = int(input("Input the number of rows "))
    col_inpt = int(input("Input the number of colums "))
    solution_type = input("Input prefererred solution type 'BFS', 'DFS' or 'A_star': ").lower()
    num_rows = row_inpt
    num_cols = col_inpt
    margin = 50
    screen_x = 1200
    screen_y = 1000
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows

    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    print("maze created")
    tic = time.perf_counter()
    if solution_type == "bfs":
        is_solvable = maze._solve_bfs(0, 0)
    elif solution_type == "dfs":
        is_solvable = maze._solve_r(0, 0)
    elif solution_type == "a_star":
        is_solvable = maze._solve_A_star(0, 0)
    if not is_solvable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    toc = time.perf_counter()

    print(f"Maze solved in {toc - tic:0.2f} seconds")

    win.wait_for_close()


main()