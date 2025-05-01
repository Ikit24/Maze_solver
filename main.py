from graphics import Window
from maze import Maze
from timer import Timer
import sys
import tkinter as tk
from tkinter import Frame, messagebox, Label, ttk

root = tk.Tk()
root.title("Maze Solver")

top_frame = Frame(root, width=800, height=800, bg="grey")
top_frame.pack(side="top", fill="x", padx=10, pady=5, expand=True)

bottom_frame = Frame(root, width=1200, height=800,bg="white")
bottom_frame.pack(side="bottom", fill="both", padx=10, pady=5, expand=True)

def start_maze():
    def get_int_from_entry(entry, field_name):
        try:
            value = int(entry.get())
            entry.config(bg="white")
            return value
        except ValueError:
            messagebox.showerror("Invalid input!", f"Please enter a valid integer for {field_name}")
            entry.delete(0, tk.END)
            entry.config(bg="red")
            entry.focus_set()
            return None

    rows = get_int_from_entry(row_entry, "rows")
    cols = get_int_from_entry(col_entry, "columns")
    if rows is None or cols is None:
        return
    
    entry.config(state="normal")
    rows = get_int_from_entry(row_entry, "rows")
    cols = get_int_from_entry(col_entry, "columns")
    solution_type = solentry("Input prefererred solution type 'BFS', 'DFS' or 'A_star': ").lower()
    num_rows = rows
    num_cols = cols
    margin = 50
    screen_x = 1200
    screen_y = 1000
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    start_btn.config(state="normal")
    sys.setrecursionlimit(10000)
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    print("maze created")
    t =  Timer()
    t.start()

    window = tk.Tk() 
    window.title('Combobox') 
    window.geometry('500x250')
    ttk.Label(window, text = "GFG Combobox Widget",  
          background = 'green', foreground ="white",  
          font = ("Times New Roman", 15)).grid(row = 0, column = 1) 
    ttk.Label(window, text = "Select the solution method :",
              font = ("Times New Roman", 10)).grid(column = 0, row = 5, padx = 10, pady = 25)
    n = tk.StringVar()
    solutions = ttk.Combobox(window, width = 30, textvariable= n)
    solutions['Solutions'] = (' BFS', 'DFS', ' A_star')
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
    entry.config(state="normal")

    win.wait_for_close()
    
    
    
row_label = tk.Label(top_frame, text="Enter nr of rows: ")
row_label.pack()
row_entry = tk.Entry(top_frame)
col_label = tk.Label(top_frame, text="Enter nr of cols: ")
col_label.pack()
col_entry = tk.Entry(top_frame)
start_btn = tk.Label(top_frame, text="Start!")
start_btn = tk.Button(top_frame, command=start_maze)
start_btn.pack()
main()