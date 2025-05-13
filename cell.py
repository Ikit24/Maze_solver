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

        # Bottom face (z1 level)
        bottom_nw = Point(self._x1, self._y1, self._z1)
        bottom_ne = Point(self._x2, self._y1, self._z1)
        bottom_se = Point(self._x2, self._y2, self._z1)
        bottom_sw = Point(self._x1, self._y2, self._z1)

        # Draw bottom walls
        self._draw_wall(bottom_sw, bottom_nw, self.has_left_wall)
        self._draw_wall(bottom_nw, bottom_ne, self.has_top_wall)
        self._draw_wall(bottom_ne, bottom_se, self.has_right_wall)
        self._draw_wall(bottom_se, bottom_sw, self.has_bottom_wall)

        if self.view_type == "3D":
            # Top face (z2 level)
            top_nw = Point(self._x1, self._y1, self._z2)
            top_ne = Point(self._x2, self._y1, self._z2)
            top_se = Point(self._x2, self._y2, self._z2)
            top_sw = Point(self._x1, self._y2, self._z2)

            # Draw top walls
            self._draw_wall(top_sw, top_nw, self.has_left_wall)
            self._draw_wall(top_nw, top_ne, self.has_top_wall)
            self._draw_wall(top_ne, top_se, self.has_right_wall)
            self._draw_wall(top_se, top_sw, self.has_bottom_wall)

            # Vertical pillars (connect bottom and top)
            self._draw_wall(bottom_nw, top_nw, self.has_ceiling_wall)
            self._draw_wall(bottom_ne, top_ne, self.has_ceiling_wall)
            self._draw_wall(bottom_se, top_se, self.has_ceiling_wall)
            self._draw_wall(bottom_sw, top_sw, self.has_ceiling_wall)

            # Back face pillars (for depth perception)
            self._draw_wall(top_nw, top_ne, self.has_ceiling_wall)
            self._draw_wall(top_ne, top_se, self.has_ceiling_wall)

    def _draw_wall(self, p1, p2, wall_exists):
        line = Line(p1, p2)
        if wall_exists:
            self._win.draw_line(line)
        else:
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        # Calculate centers with a slight offset toward the front
        offset = 0.15  # 15% offset to avoid overlapping walls
        x_center = (self._x1 + self._x2) / 2 + (self._x2 - self._x1) * offset
        y_center = (self._y1 + self._y2) / 2 + (self._y2 - self._y1) * offset
        z_center = (self._z1 + self._z2) / 2

        x_center2 = (to_cell._x1 + to_cell._x2) / 2 + (to_cell._x2 - to_cell._x1) * offset
        y_center2 = (to_cell._y1 + to_cell._y2) / 2 + (to_cell._y2 - to_cell._y1) * offset
        z_center2 = (to_cell._z1 + to_cell._z2) / 2

        # Draw line
        color = "red" if undo else "green"
        line = Line(
            Point(x_center, y_center, z_center),
            Point(x_center2, y_center2, z_center2),
            width=3
        )
        self._win.draw_line(line, color)