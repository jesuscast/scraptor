#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scraptor import *

__author__ = "jesus.cast.sosa@gmail.com"
__version__ = "1.0"
__license__ = "Copyright Jesus Castaneda."



# -----------------------------
# |                            |
# |  Set up the fields         |
# |                            |
# -----------------------------
@field("p", name="text")
def y(x):
	print 'p: '
	print x
	return x

@field(".//span[@class='_timestamp js-short-timestamp ']", name="time", attr = "data-time")
def y(x):
	print 'Parsing this particular filed'
	print x
	max_lock_req = requests.get("https://vivid-inferno-9795.firebaseio.com/max_lock_testing/.json")
	if max_lock_req.status_code != 200:
		return ConnectionErrors.NoConnection
	max_lock = int(max_lock_req.content)
	print 'max_lock: '+str(max_lock)
	if int(x) > max_lock:
		print 'x is bigger than max_lock'
		newLock = {'max_lock_testing': int(x.replace('"','')) }
		k = requests.patch(url = 'https://vivid-inferno-9795.firebaseio.com/.json?auth=Jv1GST7wGCGMPfxJLl2Av7yeTPVTkXa7cNucf9t5', data= json.dumps(newLock))
	else:
		print 'x is less than max_lock'
	r = requests.get("https://vivid-inferno-9795.firebaseio.com/storage_lock_testing/.json")
	if r.status_code == 200:
		print 'updated storage'
		posting_lock = int(r.content)
		if int(x) <= posting_lock:
			return RunningErrors.LimitFound
		else:
			return (x, x)
	else:
		print 'did not updated storage'
		return ConnectionErrors.NoConnection


# ------------------------------
# |                            |
# |  Set storage  and logins   |
# |                            |
# ------------------------------
login = Login(username = "jesus.cast.sosa@gmail.com", password = "vistabobgub")
storage = FireBaseConnection(url = "https://vivid-inferno-9795.firebaseio.com/somebodiestweets", secret = "Jv1GST7wGCGMPfxJLl2Av7yeTPVTkXa7cNucf9t5")


# ------------------------------
# |                            |
# |  Run the main program      |
# |                            |
# ------------------------------
# @deamonizer
def main():
	print 'Before running scrapper'
	run(url = "https://twitter.com/BigBang_CBS", nodeOfType = "//li[@data-item-type='tweet']", storage = storage, login = login)
	print 'End of running scraper'
	# Set the lock for the next execution
	# print_text('Saving locks')
	# newLockReq = requests.get("https://vivid-inferno-9795.firebaseio.com/max_current_lock/.json")
	# newLock = None
	# if newLockReq.status_code != 200:
	# 	sys.exit()
	# newLock = newLockReq.content
	# dataForLock = {'storage_lock_testing': int(newLock)}
	# updateReq =requests.patch(url = "https://vivid-inferno-9795.firebaseio.com/.json?auth=Jv1GST7wGCGMPfxJLl2Av7yeTPVTkXa7cNucf9t5", data = json.dumps(dataForLock))
	# if updateReq.status_code != 200:
	# 	sys.exit()

if __name__=="__main__":
	main()