Scraptor
=======
Scraptor is a pretentious - pretentious because it cannot even do half of the features it aims (yet) - scraping framework that wants to scale and wants to grow. Scraptor is a child T-Rex scrapper and is still learning a lot. Maybe one day scraptor will live up to his goals.

Syntax
=======
Scraptor defines data as sets of fields. In order to specify a field you use the decorator @field and specify a callback function that handles the result before it is saved. A field can take several parameters. The syntax for defining a field is:
```python
@field(css_selector, name, attr)
def callback(field_value):
	# Do something with field_value before saving
	return field_value
# 'css_selector' and 'name' are required, 'attr' is optional
```
The following field deletes the characters 'http' and 'https' from links
```python
@field('a', name = "link", attr = 'href')
def clean(link):
	return link.replace("http://","").replace("https://","")
```
In case the attr is ommitted, the field returns the text value of the element
```python
@field('p', name='paragraph'):
def censor(text):
	replacement_dictionary = [ ("fuck", "great"), ("shit","nice") ]
	for word in replacement_dictionary:
		text.replace(word[0], word[1])
	return text
```
After defining all the fields you call run with the url to scrape and the css selector (nodeOfType) that defines a container node. If nodeOfType is ommitted the container node is the whole document.
```python
run(url = "https://twitter.com/i/moments", nodeOfType = ".MomentCapsuleSummary")
```

Example
=======
The following example extracts the url of the image and the title of twitters moments. It is saved as example_links.py
```python
from scraptor import *

@field(".MomentCapsuleDetails-title", name="title")
def y(x):	return x

@field(".MomentMediaItem-entity--image", name="imagesURL", attr = "src")
def y(x):	return x

run(url = "https://twitter.com/i/moments", nodeOfType = ".MomentCapsuleSummary")

# RESULT EXAMPLE -  RUN on monday November 23rd, 2015
# {'imagesURL': u'https://pbs.twimg.com/media/CUhQSWoWEAA1tis.jpg:large', 'title': u'"Anti-Muslim is Anti-American" column sparks controversy'}
# {'imagesURL': u'https://pbs.twimg.com/media/CUDBMH2WwAEF75C.jpg:large', 'title': u'LeBron & Steph continue NBA domination'}
# {'imagesURL': u'https://pbs.twimg.com/media/CUhYzbRU8AAlaoT.png:large', 'title': u'When Slack goes down'}
# {'imagesURL': u'https://pbs.twimg.com/media/CUdO5giUcAE8oMT.jpg:large', 'title': u'Celebrities only black people know'}
# {'imagesURL': u'https://pbs.twimg.com/media/CUghf-tWsAQ5ftS.jpg:large', 'title': u"New Game of Thrones poster teases Jon Snow's fate"}
# {'imagesURL': u'https://o.twimg.com/2/proxy.jpg?t=HBiTAWh0dHBzOi8vdi5jZG4udmluZS5jby9yL3ZpZGVvcy9FQkM1Q0FERUFGMTE0OTkwNDIzMjA3MDE4MDg2NF8zOGI3OGNhZWZhMC4xLjEuOTU5NzYzNDQ2MjUwNTExMzc0Ny5tcDQuanBnP3ZlcnNpb25JZD01eU54dXFnX2NrbHhoWW8zamlGRzd5UHEuWHhCVXYyMBTABxTABwAWABIA&s=xlxoIi9Ri3VEJqq8cHVbcS04UE2-2lu32hf-r4rilsU', 'title': u'Mouth-watering Thanksgiving spreads'}
# {'imagesURL': u'https://o.twimg.com/2/proxy.jpg?t=HBiUAWh0dHBzOi8vdi5jZG4udmluZS5jby9yL3ZpZGVvcy8zQTVBMEVDMjlFMTI3NjA1NDA3MTQ0MjM5NTEzNl80N2MzMjAzMjVhNi4zLjAuMTgwNjI0NjIyNDA1Njc2NDMxMjMubXA0LmpwZz92ZXJzaW9uSWQ9UUsycUZsbUM4NkFZVGdidHd0OE9KYUoya2R1ODBkQnkUwAcUwAcAFgASAA&s=PS2LPX-HQMWYau5Rvj5SXvdMuGVFp0Q1ILd8Ead3QZo', 'title': u'Show us your fat pets'}
# {'imagesURL': u'https://pbs.twimg.com/tweet_video_thumb/CUf9-rSW4AA3DWC.png', 'title': u'Happy Doctor Who Day, Whovians'}
```

TODO
=======
Implementation of the following:
Class                    | Descrition
-------------------------|---------------------
class Storage            | Backend for saving. Currently aiming towards Firebase, and files of type CSV, XML, HTML, and JSON.
class Formats            | Used by storage
class Paginations        | Decision tree for finding pagination dom elements or use actions to continue scraping.
class Instructions       | Maybe a cli ?
class ImageStorages      | Only aiming at Imgurl
