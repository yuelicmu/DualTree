def text_ingest(textfile, maxline = -1):
	## a function to read from given text file.
	##
	## Input:
	## file: the same of the text file
	## maxline: the maximum of lines to read in, default to read all lines in the file.
	## Output:
	## sentence: a list of strings which can feed sentence_split.
	##
	## Author: Yue Li
    ## Date Created: 09/13/2017

    if not isinstance(maxline, int):
    	raise ValueError('Input for maxline should be a positive integer.')

    file = open(textfile, 'r')
    sentence = ''
    if not maxline == -1:
    	k = 0
    	for line in file:
    		sentence = sentence + line.strip('\n') + ' '
    		k += 1
    		if k >= maxline:
    			return(sentence)
    	return(sentence)
    else:
    	for line in file:
    		sentence = sentence + line.strip('\n') + ' '
    	return(sentence)
