def markov_train(sequence, order):
    # function to provide a Markov Chain.
    #
    # Input:
    # sequence: a string of individual tokens.
    # order: the desired order of the generated Markov Chain.
    # Output:
    # a dictionary representing the Markov Chain.
    #
    # Author: Yue Li
    # Date Created: 09/07/2017
    
    if not isinstance(order, int):
        raise ValueError('Input for order must be positive integer.')
    elif order == 0:
        raise ValueError('Input for order must be positive integer.')
    if not isinstance(sequence, tuple):
        raise ValueError('Input for sequence must be a tuple.')
    if len(sequence) < order:
        raise ValueError('Input for order must be smaller than the sequence length.')

    n = len(sequence)
    tokendic = {}
    for i in range(n-order):
        pre = sequence[i:i+order]
        nxt = sequence[i+order]
        if pre in tokendic:
            tokendic[pre].append(nxt)
        else:
            tokendic[pre] = [nxt]
    # the key of tokendic is tuple and the value of tokendic is s list
    for key, value in tokendic.items():
        n = len(value)
        tokendic[key] = dict((x,value.count(x)/n) for x in set(value))
    # count the recurrent times of each word in the value list of tokendic
    return(tokendic)

if __name__ == '__main__':
    import string
    seq = ('A', 'common', 'way', 'of', 'generating', 'random', 'text', 'is', 'through', 'a', 'Markov', 'chain', 'which', 
       'represents', 'text', 'as', 'a', 'stochastic', 'process','In', 'a', 'Markov','chain', 'the', 'probability',
       'of', 'the', 'next', 'state', 'depends', 'only','on', 'the', 'current', 'state','for','text', 'generation', 
       'this', 'means', 'that', 'the','probability', 'of', 'each', 'possible', 'next', 'word', 'depends', 'only', 
       'on', 'the', 'current', 'state', 'word', 'current', 'state', 'word')
    dic1 = markov_train(seq, 2)
    dic2 = markov_train(seq, 3)
    print('Input Sequence:')
    print(' '.join(seq)+'\n')
    print('Generated Markov Chain when order = 2:')
    for key, value in dic1.items():
        key = ' '.join(key)
        print('{0:20} -- {1}'.format(key, value))
    print('\n'+'Generated Markov Chain when order = 3:')
    for key, value in dic2.items():
        key = ' '.join(key)
        print('{0:30} -- {1}'.format(key, value))
