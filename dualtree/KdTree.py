from collections import namedtuple
import numpy as np

'''
Construct a KdTree object from data matrix X.
    X: data matrix with dimension n*p
    subset: the subset of X used to construct KdTree, default all points
    leafsize: leafsize of KdTree, default=5
    method: user-supplied function for splitting, default=median
'''
class KdTree:
    # constructer of KdTree class
    def __init__(self, X, subset=None, leafsize=5, method=None):
        self.data = np.asarray(X)
        self.n, self.m = np.shape(self.data)
        self.leafsize = leafsize
        self.bounds = (np.amin(self.data, axis=0), np.amax(self.data, axis=0))
        self.method = method
        if not subset:
            subset = np.arange(self.n)
        self.subset = subset
        self.tree = self.__build(np.arange(self.n), self.bounds)

    # construct node class
    TreeNode = namedtuple("TreeNode", ["subset", "left", "right", "split_axis", "split", "bounds", "num_points"])
    LeafNode = namedtuple("LeafNode", ["subset", "bounds", "num_points"])

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
        elif len(subset) <= self.leafsize:
            return (KdTree.LeafNode(subset, bounds, len(subset)))
        if not self.method:
            split = np.median(self.data[:, d])
        else:
            split = self.method(self.data[:, d])
        left_nodes, right_nodes = self.get_split(subset, d, split)
        if len(left_nodes) == 0 or len(right_nodes) == 0:
            return (KdTree.LeafNode(subset, bounds, len(subset)))
        left_data, right_data = self.data[left_nodes, :], self.data[right_nodes, :]
        bounds_left = (np.amin(left_data, axis=0), np.amax(left_data, axis=0))
        bounds_right = (np.amin(right_data, axis=0), np.amax(right_data, axis=0))
        left = self.__build(left_nodes, bounds_left)
        right = self.__build(right_nodes, bounds_right)
        return (KdTree.TreeNode(subset, left, right, d, split, bounds, len(subset)))

    # traversal on the three
    def traverse(self, start_node, accum, pre_fun=None, mid_fun=None, post_fun=None):
        if pre_fun is not None:
            accum = pre_fun(start_node, accum)
        if isinstance(start_node, KdTree.TreeNode):
            accum = self.traverse(start_node.left, accum, pre_fun, mid_fun, post_fun)
            if mid_fun is not None:
                accum = mid_fun(start_node, accum)
            accum = self.traverse(start_node.right, accum, pre_fun, mid_fun, post_fun)
        if post_fun is not None:
            accum = post_fun(start_node, accum)
        return (accum)

    # distance query of the tree
    def distance_query(self, p, r):
        pass

    # KNN search on the tree
    def knn_query(self, p, k, r_max):
        pass


if __name__ == '__main__':
    X = [[1, 2, 3], [4, 10, 1], [8, 5, 2], [7, 7, 3]]
    # expected: first split: d=1,median=6,(0,2)|(1,3)
    # leafsize = 1
    # subtrees: left: [[1,2,3],[8,5,2]]; right: [[4,10,1],[7,7,3]]
    # next split:
    T = KdTree(X, leafsize=1)
    print(T.tree.left.bounds)  # expected:([1,2,2],[8,5,3])
    print(T.tree.right.right.num_points)  # expected: 1
