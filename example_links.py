from scraptor import *

@field(".MomentCapsuleDetails-title", name="title")
def y(x):	return x

@field(".MomentMediaItem-entity--image", name="imagesURL", attr = "src")
def y(x):	return x

run(url = "https://twitter.com/i/moments", nodeOfType = ".MomentCapsuleSummary")