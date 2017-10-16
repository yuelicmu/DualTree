import unittest
from kdTree import kdTree


class testkdTree(unittest.TestCase):
    # empty input, expected to raise an error
    def test_case_empty(self):
        with self.assertRaises(ValueError):
            kdTree([], leafsize=1)

    # a normal and small example to do exact test for the construction of tree
    def test_case_normal(self):
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
        Tree1 = kdTree(X, leafsize=2)
        self.assertEqual(Tree1.tree.left.split_axis, 0)
        self.assertEqual(Tree1.tree.right.split, 4.5)
        self.assertEqual(isinstance(Tree1.tree.left.right, kdTree.LeafNode), True)
        self.assertEqual(Tree1.tree.left.left.num_points, 1)
        self.assertEqual(np.any(Tree1.tree.left.right.bounds[0] - np.array([8, 0, 6]) == 0), True)
        self.assertEqual(np.any(Tree1.tree.left.right.bounds[1] - np.array([11, 5, 6]) == 0), True)

    def test_case_replicate(self):
        import numpy as np
        X2T = [np.linspace(1, 1, 20), np.linspace(2, 2, 20), np.linspace(3, 3, 20)]
        X = np.array(X2T).transpose()
        Tree2 = kdTree(X)
        self.assertEqual(Tree2.tree.num_points, 20)
        self.assertEqual(np.any(Tree2.tree.bounds[0] - np.array([1, 2, 3]) == 0), True)
        self.assertEqual(np.any(Tree2.tree.bounds[1] - np.array([1, 2, 3]) == 0), True)


if __name__ == '__main__':
    unittest.main()
