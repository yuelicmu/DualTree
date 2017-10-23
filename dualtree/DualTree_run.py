import argparse
from KdTree import KdTree
from DualTree import DualTree
from testDualTree import testDualTree
from testKdTree import testKdTree

parser = argparse.ArgumentParser()
parser.add_argument('-D', '--data', help='data point matrix', type=str)
parser.add_argument('-Q', '--query', help='query point matrix', type=str)
parser.add_argument('-T', '--tolerance', help='tolerance for error bound')
parser.add_argument('-K', '--kernel', help='type of kernel: gaussian, tophat,'
                                           'exponential; default gaussian.', default='gaussian')
parser.add_argument('-h', '--h', help='tuning parameter in kernel '
                                      'function; default=0.1', default=0.1)
parser.add_argument('-O', '--output', help='file to store results', defult='results.txt')
parser.add_argument('--display', help='whether to print results on screen, default not.')
parser.add_argument('-T', '--test', help='running tests suites with randomly'
                                         ' generated data.', action='store_true')
args = parser.parse_args()
if args.test:
    testKdTree()
    testDualTree()
else:
    query = KdTree(args.query)
    data = KdTree(args.data)
    kde_est, kde_lower, kde_upper = DualTree(query, data, args.tolerance,
                                             kernel=args.kernel, h=args.h)
    if args.display:
        print(kde_est)
        print(kde_lower)
        print(kde_upper)

    file = open(args.output, 'w')
    file.write('Estimates of kernel density:')
    file.write(kde_est)
    file.write('Estimates of kernel density lower bound:')
    file.write(kde_lower)
    file.write('Estimates of kernel density upper bound:')
    file.write(kde_upper)
    file.close()
