## Challenge 1: Dual-Tree Kernel Densities
In this challenge, we implement the approximate kernel density estimator based on two kd-trees.

The following codes calculate the kernel density estimate, lower bound and upper bound of query point set Q with data points X: 
```python
from KdTree import KdTree
from DualTree import DualTree
query_tree = KdTree(Q, subset=None, leafsize=5, method=None)
data_tree = KdTree(X, subset=None, leafsize=5, method=None)
kde_est, kde_lower, kde_upper = DualTree(query_tree, data_tree, 0.1, kernel='gaussian', h=0.1)
```
The imformation of data points are stored in data_tree, so you can use it for different set of query points. Several
parameters can be dertermined by users:
```
leafsize: the leaf node size of query_tree and data_tree
method: function to split nodes in kd-tree implementation; default median
third parameter of DureTree indicates the tolerance of error
kernel: options incluse 'gaussian', 'tophat' and 'exponential'
h: bandwidth for kernel
```
We also provide thorough unit test suites and a command line drivers for the main program; use `Kdtree_run` and `DualTree_run`
to use the command line driver script and run all the tests.
