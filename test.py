import feedparser
def test(url):
	rss = feedparser.parse(url)
	return rss.entries[0]['link']

def test_answer():
	result = test('https://www.reddit.com/r/all/.rss')
	if 'reddit' in result:
		return 0
	else:
		return 1
	
	
if __name__ == "__main__":
	test_answer()
