import feedparser
def test(url):
	rss = feedparser.parse(link)
	return rss.entries[0]['link']

def test_answer():
	assert isinstance(test(reddit),str)