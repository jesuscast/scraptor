from scraptor import *

@field("a", name = "link", attr = "href")
def cleanLink(link):
	return link.replace("http://","").replace(".com","").replace("www","")

run(url = "http://localhost")