from cell import Cell
from collections import deque
import random
import time
import heapq

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self.maze_solve = False

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

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
        time.sleep(0.03)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True        
        while True:
            next_index_lst = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i-1][j].visited:
                next_index_lst.append((i - 1, j))
            # right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_lst.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_lst.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_lst.append((i, j + 1))
            
            # if there's nowhere to go from here
            # break out
            if len(next_index_lst) == 0:
                self._draw_cell(i, j)
                return
            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_lst))
            next_index = next_index_lst[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])        

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True
        # Left
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        # Right    
        if i < self._num_cols - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)
        # Up
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        # Down
        if j < self._num_rows - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_bottom_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        
        return False
        
    def solve(self):
        self._reset_cells_visited()
        result = self._solve_A_star(0, 0)
        self.maze_solve = result
        return result
    
    def _solve_bfs(self, i, j):
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        queue = deque([(i, j)])
        self._cells[i][j].visited = True

        while queue:
            current_i, current_j = queue.popleft()
            self._animate()

            if current_i == self._num_rows - 1 and current_j == self._num_cols - 1:
                return True
            
            # Left
            if current_i > 0 and not self._cells[current_i - 1][current_j].visited and not self._cells[current_i][current_j].has_left_wall:
                self._cells[current_i][current_j].draw_move(self._cells[current_i - 1][current_j])
                self._cells[current_i - 1][current_j].visited = True
                queue.append((current_i - 1, current_j))
            # Right
            if current_i < self._num_cols - 1 and not self._cells[current_i + 1][current_j].visited and not self._cells[current_i][current_j].has_right_wall:
                self._cells[current_i][current_j].draw_move(self._cells[current_i + 1][current_j])
                self._cells[current_i + 1][current_j]. visited = True
                queue.append((current_i + 1, current_j))
            # Up
            if current_j > 0 and not self._cells[current_i][current_j - 1].visited and not self._cells[current_i][current_j].has_top_wall:
                self._cells[current_i][current_j].draw_move(self._cells[current_i][current_j - 1])
                self._cells[current_i][current_j - 1].visited = True
                queue.append((current_i, current_j - 1))
            # Down
            if current_j < self._num_rows - 1 and not self._cells[current_i][current_j + 1].visited and not self._cells[current_i][current_j].has_bottom_wall:
                self._cells[current_i][current_j].draw_move(self._cells[current_i][current_j + 1])
                self._cells[current_i][current_j + 1].visited = True
                queue.append((current_i, current_j + 1))     
        # No path found
        return False
    
    def _calculate_heuristic(self, current, goal):
        current_i, current_j = current
        goal_i, goal_j = goal
        
        # Manhattan distance
        return abs(current_i - goal_i) + abs(current_j - goal_j)

    
    def _solve_A_star(self, start_i, start_j):
        goal_i, goal_j = self._num_rows - 1, self._num_cols - 1

        if start_i == goal_i and start_j == goal_j:
            return True
        
        # Tracks teps from start
        g_scores = {}
        g_scores[(start_i, start_j)] = 0

        # Calculate f scores (g + h)
        f_scores = {}
        f_scores[(start_i, start_j)] = self._calculate_heuristic((start_i, start_j), (goal_i, goal_j))

        # Priority queue
        open_set = []
        heapq.heappush(open_set, (f_scores[(start_i, start_j)], (start_i, start_j)))

        # Track visited cells for reconstruction
        visited = set()
        parents = {}

        while open_set:
            _, (current_i, current_j) = heapq.heappop(open_set)
            self._animate()

            if current_i == goal_i and current_j == goal_j:
                return True
            visited.add((current_i, current_j))
            self._cells[current_i][current_j].visited = True
            # Left
            if (current_i > 0 and not self._cells[current_i][current_j].has_left_wall):
                neighbor = (current_i - 1, current_j)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j].draw_move(self._cells[neighbor[0]][neighbor[1]])
                        self._cells[neighbor[0]][neighbor[1]].visited = True
            
            # Right
            if (current_i < self._num_rows - 1 and not self._cells[current_i][current_j].has_right_wall):
                neighbor = (current_i + 1, current_j)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j].draw_move(self._cells[neighbor[0]][neighbor[1]])
                        self._cells[neighbor[0]][neighbor[1]].visited = True

            # Up
            if (current_j > 0 and not self._cells[current_i][current_j].has_top_wall):
                neighbor = (current_i, current_j - 1)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j].draw_move(self._cells[neighbor[0]][neighbor[1]])
                        self._cells[neighbor[0]][neighbor[1]].visited = True

            # Down
            if (current_j < self._num_rows - 1 and not self._cells[current_i][current_j].has_bottom_wall):
                neighbor = (current_i, current_j + 1)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j].draw_move(self._cells[neighbor[0]][neighbor[1]])
                        self._cells[neighbor[0]][neighbor[1]].visited = True
        return False