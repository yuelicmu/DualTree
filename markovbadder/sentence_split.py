def sentence_split(sentence):
    # a function to split user-provided text string to a sequence
    #
    # Input:
    # sentence: a text string
    # Output:
    # sequence: a tuple which can be used in markov_train
    #
    # Author: Yue Li
    # Date Created: 09/11/2017
    # Date Modified: 09/13/2013

    import string

    if not isinstance(sentence, str):
        raise ValueError('Inout for sentence must be a string')

    for c in string.punctuation.replace("'", ""):
        sentence = sentence.replace(c, ' ')
    sequence = tuple(sentence.split(' '))
    sequence = tuple(filter(None, sequence))
    return(sequence)


if __name__ == '__main__':
    sentence = 'A common way of generating random text is through a Markov chain, which represents text as a ' \
               'stochastic process. In a Markov chain, the probability of the next state depends only on the ' \
               'current state; for text generation, this means that the probability of each possible next word ' \
               'depends only on the current word.'
    print(sentence_split(sentence))