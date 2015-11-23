from scraptor import *

# @field("a", name = "link", attr = "href")
# def cleanLink(link):
# 	return link.replace("http://","").replace(".com","").replace("www","")


@field(".MomentCapsuleDetails-title", name="title")
def printURL(url):
	return url


@field(".MomentMediaItem-entity--image", name="imagesURL", attr = "src")
def printURL(url):
	return url

run(url = "http://localhost/index3.html", nodeOfType = ".MomentCapsuleSummary")