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
depth_label = tk.Label(top_frame, text="Enter depth: ")
depth_label.pack()
depth_entry = tk.Entry(top_frame)
depth_entry.pack()

# Add a slider for 3D perspective adjustment
perspective_label = tk.Label(top_frame, text="3D Perspective:")
perspective_label.pack()
perspective_slider = tk.Scale(top_frame, from_=0, to=100, orient=tk.HORIZONTAL)
perspective_slider.set(30)  # Default value
perspective_slider.pack()

view_var = tk.StringVar(value="3D")
view_frame = tk.Frame(top_frame)
view_frame.pack()
tk.Radiobutton(view_frame, text="2D View", variable=view_var, value="2D").pack(side="left")
tk.Radiobutton(view_frame, text="3D View", variable=view_var, value="3D").pack(side="left")

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
    depth = get_int_from_entry(depth_entry, "depth")
    selected = solution_var.get()
    
    if rows is None or cols is None or depth is None:
        return
    
    margin = 50
    screen_x = 1200
    screen_y = 1000
    cell_size_x = (screen_x - 2 * margin) / cols
    cell_size_y = (screen_y - 2 * margin) / rows
    cell_size_z = min(cell_size_x, cell_size_y) / 2
    
    main_x = root.winfo_x()
    main_y = root.winfo_y()
    maze_x = main_x + root.winfo_width() + 10
    maze_y = main_y
    
    # Get perspective value if the slider exists
    perspective = perspective_slider.get() if 'perspective_slider' in globals() else 30
    
    # Get view type if the radio buttons exist
    view_type = view_var.get() if 'view_var' in globals() else "3D"
    
    win = Window(screen_x, screen_y, x_position=maze_x, y_position=maze_y)
    maze = Maze(
        x1=margin, 
        y1=margin, 
        z1=0,            # Z position offset
        num_rows=rows, 
        num_cols=cols, 
        _num_levels=depth,
        cell_size_x=cell_size_x, 
        cell_size_y=cell_size_y, 
        cell_size_z=cell_size_z, 
        win=win,
        view_type=view_type,      # Pass view_type parameter
        perspective=perspective
    )
    selected = solution_var.get()

    timer.start()    
    if selected == "BFS":
        is_solvable = maze._solve_bfs(0, 0, 0)  # Added z=0 parameter for starting position
    elif selected == "DFS":
        is_solvable = maze._solve_r(0, 0, 0)    # Added z=0 parameter for starting position
    elif selected == "A_star":
        is_solvable = maze._solve_A_star(0, 0, 0)  # Added z=0 parameter for starting position
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