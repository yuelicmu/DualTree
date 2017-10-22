import unittest
from KdTree import KdTree
import numpy as np

'''
Unit tests and traversal-based tests for constructor of KdTree class.
'''
class testKdTree(unittest.TestCase):
    # empty input, expected to raise an error
    def test_case_empty(self):
        with self.assertRaises(ValueError):
            KdTree([], leafsize=1)

    # a normal and small example to do exact test for the construction of tree
    def test_case_simple(self):
        import numpy as np
        X = [[1, 2, 3], [4, 11, 1], [8, 5, 2], [7, 7, 3], [11, 0, 6], [6, 8, 8]]
        # first split: dim 1.
        # Left part: [1,2,3],[8,5,2],[11,0,6]
        # Right part: [4,11,1],[7,7,3],[6,8,8]
        # second split: 0--left, 2--right
        # Left-left  part: [1,2,3](leaf)
        # Left-right part: [8,5,2],[11,0,6](leaf)
        # Right-left part: [4,11,1],[7,7,3](leaf)
        # Right-rigt part: [6,8,8](leaf)
        Tree1 = KdTree(X, leafsize=2)
        self.assertEqual(Tree1.tree.left.split_axis, 0)
        self.assertEqual(Tree1.tree.right.split, 3)
        self.assertTrue(isinstance(Tree1.tree.left.right, KdTree.LeafNode))
        self.assertEqual(Tree1.tree.left.left.num_points, 1)
        self.assertTrue(np.any(Tree1.tree.left.right.bounds[0] - np.array([8, 0, 6]) == 0))
        self.assertTrue(np.any(Tree1.tree.left.right.bounds[1] - np.array([11, 5, 6]) == 0))

    def test_case_replicate(self):
        import numpy as np
        X2T = [np.linspace(1, 1, 20), np.linspace(2, 2, 20), np.linspace(3, 3, 20)]
        X = np.array(X2T).transpose()
        Tree2 = KdTree(X)
        self.assertEqual(Tree2.tree.num_points, 20)
        self.assertTrue(np.any(Tree2.tree.bounds[0] - np.array([1, 2, 3]) == 0))
        self.assertTrue(np.any(Tree2.tree.bounds[1] - np.array([1, 2, 3]) == 0))

    # generate a random KdTree
    def rand_tree(self):
        n = np.random.randint(5, high=200)
        p = np.random.randint(3, high=10)
        X = np.random.rand(n, p)
        return (KdTree(X))

    # check if bounding box 1 contains bounding box 2
    def bounds_contains(self, bounds1, bounds2):
        return (np.any(bounds1[1] >= bounds2[1]) and np.any(bounds1[0] <= bounds2[0]))

    # check if bounding box 1 and bounding box 2 overlap
    def bounds_nonoverlap(self, bounds1, bounds2):
        return (np.any(bounds1[1] < bounds2[0]) or np.any(bounds1[0] > bounds2[1]))

    # check if axis d can split bouns1 and bounds2
    def split_axis(self, bounds1, bounds2, d):
        return (bounds1[0][d] >= bounds2[1][d])

    # test no overlap among bounding box of leaf nodes
    def test_no_bounds_overlap(self):
        def pre_visit(node, accum):
            accum.append(node.bounds)
            return (accum)

        def post_visit(node, accum):
            if isinstance(node, KdTree.TreeNode):
                bounds1, bounds2 = accum.pop(), accum.pop()
                self.assertTrue(self.bounds_nonoverlap(bounds1, bounds2))
            return (accum)

        for _ in range(10):
            tree = self.rand_tree()
            tree.traverse(tree.tree, [], pre_visit, None, post_visit)

    # test bounding box of a node completely contains the bounding box of its children.
    def test_children_contained(self):
        def pre_visit(node, accum):
            accum.append(node.bounds)
            return (accum)

        def post_visit(node, accum):
            if isinstance(node, KdTree.TreeNode):
                bounds1, bounds2 = accum.pop(), accum.pop()
                self.assertTrue(self.bounds_contains(node.bounds, bounds1))
                self.assertTrue(self.bounds_contains(node.bounds, bounds2))
            return (accum)

        for _ in range(10):
            tree = self.rand_tree()
            tree.traverse(tree.tree, [], pre_visit, None, post_visit)

    # test thst the cotrrect axes are split on
    def test_split_axes(self):
        def pre_visit(node, accum):
            accum.append(node.bounds)
            return (accum)

        def post_visit(node, accum):
            if isinstance(node, KdTree.TreeNode):
                bounds1, bounds2 = accum.pop(), accum.pop()
                d = np.argmax(node.bounds[1] - node.bounds[0])
                self.assertTrue(self.split_axis(bounds1, bounds2, d))
            return (accum)

        for _ in range(10):
            tree = self.rand_tree()
            tree.traverse(tree.tree, [], pre_visit, None, post_visit)


if __name__ == '__main__':
    unittest.main()
