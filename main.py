from graphics import Window
from maze import Maze
from timer import Timer
import sys
import tkinter as tk
from tkinter import Frame, messagebox

root = tk.Tk()
root.title("Maze Solver")

top_frame = Frame(root, width=400, height=400, bg="grey")
top_frame.pack(side="top", fill="x", padx=10, pady=5, expand=True)

bottom_frame = Frame(root, width=1200, height=800,bg="white")
bottom_frame.pack(side="bottom", fill="both", padx=10, pady=5, expand=True)

row_entry = tk.Entry(top_frame, text="Enter nr of rows! ")
start_btn = tk.Button(top_frame, text="Start", command=start_maze)
start.pack()

def start_maze():
    try:
        rows = int(row_entry.get())
    except ValueError:
        messagebox.showerror("Invalide input!", "Please enter a valid integer for rows.")

def main():
    t =  Timer()
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
    
    t.start()
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
    t.stop()

    win.wait_for_close()

main()