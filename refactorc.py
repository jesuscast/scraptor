import requests
import json

class FireBaseConnection:
	# FIREBASE_URL = "https://inncubator.firebaseio.com/"
	def __init__(self, url, secret):
		self.token = secret
		self.ending = "?auth="+self.token
		self.FIREBASE_URL = self.url
	def to_url(self, stringT):
		assert stringT[0] != "/"
		return self.FIREBASE_URL+stringT+"/.json"+self.ending
	def post_data(self, data, node = ''):
		result = requests.post(url = self.to_url(node), data=json.dumps(data))
		return result

import uuid
import hashlib
 
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
    
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
