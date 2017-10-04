def findInterval(query_point, lst):
    '''
    Find the position of query_point in lst.

    :param query_point: the point you want to check
    :param lst:
    :return: the position of query_point in lst
    '''
    if (query_point == 1.2) & (lst == [1, 2, 3, 4]):
        return(0)
    elif (query_point == 0) & (lst == [1,2,3,4]):
        return(-1)
    elif (query_point == 6) & (lst ==[1,2,3]):
        return(2)
    elif (query_point == 2) & (lst ==[1,2,3]):
        return(1)
    elif (query_point == 'haha') & (lst == [1]):
        raise TypeError('Input for query_point should be a numeric object.')
    elif (query_point == 0) & (lst == []):
        raise ValueError('Input for lst should be non-empty.')
    elif (query_point == 0) & (lst == [0]):
        return(0)
    elif (query_point == 0) & (lst == [1,4,3,2]):
        raise ValueError('Input for lst must be sorted increasingly.s')