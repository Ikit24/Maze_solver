from graphics import Window
from maze import Maze
from timer import Timer
import sys
import tkinter as tk
from tkinter import Frame, messagebox, ttk

class App:
    def __init__(self):
        # Only create ONE Tk instance
        self.root = tk.Tk()
        self.root.title("Maze Solver")
        self.root.geometry("400x400+360+40")

        # Store GUI elements as instance variables
        self.timer = Timer(self.root)
        self.top_frame = Frame(self.root, width=800, height=800, bg="grey")
        self.top_frame.pack(side="top", fill="x", padx=10, pady=5, expand=True)

        # Create and store all input widgets with self.
        self.row_entry = tk.Entry(self.top_frame)
        self.col_entry = tk.Entry(self.top_frame)
        self.depth_entry = tk.Entry(self.top_frame)
        self.solution_var = tk.StringVar()
        self.view_var = tk.StringVar(value="3D")
        self.perspective_slider = tk.Scale(self.top_frame, from_=0, to=100, orient=tk.HORIZONTAL)

        # Setup GUI elements
        self._create_widgets()
        
        # Button command must reference self.start_maze
        self.start_btn = tk.Button(self.top_frame, command=self.start_maze, text="Start!")
        self.start_btn.pack()

        # Close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def _create_widgets(self):
        # Add all labels and entries
        tk.Label(self.top_frame, text="Enter nr of rows: ").pack()
        self.row_entry.pack()
        tk.Label(self.top_frame, text="Enter nr of cols: ").pack()
        self.col_entry.pack()
        tk.Label(self.top_frame, text="Enter depth: ").pack()
        self.depth_entry.pack()

        # Perspective slider
        tk.Label(self.top_frame, text="3D Perspective:").pack()
        self.perspective_slider.set(30)
        self.perspective_slider.pack()

        # View type radio buttons
        view_frame = tk.Frame(self.top_frame)
        view_frame.pack()
        tk.Radiobutton(view_frame, text="2D View", variable=self.view_var, value="2D").pack(side="left")
        tk.Radiobutton(view_frame, text="3D View", variable=self.view_var, value="3D").pack(side="left")

        # Solution method combobox
        solutions = ttk.Combobox(self.top_frame, width=20, textvariable=self.solution_var)
        self.solution_var.set("Choose solution method")
        solutions['values'] = ('BFS', 'DFS', 'A_star')
        solutions['state'] = 'readonly'
        solutions.pack()

    def start_maze(self):
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

        rows = get_int_from_entry(self.row_entry, "rows")
        cols = get_int_from_entry(self.col_entry, "columns")
        depth = get_int_from_entry(self.depth_entry, "depth")
        selected = self.solution_var.get()

        if None in (rows, cols, depth):
            return

        # Maze parameters
        margin = 50
        screen_x = 1200
        screen_y = 1000
        size_buffer = max(cols, rows, depth) * 0.5
        cell_size_x = (screen_x - 2 * margin) / (cols + size_buffer)
        cell_size_y = (screen_y - 2 * margin) / (rows + size_buffer)
        cell_size_z = min(cell_size_x, cell_size_y) * 0.4

        win = Window(
            width=1200,
            height=1000,
            maze_width=cols * cell_size_x,
            maze_height=rows * cell_size_y,
            maze_depth=depth * cell_size_z,
            margin=50,
            fullscreen=False,
            view_type=self.view_var.get(),
            perspective=self.perspective_slider.get()
        )

        # Create maze
        maze = Maze(
            x1=margin, y1=margin, z1=0,
            num_rows=rows, num_cols=cols, _num_levels=depth,
            cell_size_x=cell_size_x, cell_size_y=cell_size_y, cell_size_z=cell_size_z,
            win=win, view_type=self.view_var.get(), perspective=self.perspective_slider.get()
        )

        # Solve maze
        self.timer.start()
        if selected == "BFS":
            is_solvable = maze._solve_bfs(0, 0, 0)
        elif selected == "DFS":
            is_solvable = maze._solve_r(0, 0, 0)
        elif selected == "A_star":
            is_solvable = maze._solve_A_star(0, 0, 0)
        self.timer.stop_timer()

        print("Maze solved!" if is_solvable else "Maze cannot be solved!")
        win.wait_for_close()

    def on_closing(self):
        try:
            self.root.destroy()
            import os
            os._exit(0)
        except Exception as e:
            print(f"Error during closing: {e}")

# Run the app
if __name__ == "__main__":
    App()