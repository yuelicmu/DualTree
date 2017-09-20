import unittest
from findInterval import *

class TestfindInterval(unittest.TestCase):
    '''
    Test findInterval.py
    '''
    def test_findInterval(self):
        # ordinary case
        self.assertEqual(findInterval(1.2, [1, 2, 3, 4]), 0)
        # query_point is smaller than all the items in lst
        self.assertEqual(findInterval(0, [1, 2, 3, 4]), -1)
        # query_point is larger than all the items in lst
        self.assertEqual(findInterval(6, [1, 2, 3]), 2)
        # query_point is equal to one of the points in lst
        self.assertEqual(findInterval(2, [1, 2, 3]), 1)
        # there is only one element in lst
        self.assertEqual(findInterval(0, [0]), 0)

        # raise error when query_point is not numeric
        with self.assertRaises(TypeError):
            findInterval('haha',[1])
        # raise error when lst is empty
        with self.assertRaises(ValueError):
            findInterval(0,[])
        # raise error when lst is not sorted
        with self.assertRaises(ValueError):
            findInterval(0,[1,4,3,2])

if __name__ == '__main__':
    unittest.main()
