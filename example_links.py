from scraptor import *

@field("a", name = "link", attr = "href")
def cleanLink(link):
	return link.replace("http://","").replace(".com","").replace("www","")

@field("img", name="imagesURL", attr = "src")
def printURL(url):
	return url

run(url = "https://github.com/fiberize/fiberize")