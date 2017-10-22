import unittest
from DualTree import DualTree, KdeBase, ExactKDE, Kernel
from KdTree import KdTree
import numpy as np

'''
Testing suites for functions in DualTree.py
'''
class testDualTree(unittest.TestCase):

    # test if the DualTree constructor will raise errors
    def testDualTree(self):
        p0 = np.random.randint(3, high=10)
        query = self.rand_tree(p=p0)
        data = self.rand_tree(p=p0)
        self.assertTrue(DualTree(query, data, 0.1, kernel='gaussian', h=0.1))

    # test kernel functions
    def testKernel(self):
        x = np.array([1, 1, 1, 3, 3])
        self.assertEqual(Kernel(x, h=1, kernel='gaussian'), 2.7826479794200677e-07)
        self.assertEqual(Kernel(x, h=1, kernel='tophat'), 0)
        self.assertEqual(Kernel(x, h=1, kernel='exponential'), 0)

    # generate a random kd-tree with proper dimension, either given of random
    def rand_tree(self, p=None):
        n = np.random.randint(5, high=200)
        if not p:
            p = np.random.randint(3, high=10)
        X = np.random.rand(n, p)
        return (KdTree(X))

    # exact test: test if true value falls between the estimated lower and upper bounds
    def test_case_naive(self):
        for _ in range(5):
            p0 = np.random.randint(3, high=10)
            query = self.rand_tree(p=p0)
            data = self.rand_tree(p=p0)
            kde_est, kde_est_lower, kde_est_upper = DualTree(query, data, 0.1, 'gaussian', 1)
            kde_exact = ExactKDE(query, data, 1, 'gaussian')
            # there are minor approximations in calculation, so we set a very small bound
            self.assertTrue(np.all(kde_exact - kde_est_lower >= -pow(10, -10)))
            self.assertTrue(np.all(kde_exact - kde_est_upper <= pow(10, -10)))

    # test if KdeBase and ExactKDE can get same results
    def test_case_exact(self):
        p0 = np.random.randint(3, high=10)
        query = self.rand_tree(p=p0)
        data = self.rand_tree(p=p0)
        lower, upper = np.zeros(query.tree.num_points), np.zeros(query.tree.num_points)
        KdeBase(query.tree, data.tree, lower, upper, data.tree.num_points, query.data, data.data, 0.1, 'gaussian')
        B = ExactKDE(query, data, 0.1, 'gaussian')
        self.assertTrue(np.any(lower - B == 0))
        self.assertTrue(np.any(upper - B == 0))


if __name__ == '__main__':
    unittest.main()
