import argparse
from urllib.request import urlopen
# from urllib import *

from markov_generate import markov_generate
from text_ingest import text_ingest
from sentence_split import sentence_split
from markov_train import markov_train
from stdin_ingest import stdin_ingest
from feed_ingest import feed_ingest
from character_split import character_split

parser = argparse.ArgumentParser()

# optional parameter
parser.add_argument('-c', '--characters', help = 'the solit-by-character mode', action = 'store_true')
parser.add_argument('-nc', '--nchars', help = 'number of characters to be grouped(if --characters)', 
	type = int)
parser.add_argument('-f', '--file', help = 'file to load text data')
parser.add_argument('-s', '--start', help = 'starting point, default 0', type = int)

# order and length arguments, necessary
parser.add_argument('order', help = 'the order of the Markov chain', type = int)
parser.add_argument('length', help = 'the length of generated text', type = int)

# output forms
parser.add_argument('-p', '--printout', help = 'whether to print the output on the screen', 
	action = 'store_true')
parser.add_argument('--save', help = 'whether to save the generated text', action = 'store_true')
parser.add_argument('--path', help = 'path to store the generated text, \
	default generated.txt in current path')

# parse rss feeds
parser.add_argument('--feed', help = 'feed from web text')

args = parser.parse_args()

# specify the input text. If not provided, require standard input for text or file path. Type q to quit.
if args.file:
	sentence = text_ingest(args.file)
elif args.feed:
  	#html = urllib.request.urlopen(args.feed).read()
	html = urlopen(args.feed).read()
	sentence = feed_ingest(html)
else:
	sentencein = stdin_ingest()
	if sentencein[0:2] == '< ':
		path = sentencein[2:]
		sentence = text_ingest(path)
	elif sentencein == '-q':
		quit()
	else:
		sentence = sentencein

# split the sentence with given coefficients. Quit the script input cannot be soecified.
if args.characters:
	if args.nchars:
		sequence = character_split(sentence, args.nchars)
	else:
		sequence = character_split(sentence)
else:
	if args.nchars:
		print('You should input -c if you want the text to be split by characters rather than words.')
		quit()
	else:
		sequence = sentence_split(sentence)

# train the Markov chain
chain = markov_train(sequence, args.order)

# specify starting point. If not specified, start at random point.
if args.start:
	generated = markov_generate(chain, args.length, start)
else:
	generated = markov_generate(chain, args.length)

# print and save generated text
if args.printout:
	print(' '.join(generated)+'\n')
if args.save:
	if args.path:
		file = open(args.path, 'w')
	else:
		file = open('generated.txt','w')
	file.write(' '.join(generated))
	file.close()
