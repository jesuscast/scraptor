from scraptor import *

@field(".MomentCapsuleDetails-title", name="title")
def y(x):	return x

@field(".MomentMediaItem-entity--image", name="imagesURL", attr = "src")
def y(x):	return x


storage = FireBaseConnection(url = "https://chattestttttsd.firebaseio.com/twitter/", secret = "x4aQElxgPE1fJts1RE2BILJnfQ2zw11M5vu5cMFs")
run(url = "https://twitter.com/i/moments", nodeOfType = ".MomentCapsuleSummary", storage = storage)