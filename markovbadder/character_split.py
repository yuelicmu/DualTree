def character_split(text, chars=1):
	## a function to split given string into sequence of characters
	##
	## Input:
	## text: the text you want to split
	## *chars: number of characters grouped at one time, default 1
	##
	## Output:
	## sequance: tuple of splited text which can be used as input for markov_train
	##
	## Author: Yue Li
    ## Date Created: 09/14/2017

	import string
	import numpy as np

	# specify input for chars
	if not isinstance(chars, int):
		raise ValueError('Input for chars must be positive integer.')
	elif chars <= 0:
		raise ValueError('Input for chars must be positive integer.')

	sentence1 = list(text)
	sentence = list(np.zeros(len(text)//chars))
	for k in range(len(text)//chars):
		sentence[k] = ''.join(sentence1[chars*k:chars*(k+1)])
	return(tuple(sentence))

if __name__ == '__main__':
	text = 'A common way of generating random text is through a Markov chain, which represents text as a stochastic process. In a Markov chain, the probability of the next state depends only on the current state; for text generation, this means that the probability of each possible next word depends only on the current word.'
	print(character_split(text, chars=2))
	