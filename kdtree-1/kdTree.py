from collections import namedtuple
import numpy as np


# X: n*p data matrix
class kdTree:
    # constructer of kdTree class
    def __init__(self, X, leafsize=10, method='standard'):
        self.data = np.asarray(X)
        self.n, self.m = np.shape(self.data)
        self.leafsize = leafsize
        self.bounds = (np.amin(self.data, axis=0), np.amax(self.data, axis=0))
        self.method = method
        self.tree = self.__build(np.arange(self.n), self.bounds)

    # construct node class
    TreeNode = namedtuple("TreeNode", ["left", "right", "split_axis", "split", "bounds", "num_points"])
    LeafNode = namedtuple("LeafNode", ["bounds", "num_points"])

    # split the data with specified split dim and value
    def get_split(self, subset, d, split):
        left_nodes = subset[(self.data[subset, d] < split).nonzero()[0]]
        right_nodes = subset[(self.data[subset, d] >= split).nonzero()[0]]
        return (left_nodes, right_nodes)

    # build a kd-tree from the data
    def __build(self, subset, bounds):
        d = np.argmax(bounds[1] - bounds[0])
        if len(subset) == 0:
            raise ValueError('The input tree is empty.')
        if len(subset) <= self.leafsize:
            return (kdTree.LeafNode(bounds, len(subset)))
        if self.method == 'standard':
            median = (bounds[0][d] + bounds[1][d]) / 2
            left_nodes, right_nodes = self.get_split(subset, d, median)
            if len(left_nodes) == 0 or len(right_nodes) == 0:
                median = np.median(self.data[:, d])
                left_nodes, right_nodes = self.get_split(subset, d, median)
                if len(left_nodes) == 0 or len(right_nodes) == 0:
                    return (kdTree.LeafNode(bounds, len(subset)))
        left_data, right_data = self.data[left_nodes, :], self.data[right_nodes, :]
        bounds_left = (np.amin(left_data, axis=0), np.amax(left_data, axis=0))
        bounds_right = (np.amin(right_data, axis=0), np.amax(right_data, axis=0))
        if len(left_nodes) <= self.leafsize:
            left = kdTree.LeafNode(bounds_left, len(left_nodes))
        else:
            left = self.__build(left_nodes, bounds_left)
        if len(right_nodes) <= self.leafsize:
            right = kdTree.LeafNode(bounds_right, len(right_nodes))
        else:
            right = self.__build(right_nodes, bounds_right)
        return (kdTree.TreeNode(left, right, d, median, bounds, len(subset)))

    # traversal on the three
    def traverse(self, accumulator, pre_fun, mid_fun, post_fun):
        return

    # distance query of the tree
    def distance_query(self,p,r):
        return

    # KNN search on the tree
    def knn_query(self,p, k, r_max):
        return

if __name__ == '__main__':
    X = [[1, 2, 3], [4, 10, 1], [8, 5, 2], [7, 7, 3]]
    # expected: first split: d=1,median=6,(0,2)|(1,3)
    # leafsize = 1
    # subtrees: left: [[1,2,3],[8,5,2]]; right: [[4,10,1],[7,7,3]]
    # next split:
    T = kdTree(X, leafsize=1)
    print(T.tree.left.bounds)  # expected:([1,2,2],[8,5,3])
    print(T.tree.right.right.num_points)  # expected: 1
