import tkinter as tk
from tkinter import BOTH, Canvas

class Window:
    def __init__(self, width, height, x_position=None, y_position=None, view_type="3D", perspective=30):
        """
        Initialize a window with the given width and height.
        """
        self.__root = tk.Toplevel()
        self.__root.title("Maze Solver")
        
        # Store view preferences
        self.__view_type = view_type
        self.__perspective = perspective
        
        if x_position is not None and y_position is not None:
            self.__root.geometry(f"{width}x{height}+{x_position}+{y_position}")        
        
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__window_running = False
        
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_closing)
        
    # Other methods remain the same...
    
    def set_view_mode(self, view_type):
        """Set the view mode (2D or 3D)"""
        self.__view_type = view_type
        
    def set_perspective(self, perspective):
        """Set the perspective value for 3D projection"""
        self.__perspective = perspective
        
    def get_view_mode(self):
        """Get the current view mode"""
        return self.__view_type
        
    def get_perspective(self):
        """Get the current perspective value"""
        return self.__perspective

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__window_running = True
        while self.__window_running:
            self.redraw()

    def draw_line(self, line, fill_color="black"):
        x1, y1 = self._project_3d_to_2d(line.p1.x, line.p1.y, line.p1.z)
        x2, y2 = self._project_3d_to_2d(line.p2.x, line.p2.y, line.p2.z)
        self.__canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=line.width)

    def _project_3d_to_2d(self, x, y, z):
        # Adjust scaling based on maze size
        scale = 0.8  # Reduce scale to fit cells
        z_scale = 0.5  # Flatten z-axis impact
        
        # Isometric projection with rotation
        iso_x = (x - y) * 0.866 * scale
        iso_y = (x + y) * 0.5 * scale - z * z_scale * scale
        
        # Center the projection
        canvas_width = self.__canvas.winfo_width() or 1200
        canvas_height = self.__canvas.winfo_height() or 1000
        center_x = canvas_width * 0.5
        center_y = canvas_height * 0.4  # Shift upward for better visibility
        
        return center_x + iso_x, center_y + iso_y

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
    def __init__(self, x, y, z=0):
        """
        Creates a point in 3D space.
        In our coordinate system:
        - x increases to the right
        - y increases going down
        - z increases going up
        """
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