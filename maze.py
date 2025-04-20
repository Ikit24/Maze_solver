from cell import Cell
import time

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win

        self._create_cells()

    def _create_cells(self):        
        for i in range(self._num_cols):
            columns = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                columns.append(cell)
            self._cells.append(columns)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i , j):
       if self._win is None:
            return    
       x1 = self.x1 + (i * self.cell_size_x)
       y1 = self.y1 + (j * self.cell_size_y)
       x2 = x1 + self.cell_size_x
       y2 = y1 + self.cell_size_y
       self._cells[i][j].draw(x1, y1, x2, y2)
       self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)