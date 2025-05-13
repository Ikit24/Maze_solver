import tkinter as tk
from tkinter import BOTH, Canvas, Toplevel

class Window:
    def __init__(
        self,
        width,
        height,
        maze_width,
        maze_height,
        maze_depth,
        margin=50,
        fullscreen=False,
        x_position=None,
        y_position=None,
        view_type="3D",
        perspective=30
    ):
        self.__root = Toplevel()
        self.__root.title("Maze Solver")
        self.__margin = margin
        self.__maze_width = maze_width
        self.__maze_height = maze_height
        self.__maze_depth = maze_depth
        self.__view_type = view_type
        self.__perspective = perspective
        self.__fullscreen = fullscreen
        self.__canvas = None

        # Handle fullscreen mode
        if self.__fullscreen:
            self.__root.attributes("-fullscreen", True)
            width = self.__root.winfo_screenwidth()
            height = self.__root.winfo_screenheight()
        elif x_position is not None and y_position is not None:
            self.__root.geometry(f"{width}x{height}+{x_position}+{y_position}")

        # Setup canvas with dynamic resizing
        self.__canvas = Canvas(
            self.__root, 
            bg="white", 
            height=height, 
            width=width,
            highlightthickness=0
        )
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__window_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def _project_3d_to_2d(self, x, y, z):
        # Get current canvas dimensions
        canvas_width = self.__canvas.winfo_width()
        canvas_height = self.__canvas.winfo_height()

        # Calculate available drawing area
        draw_width = canvas_width - 2 * self.__margin
        draw_height = canvas_height - 2 * self.__margin

        # Calculate dynamic scaling factors
        x_scale = draw_width / max(self.__maze_width, 1)
        y_scale = draw_height / max(self.__maze_height + self.__maze_depth, 1)
        scale = min(x_scale, y_scale) * 0.85  # 15% buffer

        # Calculate isometric projection
        iso_x = (x - y) * 0.866 * scale
        iso_y = (x + y) * 0.5 * scale - z * scale * 0.3

        # Center the projection
        center_x = self.__margin + (draw_width / 2)
        center_y = self.__margin + (draw_height / 2)

        return center_x + iso_x, center_y + iso_y

    def draw_line(self, line, fill_color="black"):
        # Convert 3D points to 2D projection
        x1, y1 = self._project_3d_to_2d(line.p1.x, line.p1.y, line.p1.z)
        x2, y2 = self._project_3d_to_2d(line.p2.x, line.p2.y, line.p2.z)
        self.__canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=line.width)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def close(self):
        self.__window_running = False
        self.__root.destroy()

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

class Line:
    def __init__(self, p1, p2, width=1):
        self.p1 = p1
        self.p2 = p2
        self.width = width

    def draw(self, window, fill_color="black"):
        window.draw_line(self, fill_color)

    def set_width(self, width):
        self.width = width

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"

class Line:
    def __init__(self, p1, p2, width=1):
        self.p1 = p1
        self.p2 = p2
        self.width = width

    def draw(self, window, fill_color="black"):
        window.draw_line(self, fill_color)

    def set_width(self, width):
        self.width = width