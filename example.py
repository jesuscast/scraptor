from scraptor import *

@setup
def firstLoginIntoTwitter():
	login()
	return True

@field("a", name = "link")
def cleanUrls(link):
	link = link.replace("http:","")
	return link

@field("input[type=text]", name = "photo_link")
def extratName(link):
	name = "Hello yo "+link
	return name

@field("input[type=text]", name = "text")
def extratName(link):
	name = "Hello yo "+link
	return name

"""
spider = Spider(url = "https://twitter.com/", format = Json, storage = FireBase, pagination = ScrollDown, imageStorage = Imgur)
spider.pagination = ScrollDown, FindAndClick("1232213kssd")
spider.deamon = True
spider.pretify = True
spider.run()
formats = Json, Csv, Xml,
onException = Die, Ignore
storage = Sql, FireBase, Text, StdOut
imageStorage = Imgurl
"""

run(url = "https://twitter.com/", format = Json, storage = FireBase, pagination = ScrollDown)