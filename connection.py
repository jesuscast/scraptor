import requests
import json
class RemoteConnection:
	TOKENS = {
		"jesus":"FdoNdFUPy20yq3ZhNMbvONL61OlkbcWgSdWsKQpV",
		"lorenzo":"lz4KJy0XzrWrQb8KvBFicPi4qOrSUKw5CPJTFoW0"
		}
	FIREBASE_URL = "https://inncubator.firebaseio.com/"
	def __init__(self):
		assert name in self.TOKENS
		self.token = self.TOKENS[name]
		self.ending = "?auth="+self.token
	def to_url(self, stringT):
		assert stringT[0] != "/"
		return self.FIREBASE_URL+stringT+"/.json"+self.ending
	def get_ad(self, ad_id):
		url = self.to_url("craigslist-information/ads/"+ad_id)
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def get_schedule(self, account):
		url = ""
		if account=="help.inncubator@gmail.com":
			url = self.to_url("craigslist-information/schedule/help-inncubator")
		elif account=="info.inncubator@gmail.com":
			url = self.to_url("craigslist-information/schedule/info-inncubator")
		elif account=="craigslist.inncubator@gmail.com":
			url = self.to_url("craigslist-information/schedule/craigslist-inncubator")
		elif account=="sharedliving5@gmail.com":
			url = self.to_url("craigslist-information/schedule/sharedliving5")
		elif account=="sfb.inncubator@gmail.com":
			url = self.to_url("craigslist-information/schedule/sfb-inncubator")
		else:
			return None
		#print url
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def get_groups(self):
		url = self.to_url("craigslist-information/groups")
		#print url
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def get_group(self, group_name):
		""" Returns an array with the ads inside the group """
		url = self.to_url("craigslist-information/groups/"+group_name)
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def set_group(self, group_name, dataL):
		""" Sets the values inside group name to data """
		data = {group_name: dataL}
		result = requests.patch(url = self.to_url('craigslist-information/groups'), data=json.dumps(data))
		if result.status_code != 200:
			print result.content
			print result.status_code
			return False
		return True
	def update_schedule(self, account, data):
		""" Updates the schedule according to the new data """
		result = requests.patch(url = self.to_url('craigslist-information/schedule/'+account), data=json.dumps(data))
		return result
	def update_ad(self, adInfo):
		data = {}
		data["account"] = adInfo.account
		data["from"] = adInfo.id_from
		data["group"] = adInfo.group
		data["replacement"] = adInfo.id_replacement
		data["status"] = adInfo.status
		data["title"] = adInfo.title
		data["expired-and-published"] = 'False'
		data['status'] = adInfo.status
		result = requests.patch(url = self.to_url('craigslist-information/ads/'+adInfo.ad_id), data=json.dumps(data))
		if result.status_code != 200:
			print str(adInfo.ad_id)+" ERROR"
			return False 
		print str(adInfo.ad_id)+" updated to firebase"
		return True
	def get_ads(self):
		url = self.to_url("craigslist-information/ads")
		print url
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def get_untracked(self):
		url = self.to_url("craigslist-information/untracked")
		print url
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None
	def set_untracked(self, dataJ):
		""" Updates the untracked ads """
		data = {}
		data["untracked"] = dataJ
		result = requests.patch(url = self.to_url('craigslist-information'), data=json.dumps(data))
		return result
	def get_lock(self, account):
		url = self.to_url("craigslist-information/schedule/"+account+"/posting_lock")
		print url
		r = requests.get(url = url)
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return int(json_r)
		else:
			return None
	def set_lock(self, account, value):
		url = self.to_url("craigslist-information/schedule/"+account)
		print url
		data = {}
		data["posting_lock"] = value
		r = requests.patch(url = url, data=json.dumps(data))
		if r.status_code == requests.codes.ok:
			json_r = r.json()
			return json_r
		else:
			return None