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
        z1,
        num_rows,
        num_cols,
        _num_levels,
        cell_size_x,
        cell_size_y,
        cell_size_z,
        depth=1,
        win=None,
        seed=None,
        view_type="3D",
        perspective=30
    ):
        self.view_type = view_type
        self.perspective = perspective
        
        self._cells = []
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._num_levels = _num_levels
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.cell_size_z = cell_size_z
        self._win = win
        self.maze_solve = False

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0, 0)
        self._reset_cells_visited()

    def _create_cells(self):  
        self._cells = []
        for i in range(self._num_cols):
            columns = []
            for j in range(self._num_rows):
                rows = []
                for k in range(self._num_levels):
                    cell = Cell(self._win, view_type=self.view_type, perspective=self.perspective)
                    cell.k = k
                    rows.append(cell)
                    
                    # Set cell coordinates for 3D drawing
                    x1 = self.x1 + i * self.cell_size_x
                    y1 = self.y1 + j * self.cell_size_y
                    z1 = self.z1 + k * self.cell_size_z
                    x2 = x1 + self.cell_size_x
                    y2 = y1 + self.cell_size_y
                    z2 = z1 + self.cell_size_z
                    
                    cell.set_coordinates(x1, y1, z1, x2, y2, z2)
                    
                columns.append(rows)
            self._cells.append(columns)

        # Draw all cells at their initial position
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                for k in range(self._num_levels):
                    self._draw_cell(i, j, k)

    def _draw_cell(self, i, j, k):
        if self._win is None:
            return
        # Remove the parameters passed to draw()
        self._cells[i][j][k].draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.01)
        
    def _break_entrance_and_exit(self):
        # Entrance: Break front-left wall at level 0
        self._cells[0][0][0].has_left_wall = False
        self._draw_cell(0, 0, 0)

        # Exit: Break far-right wall at the highest level
        exit_i = self._num_cols - 1
        exit_j = self._num_rows - 1
        exit_k = self._num_levels - 1
        self._cells[exit_i][exit_j][exit_k].has_right_wall = False
        self._draw_cell(exit_i, exit_j, exit_k)

    # Update _break_walls_r method in maze.py
    def _break_walls_r(self, i, j, k=0):
        self._cells[i][j][k].visited = True
        
        neighbors = []
        
        # Check left neighbor
        if i > 0 and not self._cells[i - 1][j][k].visited:
            neighbors.append(("left", i - 1, j, k))
        
        # Check right neighbor
        if i < self._num_cols - 1 and not self._cells[i + 1][j][k].visited:
            neighbors.append(("right", i + 1, j, k))
        
        # Check top neighbor
        if j > 0 and not self._cells[i][j - 1][k].visited:
            neighbors.append(("top", i, j - 1, k))
        
        # Check bottom neighbor
        if j < self._num_rows - 1 and not self._cells[i][j + 1][k].visited:
            neighbors.append(("bottom", i, j + 1, k))
        
        # Check up neighbor (increase in z)
        if k < self._num_levels - 1 and not self._cells[i][j][k + 1].visited:
            neighbors.append(("up", i, j, k + 1))
        
        # Check down neighbor (decrease in z)
        if k > 0 and not self._cells[i][j][k - 1].visited:
            neighbors.append(("down", i, j, k - 1))
        
        # Randomize the neighbors
        random.shuffle(neighbors)
        
        # Visit each neighbor
        for direction, next_i, next_j, next_k in neighbors:
            if direction == "left":
                self._cells[i][j][k].has_left_wall = False
                self._cells[next_i][next_j][next_k].has_right_wall = False
            elif direction == "right":
                self._cells[i][j][k].has_right_wall = False
                self._cells[next_i][next_j][next_k].has_left_wall = False
            elif direction == "top":
                self._cells[i][j][k].has_top_wall = False
                self._cells[next_i][next_j][next_k].has_bottom_wall = False
            elif direction == "bottom":
                self._cells[i][j][k].has_bottom_wall = False
                self._cells[next_i][next_j][next_k].has_top_wall = False
            elif direction == "up":
                self._cells[i][j][k].has_ceiling_wall = False
                self._cells[next_i][next_j][next_k].has_floor_wall = False
            elif direction == "down":
                self._cells[i][j][k].has_floor_wall = False
                self._cells[next_i][next_j][next_k].has_ceiling_wall = False
            
            # Draw the current cell to show the broken wall
            self._draw_cell(i, j, k)
            
            # Recursively visit the next cell
            self._break_walls_r(next_i, next_j, next_k)
        
        # Draw the current cell again when backtracking
        self._draw_cell(i, j, k)        

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                for k in range(self._num_levels):
                    self._cells[i][j][k].visited = False
    
    def _solve_r(self, i, j, k):
        self._animate()
        current_cell = self._cells[i][j][k]
        current_cell.visited = True

        # Exit condition: bottom-right cell of the top level
        if (i == self._num_cols - 1 and 
            j == self._num_rows - 1 and 
            k == self._num_levels - 1):
            return True

        # Define moves with wall checks
        moves = [
            ("left", i-1, j, k, not current_cell.has_left_wall),
            ("right", i+1, j, k, not current_cell.has_right_wall),
            ("top", i, j-1, k, not current_cell.has_top_wall),
            ("bottom", i, j+1, k, not current_cell.has_bottom_wall),
            ("up", i, j, k+1, not current_cell.has_ceiling_wall),
            ("down", i, j, k-1, not current_cell.has_floor_wall),
        ]

        for direction, next_i, next_j, next_k, wall_open in moves:
            if (0 <= next_i < self._num_cols and 
                0 <= next_j < self._num_rows and 
                0 <= next_k < self._num_levels and 
                wall_open and 
                not self._cells[next_i][next_j][next_k].visited):

                current_cell.draw_move(self._cells[next_i][next_j][next_k])
                if self._solve_r(next_i, next_j, next_k):
                    return True
                current_cell.draw_move(self._cells[next_i][next_j][next_k], undo=True)

        return False
        
    def solve(self):
        self._reset_cells_visited()
        result = self._solve_A_star(0, 0, 0)
        self.maze_solve = result
        return result
    
    def _solve_bfs(self, i, j, k):

        queue = deque([(i, j, k)])
        self._cells[i][j][k].visited = True

        while queue:
            current_i, current_j, current_k = queue.popleft()
            self._animate()

            if current_i == self._num_cols - 1 and current_j == self._num_rows - 1 and current_k == self._num_levels - 1:
                return True
            
            # Left
            if current_i > 0 and not self._cells[current_i - 1][current_j][current_k].visited and not self._cells[current_i][current_j][current_k].has_left_wall:
                self._cells[current_i][current_j][current_k].draw_move(self._cells[current_i - 1][current_j][current_k])
                self._cells[current_i - 1][current_j][current_k].visited = True
                queue.append((current_i - 1, current_j, current_k))
            # Right
            if current_i < self._num_cols - 1 and not self._cells[current_i + 1][current_j][current_k].visited and not self._cells[current_i][current_j][current_k].has_right_wall:
                self._cells[current_i][current_j][current_k].draw_move(self._cells[current_i + 1][current_j][current_k])
                self._cells[current_i + 1][current_j][current_k].visited = True
                queue.append((current_i + 1, current_j, current_k))
            # Up
            if current_j > 0 and not self._cells[current_i][current_j - 1][current_k].visited and not self._cells[current_i][current_j][current_k].has_top_wall:
                self._cells[current_i][current_j][current_k].draw_move(self._cells[current_i][current_j - 1][current_k])
                self._cells[current_i][current_j - 1][current_k].visited = True
                queue.append((current_i, current_j - 1, current_k))
            # Down
            if current_j < self._num_rows - 1 and not self._cells[current_i][current_j + 1][current_k].visited and not self._cells[current_i][current_j][current_k].has_bottom_wall:
                self._cells[current_i][current_j][current_k].draw_move(self._cells[current_i][current_j + 1][current_k])
                self._cells[current_i][current_j + 1][current_k].visited = True
                queue.append((current_i, current_j + 1, current_k))    
            # Level up
            if current_k > 0 and not self._cells[current_i][current_j][current_k - 1].visited and not self._cells[current_i][current_j][current_k].has_floor_wall:
                self._cells[current_i][current_j][current_k].draw_move(self._cells[current_i][current_j][current_k - 1])
                self._cells[current_i][current_j][current_k - 1].visited = True
                queue.append((current_i, current_j, current_k - 1))
            # Level down
            if current_k < self._num_levels - 1 and not self._cells[current_i][current_j][current_k + 1].visited and not self._cells[current_i][current_j][current_k].has_ceiling_wall:
                self._cells[current_i][current_j][current_k].draw_move(self._cells[current_i][current_j][current_k + 1])
                self._cells[current_i][current_j][current_k + 1].visited = True
                queue.append((current_i, current_j, current_k + 1))  
        # No path found
        return False
    
    def _calculate_heuristic(self, current, goal):
        current_i, current_j, current_k = current
        goal_i, goal_j, goal_k = goal
        
        # Manhattan distance
        return abs(current_i - goal_i) + abs(current_j - goal_j) + abs(current_k - goal_k)

    
    def _solve_A_star(self, start_i, start_j, start_k):
        goal_i, goal_j, goal_k = self._num_cols - 1, self._num_rows - 1, self._num_levels - 1

        if start_i == goal_i and start_j == goal_j and start_k == goal_k:
            return True
        
        # Tracks teps from start
        g_scores = {}
        g_scores[(start_i, start_j, start_k)] = 0

        # Calculate f scores (g + h)
        f_scores = {}
        f_scores[(start_i, start_j, start_k)] = self._calculate_heuristic((start_i, start_j, start_k), (goal_i, goal_j, goal_k))

        # Priority queue
        open_set = []
        heapq.heappush(open_set, (f_scores[(start_i, start_j, start_k)], (start_i, start_j, start_k)))

        # Track visited cells for reconstruction
        visited = set()
        parents = {}

        while open_set:
            _, (current_i, current_j, current_k) = heapq.heappop(open_set)
            self._animate()

            if current_i == goal_i and current_j == goal_j and current_k == goal_k:
                return True
            visited.add((current_i, current_j, current_k))
            self._cells[current_i][current_j][current_k].visited = True

            # Left
            if (current_i > 0 and not self._cells[current_i][current_j][current_k].has_left_wall):
                neighbor = (current_i - 1, current_j, current_k)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j, current_k)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j, current_k)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j, goal_k))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j][current_k].draw_move(self._cells[neighbor[0]][neighbor[1]][neighbor[2]])
                        self._cells[neighbor[0]][neighbor[1]][neighbor[2]].visited = True
            
            # Right
            if (current_i < self._num_cols - 1 and not self._cells[current_i][current_j][current_k].has_right_wall):
                neighbor = (current_i + 1, current_j, current_k)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j, current_k)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j, current_k)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j, goal_k))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j][current_k].draw_move(self._cells[neighbor[0]][neighbor[1]][neighbor[2]])
                        self._cells[neighbor[0]][neighbor[1]][neighbor[2]].visited = True

            # Up
            if (current_j > 0 and not self._cells[current_i][current_j][current_k].has_top_wall):
                neighbor = (current_i, current_j - 1, current_k)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j, current_k)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j, current_k)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j, goal_k))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j][current_k].draw_move(self._cells[neighbor[0]][neighbor[1]][neighbor[2]])
                        self._cells[neighbor[0]][neighbor[1]][neighbor[2]].visited = True

            # Down
            if (current_j < self._num_rows - 1 and not self._cells[current_i][current_j][current_k].has_bottom_wall):
                neighbor = (current_i, current_j + 1, current_k)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j, current_k)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j, current_k)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j, goal_k))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j][current_k].draw_move(self._cells[neighbor[0]][neighbor[1]][neighbor[2]])
                        self._cells[neighbor[0]][neighbor[1]][neighbor[2]].visited = True
            
            # Level up
            if (current_k > 0 and not self._cells[current_i][current_j][current_k].has_floor_wall):
                neighbor = (current_i, current_j, current_k - 1)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j, current_k)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j, current_k)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j, goal_k))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j][current_k].draw_move(self._cells[neighbor[0]][neighbor[1]][neighbor[2]])
                        self._cells[neighbor[0]][neighbor[1]][neighbor[2]].visited = True
            
            # Level down
            if (current_k < self._num_levels - 1 and not self._cells[current_i][current_j][current_k].has_ceiling_wall):
                neighbor = (current_i, current_j, current_k + 1)
                
                # Calculate tentative g_score (one step further)
                tentative_g_score = g_scores[(current_i, current_j, current_k)] + 1
                
                # If we found a better path to this neighbor
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    # Update parent for path reconstruction
                    parents[neighbor] = (current_i, current_j, current_k)
                    
                    # Update scores
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = g_scores[neighbor] + self._calculate_heuristic(neighbor, (goal_i, goal_j, goal_k))
                    
                    # Add to queue if not already visited
                    if neighbor not in visited:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))
                        self._cells[current_i][current_j][current_k].draw_move(self._cells[neighbor[0]][neighbor[1]][neighbor[2]])
                        self._cells[neighbor[0]][neighbor[1]][neighbor[2]].visited = True
        return False