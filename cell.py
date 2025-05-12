from graphics import Line, Point
import time

class Cell:
    def __init__(self, win=None, view_type="3D", perspective=30):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.has_ceiling_wall = True
        self.has_floor_wall  = True 
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._z1 = None
        self._z2 = None
        self._win = win
        self.view_type = view_type
        self.perspective = perspective

    def set_coordinates(self, x1, y1, z1, x2, y2, z2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._z1 = z1
        self._z2 = z2

    def draw(self):
        if self._win is None:
            return

        if self.view_type == "3D":
            self._draw_wall(Point(self._x1, self._y2, self._z1), Point(self._x1, self._y1, self._z1), self.has_left_wall)
            self._draw_wall(Point(self._x1, self._y1, self._z1), Point(self._x2, self._y1, self._z1), self.has_top_wall)
            self._draw_wall(Point(self._x2, self._y1, self._z1), Point(self._x2, self._y2, self._z1), self.has_right_wall)
            self._draw_wall(Point(self._x2, self._y2, self._z1), Point(self._x1, self._y2, self._z1), self.has_bottom_wall)

            self._draw_wall(Point(self._x1, self._y1, self._z1), Point(self._x1, self._y1, self._z2), self.has_ceiling_wall)
            self._draw_wall(Point(self._x2, self._y1, self._z1), Point(self._x2, self._y1, self._z2), self.has_ceiling_wall)
        else:
            self._draw_wall(Point(self._x1, self._y1), Point(self._x2, self._y1), self.has_top_wall)
            self._draw_wall(Point(self._x2, self._y1), Point(self._x2, self._y2), self.has_right_wall)
            self._draw_wall(Point(self._x2, self._y2), Point(self._x1, self._y2), self.has_bottom_wall)
            self._draw_wall(Point(self._x1, self._y2), Point(self._x1, self._y1), self.has_left_wall)

    def _draw_wall(self, p1, p2, wall_exists):
        line = Line(p1, p2)
        if wall_exists:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        
        x_center = (self._x1 + self._x2) / 2
        y_center = (self._y1 + self._y2) / 2
        z_center = (self._z1 + self._z2) / 2
            
        x_center2 = (to_cell._x1 + to_cell._x2) / 2
        y_center2 = (to_cell._y1 + to_cell._y2) / 2
        z_center2 = (to_cell._z1 + to_cell._z2) / 2
            
        fill_color = "green" if not undo else "red"
        
        line_width = 3
        
        line = Line(
            Point(x_center, y_center, z_center), 
            Point(x_center2, y_center2, z_center2),
            width=line_width
        )
        self._win.draw_line(line, fill_color)
        
        if undo:
            time.sleep(0.01)
        else:
            time.sleep(0.05)