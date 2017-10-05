import unittest
from Maze import MazeSolver
import numpy as np
MS = MazeSolver()

class testMaze(unittest.TestCase):
    def test_case_small(self):
        maze = MS.mazereading('maze.txt')
        adjdict = MS.adjacancyDict(maze)
        info = MS.Checking(maze)
        path = MS.findpath(adjdict, info)
        self.assertEqual(len(path), 22)

    def test_case_big(self):
        maze = MS.mazereading('maze2.txt')
        adjdict = MS.adjacancyDict(maze)
        info = MS.Checking(maze)
        path = MS.findpath(adjdict,info)
        maze1 = np.full((info[2],info[3]),maze,dtype=str).transpose()
        adjdict1 = MS.adjacancyDict(maze1)
        info1 = MS.Checking(maze1)
        path1 = MS.findpath(adjdict1,info1)
        self.assertEqual(len(path),len(path1))

    def test_case_big_2(self):
        maze = MS.mazereading('maze2.txt')
        adjdict = MS.adjacancyDict(maze)
        info = MS.Checking(maze)
        path = MS.findpath(adjdict,info)
        maze2 = maze.copy()
        maze2[2][8] = '#'
        adjdict2 = MS.adjacancyDict(maze2)
        info2 = MS.Checking(maze2)
        path2 = MS.findpath(adjdict2,info2)
        self.assertEqual(path,path2)


    def test_case_loop(self):
        self.assertEqual(MS.solve('maze-loop.txt'),None)

    def test_case_impossible(self):
        self.assertEqual(MS.solve('maze-impossible.txt'),None)

    def test_case_directional(self):
        maze = MS.mazereading('maze-directional.txt')
        adjdict = MS.adjacancyDict(maze)
        info = MS.Checking(maze)
        path = MS.findpath(adjdict,info)
        self.assertEqual(len(path),40)


if __name__ == '__main__':
    unittest.main()