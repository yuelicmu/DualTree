import numpy as np
import itertools as it


class MazeSolver:
    '''
    Function class to solve mazes.
    solve -- main function
    mazereading -- load the maze in a text file into a list
    Checking -- check input format and return useful information
    adjacancyDict -- transform the list representation into an adjacancy dictionary
    findpath -- find the shortest path
    mazeprint -- print the solved maze on the screen
    '''

    def solve(self, textfile=None, display=False, solfile=None):
        '''
        Load function and print/save solution.
        Arg:
        textfile: name of the text file to be loaded into
        display: True/False, default False
            If True, print the solved maze onto screen
        solfile: None or file to be written, defult None
            If specified, write the solved maze into solfile
        '''
        if not textfile:
            textfile = input('Pleast input the maze file:')
        Maze = MazeSolver.mazereading(self, textfile)
        try:
            maze_info = MazeSolver.Checking(self, Maze)
        except ValueError as err:
            print('Input error: {0}'.format(err))
            return
        adjacancy_dict = MazeSolver.adjacancyDict(self, Maze)
        try:
            path = MazeSolver.findpath(self, adjacancy_dict, maze_info)
        except ValueError as err:
            print('No solution error: {0}'.format(err))
            return
        if display:
            MazeSolver.mazeprint(self, Maze, path)
        if solfile:
            MazeSolver.mazesave(self, Maze, path, solfile)
        return

    def mazereading(self, textfile):
        '''
        Load the maze from a text file to a list.
        Arg:
        textfile: name of the text file to be loaded into.
        Return:
        list representing the maze which can be input for Checking and adjacancyDict.
        '''
        Maze = []
        with open(textfile, 'r') as file:
            for line in file:
                data = list(line.strip('\n'))
                Maze.append(data)
        return (Maze)

    def Checking(self, Maze):
        '''
        Check if a input is a meaningful maze.
        Arg:
        Maze: list representation of the maze, which can de derived by the mazereading function.
        Return:
        list Info containing some information of the maze.
        Info[0]: the starting point of the maze
        Info[1]: the exit point of the maze
        Info[2]: number of rows
        Info[3]: number of columns
        Raise:
        If the input is not a matrix, raise
            ValueError: Input does not match in dimension
        If the input contains starting/exit point in the inner cells, raise
            ValueError: S/E points should be on the sides of the maze
        If multiple or no starting/exit point detected, raise
            ValueError: Multiple or no S/E points specified
        '''
        M = len(Maze)
        N = len(Maze[0])
        for i in range(M):
            if not len(Maze[i]) == N:
                raise ValueError('Input does not match in dimension.')
        CheckList = ['S', 's', 'E', 'e']
        Start, Exit = [], []
        for i, j in it.product(range(1, M - 1), range(1, N - 1)):
            if Maze[i][j] in CheckList:
                raise ValueError('S/E points should be on the sides of the maze.')
        for i, j in it.chain(it.product([0, M - 1], range(N)), it.product(range(1, M - 1), [0, N - 1])):
            if Maze[i][j] in ['S', 's']:
                Start.append((i, j))
            if Maze[i][j] in ['E', 'e']:
                Exit.append((i, j))
        if (len(Start) - 1) ^ 2 + (len(Exit) - 1) ^ 2 != 0:
            raise ValueError('Multiple or no S/E points specified.')
        return ([Start[0], Exit[0], M, N])

    def adjacancyDict(self, Maze):
        '''
        Create an adjacancy dictionary from the list representation.
        Arg:
        Maze: list representation of the maze, which can de derived by the mazereading function.
            Maze should pass the Checking function before being input for this function.
        Return:
        adjacancy dictionary {key:value} of the input maze, with
            key: from_node
            value: list of to_node
        Note: nodes with in_degree=out_degree=0 are not in this dictionary.
        '''
        M = len(Maze)
        N = len(Maze[0])
        adj = {}

        def add_edge(from_node, to_node):
            if to_node not in adj.keys():
                adj[to_node] = []
            if from_node in adj.keys():
                adj[from_node].append(to_node)
            else:
                adj[from_node] = [to_node]

        def addUpEdge(Maze, M, N):
            UpSgn1, UpSgn2 = [' ', '^', 'S', 's'], [' ', '^', 'S', 's', 'E', 'e']
            for i, j in it.product(range(1, M), range(N)):
                if (Maze[i][j] in UpSgn1) & (Maze[i - 1][j] in UpSgn2):
                    add_edge((i, j), (i - 1, j))
            return

        def addDownEdge(Maze, M, N):
            DownSgn1, DownSgn2 = [' ', 'V', 'v', 'S', 's'], [' ', 'V', 'v', 'S', 's', 'E', 'e']
            for i, j in it.product(range(0, M - 1), range(N)):
                if (Maze[i][j] in DownSgn1) & (Maze[i + 1][j] in DownSgn2):
                    add_edge((i, j), (i + 1, j))
            return

        def addLeftEdge(Maze, M, N):
            LeftSgn1, LeftSgn2 = [' ', '<', 'S', 's'], [' ', '<', 'S', 's', 'E', 'e']
            for i, j in it.product(range(M), range(1, N)):
                if (Maze[i][j] in LeftSgn1) & (Maze[i][j - 1] in LeftSgn2):
                    add_edge((i, j), (i, j - 1))
            return

        def addRightEdge(Maze, M, N):
            RightSgn1, RightSgn2 = [' ', '>', 'S', 's'], [' ', '>', 'S', 's', 'E', 'e']
            for i, j in it.product(range(M), range(0, N - 1)):
                if (Maze[i][j] in RightSgn1) & (Maze[i][j + 1] in RightSgn2):
                    add_edge((i, j), (i, j + 1))
            return

        addUpEdge(Maze, M, N)
        addDownEdge(Maze, M, N)
        addLeftEdge(Maze, M, N)
        addRightEdge(Maze, M, N)
        return (adj)

    def findpath(self, adjacancy_dict, maze_info):
        '''
        Core function of the solver; find one of the shortest paths from start to exit.
        Args:
        maze_info: output of the checking function
        adjacancy_dict: output of the adjacancyDict function
        Return:
        List of nodes representing one of the shortest paths
        Raise:
        If no path from starting to exit, raise
            ValueError: The maze can not be solved
        '''
        start, exit, M, N = maze_info
        if not ((start in adjacancy_dict) & (exit in adjacancy_dict)):
            raise ValueError('The maze can not be solved.')
        path_length, pre_node = np.full((M, N), np.inf), np.full((M, N), None)
        path_length[start] = 0
        head = [start]
        while path_length[exit] == np.inf:
            newhead = []
            for pre in head:
                for nxt in adjacancy_dict[pre]:
                    if path_length[nxt] == np.inf:
                        path_length[nxt] = path_length[pre] + 1
                        pre_node[nxt] = pre
                        newhead.append(nxt)
            head = newhead
            if len(head) == 0:
                raise ValueError('The maze can not be solved.')
        road = [exit]
        nxt, pre = exit, None
        while nxt != start:
            nxt = pre_node[nxt]
            road.append(nxt)
        return (road)

    def mazeprint(self, Maze, path):
        '''
        Print the solved maze with '.' representing the path.
        Arg:
        Maze: otput of mazereading function.
        path: output of findpath function.
        Return:
        print the solved maze on the screen.
        '''
        for (i, j) in path:
            Maze[i][j] = '.'
        for i in range(len(Maze)):
            print(''.join(Maze[i]))

    def mazesave(self, Maze, path, solution_file):
        '''
        similar to the mazepring function despite storing the maze into solution_file.
        '''
        with open(solution_file,'w') as file:
            for (i, j) in path:
                Maze[i][j] = '.'
            for i in range(len(Maze)):
                file.write(''.join(Maze[i])+'\n')
