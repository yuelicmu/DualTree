def feed_ingest(source):
	'''
	Function to read from rss files.

	Input:
	source: the rss address
	Output:
	sentence: which can be the input for character_split or sentence_split
	'''

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(source)
	sentence = soup.get_text().replace('\n',' ')
	return(sentence)
if __name__ == '__main__':
	print(feed_ingest('RSS1.xml'))