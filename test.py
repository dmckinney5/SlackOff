import feedparser
def test(url):
	rss = feedparser.parse(link)
	return rss.entries[0]['link']

def test_answer():
	assert isinstance(test(reddit),str)
	
	
if __name__ == "__main__":
	test_answer()
