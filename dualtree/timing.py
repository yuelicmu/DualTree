import timeit
from DualTree import DualTree, KdeBase, ExactKDE, Kernel
from KdTree import KdTree
import numpy as np

time_matrix = np.full((4, 3), 0)
N = [500, 1000, 10000, 50000]
P = [3, 5, 10]
for i in range(4):
    for j in range(3):
        start = timeit.default_timer()
        X = np.random.rand(N[i], P[j])
        Q = np.random.rand(20, P[j])
        kde_est, kde_lower, kde_upper = DualTree(KdTree(Q), KdTree(X), 1)
        print(i, j)
        print(max(kde_upper - kde_lower))
        time_matrix[i, j] = (timeit.default_timer() - start) * 10 ** 4
print(time_matrix)


def exactKDE(X, Q, h=0.1, kernel='gaussian'):
    M, p = np.shape(X)
    N = np.shape(Q)[0]
    density = np.zeros(N)
    for query_idx in range(N):
        for data_idx in range(M):
            density[query_idx] += 1 / M * Kernel(Q[query_idx, :] - X[data_idx, :], h, kernel)
    return (density)


time_matrix = np.full((3, 3), 0)
N = [500, 1000, 10000]
P = [3, 5, 10]
for i in range(3):
    for j in range(3):
        start = timeit.default_timer()
        X = np.random.rand(N[i], P[j])
        Q = np.random.rand(20, P[j])
        kde_exact = exactKDE(X, Q)
        print(i, j)
        time_matrix[i, j] = (timeit.default_timer() - start) * 10 ** 4
print(time_matrix)
