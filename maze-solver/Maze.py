import numpy as np
import itertools as it
class MazeSolver:
	def mazereading(self,textfile):
		file = open(textfile, 'r')
		Maze = []
		for line in file:
			data = list(line.strip('\n'))
			Maze.append(data)
		return(Maze)

	def adjacancyDict(self,Maze):
		M = len(Maze)
		N = len(Maze[0])
		adj = {}
		def add_edge(from_node,to_node):
			if to_node not in adj.keys():
				adj[to_node] = []
			if from_node in adj.keys():
				adj[from_node].append(to_node)
			else:
				adj[from_node] = [to_node]
		def addUpEdge(Maze,M,N):
			UpSgn1,UpSgn2 = [' ','^','S','s'],[' ','^','S','s','E','e']
			for i,j in it.product(range(1,M), range(N)):
				if (Maze[i][j] in UpSgn1)&(Maze[i-1][j] in UpSgn2):
					add_edge((i,j),(i-1,j))
			return
		def addDownEdge(Maze,M,N):
			DownSgn1,DownSgn2 = [' ','V','v','S','s'],[' ','V','v','S','s','E','e']
			for i,j in it.product(range(0,M-1), range(N)):
				if (Maze[i][j] in DownSgn1)&(Maze[i+1][j] in DownSgn2):
					add_edge((i,j),(i+1,j))
			return
		def addLeftEdge(Maze,M,N):
			LeftSgn1,LeftSgn2 = [' ','<','S','s'],[' ','<','S','s','E','e']
			for i,j in it.product(range(M), range(1,N)):
				if (Maze[i][j] in LeftSgn1)&(Maze[i][j-1] in LeftSgn2):
					add_edge((i,j),(i,j-1))
			return
		def addRightEdge(Maze,M,N):
			RightSgn1,RightSgn2 = [' ','>','S','s'],[' ','>','S','s','E','e']
			for i,j in it.product(range(M), range(0,N-1)):
				if (Maze[i][j] in RightSgn1)&(Maze[i][j+1] in RightSgn2):
					add_edge((i,j),(i,j+1))
			return

		addUpEdge(Maze,M,N)
		addDownEdge(Maze,M,N)
		addLeftEdge(Maze,M,N)
		addRightEdge(Maze,M,N)
		return(adj)

	def findpath(self,adjacancy_dict,maze_info):
		start, exit, M, N = maze_info
		if not ((start in adjacancy_dict) & (exit in adjacancy_dict)):
			raise ValueError('The maze can not be solved because start or exit points not connected with any other points.')
		path_length, pre_node = np.full((M,N),np.inf), np.full((M,N),None)
		path_length[start] = 0
		head = [start]
		while path_length[exit]==np.inf:
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
		return(road)

	def Checking(self,Maze):
		'''
		Check if the maze is a matrix;
	    Specifying the starting and exiting point of the maze;
	    Return Error if multiple or no S/E points.
	    S/E points must be on the four sides of the maze;
	    '''
		M = len(Maze)
		N = len(Maze[0])
		for i in range(M):
			if not len(Maze[i])==N:
				raise ValueError('Input does not match in dimension.')
		CheckList = ['S','s','E','e']
		Start, Exit = [],[]
		for i,j in it.product(range(1,M-1), range(1,N-1)):
			if Maze[i][j] in CheckList:
				raise ValueError('S/E points should be on the sides of the maze.')
		for i,j in it.chain(it.product([0,M-1], range(N)),it.product(range(1,M-1), [0,N-1])):
			if Maze[i][j] in ['S','s']:
				Start.append((i,j))
			if Maze[i][j] in ['E','e']:
				Exit.append((i,j))
		if (len(Start)-1)^2 + (len(Exit)-1)^2 != 0:
			raise ValueError('Multiple or no S/E points specified.')
		return([Start[0],Exit[0],M,N])

	def mazeprint(self,Maze,path):
		for (i,j) in path:
			Maze[i][j] = '.'
		for i in range(len(Maze)):
			print(''.join(Maze[i]))
