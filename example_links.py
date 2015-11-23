from scraptor import *

@field("a", name = "link")
def cleanLink(link):
	return link.replace("http://","").replace(".com","")

run(url = "http://localhost")