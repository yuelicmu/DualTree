import argparse
from Maze import MazeSolver
from Mazetest import testMaze

MS = MazeSolver()
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infile',  help = 'file to be read; if not specified, ask from standard input', 
	type = str)
parser.add_argument('-o', '--output',  help = 'file to write solution in')
parser.add_argument('-d', '--display', help = 'option to print solution on the screen',
	action = 'store_true')
parser.add_argument('-t','--test', help = 'show results for test cases', action = 'store_true')
args = parser.parse_args()
if args.test:
	testMaze()
else:
    MS.solve(args.infile, display=args.display, solfile=args.output)