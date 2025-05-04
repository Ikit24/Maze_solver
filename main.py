from graphics import Window
from maze import Maze
from timer import Timer
import sys
import tkinter as tk
from tkinter import Frame, messagebox, ttk

root = tk.Tk()
root.title("Maze Solver")
timer = Timer(root)
root.geometry("400x400+360+40")

top_frame = Frame(root, width=800, height=800, bg="grey")
top_frame.pack(side="top", fill="x", padx=10, pady=5, expand=True)

row_label = tk.Label(top_frame, text="Enter nr of rows: ")
row_label.pack()
row_entry = tk.Entry(top_frame)
row_entry.pack()
col_label = tk.Label(top_frame, text="Enter nr of cols: ")
col_label.pack()
col_entry = tk.Entry(top_frame)
col_entry.pack()

solution_var = tk.StringVar()
solutions = ttk.Combobox(top_frame, width = 20, textvariable=solution_var)
solution_var.set("Choose solution method")
solutions.pack()
solutions['values'] = ('BFS', 'DFS', 'A_star')
solutions['state'] = 'readonly'

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
    selected = solution_var.get()
    if rows is None or cols is None:
        return
    
    margin = 50
    screen_x = 1200
    screen_y = 1000
    cell_size_x = (screen_x - 2 * margin) / cols
    cell_size_y = (screen_y - 2 * margin) / rows        
    main_x = root.winfo_x()
    main_y = root.winfo_y()
    maze_x = main_x + root.winfo_width() + 10
    maze_y = main_y
    win = Window(screen_x, screen_y, x_position=maze_x, y_position=maze_y)
    maze = Maze(margin, margin, rows, cols, cell_size_x, cell_size_y, win=win)
    selected = solution_var.get()

    timer.start()    
    if selected == "BFS":
        is_solvable = maze._solve_bfs(0, 0)
    elif selected == "DFS":
        is_solvable = maze._solve_r(0, 0)
    elif selected == "A_star":
        is_solvable = maze._solve_A_star(0, 0)
    if not is_solvable:
        print("maze can not be solved!")
    else:
        print("maze solved!")
    timer.stop_timer()
    sys.setrecursionlimit(10000)
    win.wait_for_close()

def on_closing():
    try:
        root.quit()
        root.destroy()
    except Exception as e:
        print(f"Error during closing: {e}")
    finally:
        import os
        os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
start_btn = tk.Button(top_frame, command=start_maze, text="Start!")
start_btn.pack()

root.mainloop()