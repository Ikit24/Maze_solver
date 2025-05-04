import tkinter as tk
from tkinter import BOTH, Canvas

class Window:
    def __init__(self, width, height, x_position=None, y_position=None):
        self.__root = tk.Toplevel()
        self.__root.title("Maze Solver")
        self.__window_running = False
        if x_position is not None and y_position is not None:
            self.__root.geometry(f"{width}x{height}+{x_position}+{y_position}")        
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()

    def draw_line(self, line, fill_color="black"):
        self.__canvas.create_line(line.p1.x, line.p1.y, line.p2.x, line.p2.y, fill=fill_color, width=line.width)

    def close(self):
        self.__window_running = False
        try:
            if self.__root.winfo_exists():
                self.__root.destroy()
        except:
            pass
    def __on_closing(self):
        self.close()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2, width=1):
        self.p1 = p1
        self.p2 = p2
        self.width = width 

    def draw(self, window, fill_color="black"):
        window.draw_line(self, fill_color)

    def set_Width(self, width):
        self.width = width