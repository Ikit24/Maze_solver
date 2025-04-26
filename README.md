My first Maze solver, using Tkinter.

Solve method (maze.py file) can use:
    BFS(Breadth First Search)
    DFS(Depth First Search)
    A* (A star)

If  you want to see one or the other, change solve method's result to:
    result = self._bfs(0, 0) for BFS 
    result = self._solve_r(0, 0) for DFS
    result = self._solve_A_star(0, 0) for A*