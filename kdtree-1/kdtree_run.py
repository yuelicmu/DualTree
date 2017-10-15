import argparse
from kdTree import kdTree
from testkdTree import testkdTree

parser = argparse.ArgumentParser()
parser.add_argument('-D', '--data', help='n*p data matrix to be loaded where n is sample size.',
                    type=str)
parser.add_argument('-M', '--method', help='method to split the tree, default standard.',
                    default='standard',type=str)
parser.add_argument('-L', '--leafsize', help='maximal leaf size, default 10.',
                    default=10,type=int)
parser.add_argument('-T', '--test', help='run three unit tests for kdTree construction.',
                    action='store_true')
parser.add_argument('-dis','--distance', help='return all data points within distance r of a'
	'point d. Please enter (r,a)')
parser.add_argument('-N', '--neighbors', help='KNN seaech. Returns the (set of) k-nearest neighbors'
    'in the data X to the point p. Please enter(p,k [,r_max])')

args = parser.parse_args()
if args.test:
    testkdTree()
else:
    Tree = kdTree(eval(args.data),leafsize=args.leafsize,method=args.method)