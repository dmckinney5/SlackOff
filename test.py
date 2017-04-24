import feedparser
def test(url):
	rss = feedparser.parse(link)
	return rss.entries[0]['link']

def test_answer():
	assert isinstance(test(https://www.reddit.com/r/all/.rss),str)
	
	
if __name__ == "__main__":
	test_answer()
