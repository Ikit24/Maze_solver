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

    def draw(self, x1, y1, x2, y2, z1=0, z2=0):
        if self._win is None:
            return
        
        # Bottom face
        bottom_nw = Point(x1, y1, z1)
        bottom_ne = Point(x2, y1, z1)
        bottom_se = Point(x2, y2, z1)
        bottom_sw = Point(x1, y2, z1)

        # Draw bottom face walls (used in both 2D and 3D)
        if self.has_left_wall:
            line = Line(bottom_sw, bottom_nw)
            self._win.draw_line(line)
        else:
            line = Line(bottom_sw, bottom_nw)
            self._win.draw_line(line, "white")
            
        if self.has_top_wall:
            line = Line(bottom_nw, bottom_ne)
            self._win.draw_line(line)
        else:
            line = Line(bottom_nw, bottom_ne)
            self._win.draw_line(line, "white")
        
        if self.has_right_wall:
            line = Line(bottom_ne, bottom_se)
            self._win.draw_line(line)
        else:
            line = Line(bottom_ne, bottom_se)
            self._win.draw_line(line, "white")
        
        if self.has_bottom_wall:
            line = Line(bottom_se, bottom_sw)
            self._win.draw_line(line)
        else:
            line = Line(bottom_se, bottom_sw)
            self._win.draw_line(line, "white")

        # If in 3D mode, draw the additional 3D elements
        if self.view_type == "3D":
            # Top face
            top_nw = Point(x1, y1, z2)
            top_ne = Point(x2, y1, z2)
            top_se = Point(x2, y2, z2)
            top_sw = Point(x1, y2, z2)
            
            # Draw top face
            if self.has_left_wall:
                line = Line(top_sw, top_nw)
                self._win.draw_line(line)
            else:
                line = Line(top_sw, top_nw)
                self._win.draw_line(line, "white")
            
            if self.has_top_wall:
                line = Line(top_nw, top_ne)
                self._win.draw_line(line)
            else:
                line = Line(top_nw, top_ne)
                self._win.draw_line(line, "white")
            
            if self.has_right_wall:
                line = Line(top_ne, top_se)
                self._win.draw_line(line)
            else:
                line = Line(top_ne, top_se)
                self._win.draw_line(line, "white")
            
            if self.has_bottom_wall:
                line = Line(top_se, top_sw)
                self._win.draw_line(line)
            else:
                line = Line(top_se, top_sw)
                self._win.draw_line(line, "white")
        
            # Draw vertical edges connecting top and bottom faces
            if self.has_ceiling_wall:
                # Northwest vertical
                line = Line(bottom_nw, top_nw)
                self._win.draw_line(line)
                # Northeast vertical
                line = Line(bottom_ne, top_ne)
                self._win.draw_line(line)
                # Southeast vertical
                line = Line(bottom_se, top_se)
                self._win.draw_line(line)
                # Southwest vertical
                line = Line(bottom_sw, top_sw)
                self._win.draw_line(line)
            else:
                # Northwest vertical
                line = Line(bottom_nw, top_nw)
                self._win.draw_line(line, "white")
                # Northeast vertical
                line = Line(bottom_ne, top_ne)
                self._win.draw_line(line, "white")
                # Southeast vertical
                line = Line(bottom_se, top_se)
                self._win.draw_line(line, "white")
                # Southwest vertical
                line = Line(bottom_sw, top_sw)
                self._win.draw_line(line, "white")

            # Floor pattern
            if self.has_floor_wall:
                # X pattern for the floor
                line = Line(bottom_nw, bottom_se)
                self._win.draw_line(line)
                line = Line(bottom_ne, bottom_sw)
                self._win.draw_line(line)
            else:
                # X pattern for the floor in white (indicating no wall)
                line = Line(bottom_nw, bottom_se)
                self._win.draw_line(line, "white")
                line = Line(bottom_ne, bottom_sw)
                self._win.draw_line(line, "white")

            # Ceiling pattern
            if self.has_ceiling_wall:
                # X pattern for the ceiling
                line = Line(top_nw, top_se)
                self._win.draw_line(line)
                line = Line(top_ne, top_sw)
                self._win.draw_line(line)
            else:
                # X pattern for the ceiling in white (indicating no wall)
                line = Line(top_nw, top_se)
                self._win.draw_line(line, "white")
                line = Line(top_ne, top_sw)
                self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        # Calculate center of current cell
        x_center = (self._x1 + self._x2) // 2
        y_center = (self._y1 + self._y2) // 2
        z_center = (self._z1 + self._z2) // 2
            
        # Calculate center of destination cell
        x_center2 = (to_cell._x1 + to_cell._x2) // 2
        y_center2 = (to_cell._y1 + to_cell._y2) // 2
        z_center2 = (to_cell._z1 + to_cell._z2) // 2
            
        fill_color = "green"
        if undo:
            fill_color = "red"
            time.sleep(0.01)
        else:
            time.sleep(0.08)
            
        # Draw a line from the center of the current cell to the center of the destination cell
        line = Line(Point(x_center, y_center, z_center), 
                    Point(x_center2, y_center2, z_center2), 
                    width=3)
        self._win.draw_line(line, fill_color)
        