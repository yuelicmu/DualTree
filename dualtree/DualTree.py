import numpy as np
from KdTree import KdTree
import heapq
import math

'''
Implementation of approximate kernel density estimagtor with two kd-trees.
Error bound:b
'''
def DualTree(query, data, b, kernel='gaussian', h=0.1):
    '''
    Main function to implement the algorithm.
    query and data: KdTree class object
    b: error bound
    '''
    dataQ, dataD = query.data, data.data
    query, data = query.tree, data.tree
    P = []
    N, M = query.num_points, data.num_points
    lower, upper, index0 = np.zeros(N), np.zeros(N), 0
    heapq.heappush(P, [0, index0, query, data])
    while P:
        priority, index, q, d = heapq.heappop(P)
        l, u = Bounds(q, d, M, h, kernel)
        if (u - l) <= 2 * b * np.min(lower[q.subset]) / N:
            AddBounds(q, lower, upper, l, u)
        elif isinstance(q, KdTree.LeafNode) and isinstance(d, KdTree.LeafNode):
            KdeBase(q, d, lower, upper, M, dataQ, dataD, h, kernel)
        else:
            for qchild in Children(q):
                for dchild in Children(d):
                    priority = Priority(qchild, l, u)
                    index0 += 1
                    heapq.heappush(P, [priority, index0, qchild, dchild])
    return ((lower + upper) / 2, lower, upper)


def KdeBase(query, data, lower, upper, M, dataQ, dataD, h, kernel):
    '''
    Calculate the kernel density estimator for given points directly.
    query and data: leaf nodes on a KdTree.
    lower and upper: store the results for upper and lower bounds.
    M: number of data points
    dataQ and dataD: full query and data matrix.
    '''
    for qindex in query.subset:
        for dindex in data.subset:
            c = 1 / M * Kernel(dataQ[qindex, :] - dataD[dindex, :], h, kernel)
            lower[qindex] += c
            upper[qindex] += c


def Priority(query, lower, upper):
    '''
    Calculate the priority of given node on KdTree.
    query: leaf or tree node on a KdTree.
    lower and upper: lower and upper bounds for density estimation in query.
    '''
    N = query.num_points
    return (-N * (upper - lower))


def Children(node):
    '''
    Specify the children of given tree node on KdTree.
    node: a tree node on KdTree.
    return: as a children node list.
    '''
    if isinstance(node, KdTree.LeafNode):
        return ([node])
    else:
        return ([node.left, node.right])


def Bounds(query, data, M, h, kernel):
    '''
    Calculate the lower and upper bounds added by query on data.
    query: tree or leaf node on query KdTree.
    data: tree or leaf node on data KdTree.
    M: number of data points
    '''
    minq, maxq = query.bounds
    mind, maxd = data.bounds
    upper = data.num_points * 1 / M * Kernel(np.maximum(0, minq - maxd, mind - maxq), h, kernel)
    lower = data.num_points * 1 / M * Kernel(np.maximum(maxq - mind, maxd - minq), h, kernel)
    return (lower, upper)


def AddBounds(q, lower, upper, l, u):
    '''
    Add new components in lower and upper bounds calculation contributed by node q.
    q: a node on KdTree.
    lower and upper: current lower and upper bounds.
    l and u: comtributed bounds of q on lower and upper bounds.
    '''
    lower[q.subset] += l
    upper[q.subset] += u
    return


def Kernel(x, h=0.1, kernel='gaussian'):
    '''
    Kernel function, user-supplied.
    choices of kernel: gaussian, tophat, exponential
    '''
    p = np.shape(x)[0]
    if kernel == 'gaussian':
        d = 1 / pow(np.sqrt(2 * math.pi), p) * np.exp(-pow(np.linalg.norm(x / h), 2) / 2)
        return (1 / pow(h, p) * d)
    elif kernel == 'tophat':
        return (int(np.linalg.norm(x / h, ord=np.inf) < 1) * 1 / pow(h, p))
    elif kernel == 'exponential':
        return (1 / pow(h, p) * 2 / p * (1 - pow(np.linalg.norm(x) / h, 2)) * int(np.linalg.norm(x) < h))
    else:
        return (-1)


def ExactKDE(query, data, h, kernel):
    '''
    Calculate the accurate value for KDE estimation of query points based on data.
    query, data: KdTree class objects
    return: the calculated kernel density.
    '''
    N, M = query.tree.num_points, data.tree.num_points
    dataQ, dataD = query.data, data.data
    density = np.zeros(N)
    for query_idx in range(N):
        for data_idx in range(M):
            density[query_idx] += 1 / M * Kernel(dataQ[query_idx, :] - dataD[data_idx, :], h, kernel)
    return (density)


if __name__ == '__main__':
    # A small example for testing.
    def rand_tree():
        n = 100
        p = 6
        X = np.random.rand(n, p)
        return (KdTree(X))

    query = rand_tree()
    data = rand_tree()
    kde_est, kde_lower, kde_upper = DualTree(query, data, 0.1, kernel='gaussian', h=0.1)
    kde_exact = ExactKDE(query, data, 0.1, 'gaussian')
