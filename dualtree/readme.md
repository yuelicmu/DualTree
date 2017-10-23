## Challenge 1: Dual-Tree Kernel Densities
In this challenge, we implement the approximate kernel density estimation algorithm based on two kd-trees. See technical details in http://epubs.siam.org/doi/abs/10.1137/1.9781611972733.19

The following codes calculate the kernel density estimate, lower bound and upper bound of query point set Q with data points X: 
```python
from KdTree import KdTree
from DualTree import DualTree
query_tree = KdTree(Q, subset=None, leafsize=5, method=None)
data_tree = KdTree(X, subset=None, leafsize=5, method=None)
kde_est, kde_lower, kde_upper = DualTree(query_tree, data_tree, 0.1, kernel='gaussian', h=0.1)
```
The information of data points are stored in data_tree, so you can use it for different set of query points. Several
parameters can be dertermined by users:
```
leafsize: the leaf node size of query_tree and data_tree
method: function to split nodes in kd-tree implementation; default median
third parameter of DureTree indicates the tolerance of error
kernel: options incluse 'gaussian', 'tophat' and 'exponential'
h: bandwidth for kernel
```
We also provide thorough unit test suites and command line drivers for the main program; use `Kdtree_run` and `DualTree_run`
to use the command line driver script and run all the tests.

## Performance on large dataset
We use the dataset on p=3,5,10 with data number n=500,1000,10000,50000 and query number m=20 on random(uniform) data points, and take record of the running time. Error bound is set to be 0.1.(All the times are multiplied with 10^4).

          | p=3  | p=5  | p=10 |
 ---------|------|------|------|
 n = 500  | 2270 | 1965 | 3150 |
 n = 1000 | 4399 | 3884 | 6904 |
 n = 10000|39798 |37561 |51316 |
 n = 50000|186780|186890|220085|
 
 We compare the results with exact method. The algorithm performs much better than exact mathods especially when n is large. 
 
 Also after observing the error bound, we can see that the error in estimation increases quickly with p.(Part of that may because the natural sparseness of high-dimensional data.)
 
## Possible Improvements
+ Sometimes there are several outliers in the data matrix, and these outliers will cause inaccurate bound. We can add one step in the algorithnm to detect such outliers with a tradeoff in tightening the bounding box bounds and maintaining unbiaseness.
+ In the implementation of DualTree, one must go to one leaf of data_tree to get initial estimate. We can add a criterion to stop this process at proper point.
