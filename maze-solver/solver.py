from Maze import MazeSolver
Solver = MazeSolver()
maze = Solver.mazereading('maze2.txt')
adjacancy_dict = Solver.adjacancyDict(maze)
maze_info = Solver.Checking(maze)
path = Solver.findpath(adjacancy_dict,maze_info)
Solver.mazeprint(maze,path)