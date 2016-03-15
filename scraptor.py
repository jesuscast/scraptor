#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium import webdriver
from datetime import datetime
import requests
import types
import time
import json
import sys
import os


# ------------------------------
# |                            |
# |  Global Variables          |
# |                            |
# ------------------------------
__author__ = "jesus.cast.sosa@gmail.com"
__version__ = "0.5.0"
__license__ = "MIT"

DEBUG_THIS = False

# ------------------------------
# |                            |
# |  Utilities                 |
# |                            |
# ------------------------------

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def debug(function):
	def activeDebug(*args, **kwargs):
		print "\033[92mEntered into "+str(function.__name__)+"\033[0m"
		exitValue = function(*args,**kwargs)
		try:
			print "\033[94mExit value of: "+str(function.__name__)+" is: "+str(exitValue)+" of type: "+str(type(exitValue))+"\033[0m"
		except:
			print "\033[91mThe result of "+function.__name__+" could not be parsed into a string"+"\033[0m"
		return exitValue
	if DEBUG_THIS:
		return activeDebug
	else:
		return function

def connected_to_internet(url='http://www.google.com/', timeout=5):
	try:
		_ = requests.get(url, timeout=timeout)
		return True
	except Exception as e:
		return False

def print_optional(type_of_print):
	def print_normal(text):
		print text
	def print_with_flush(text):
		print text
		sys.stdout.flush()
	if type_of_print == 'stdout':
		return print_normal
	else:
		return print_with_flush

output_deamonizer = 'stdout'
print_text = print_optional(output_deamonizer)

# ------------------------------
# |                            |
# |  Connection Class          |
# |                            |
# ------------------------------

class FireBaseConnection:
	def __init__(self, url, secret):
		self.token = secret
		self.ending = "?auth="+self.token
		self.FIREBASE_URL = url
	def to_url(self, stringT):
		return self.FIREBASE_URL+stringT+"/.json"+self.ending
	def post_data(self, data, node = ''):
		result = None
		if node == '':
			result = requests.post(url = self.to_url(''), data=json.dumps(data))
		else:
			newElement = {}
			newElement[str(node)] = data
			result = requests.patch(url = self.to_url(''), data=json.dumps(newElement))
		return result

# ------------------------------
# |                            |
# |  Error Classes             |
# |                            |
# ------------------------------

class ParsingErrors:
	Url = "url"+'-'*5
	AttributeNotPresent = 'AttributeNotPresent'+'-'*5

class RunningErrors:
	LimitFound = 'LimitFound'+'-'*5

class ConnectionErrors:
	NoConnection = 'NoConnection'+'-'*5

def Instructions(errorType):
	""" Parsrs the correspondent error message for 'instructions' when calling the run function """
	if errorType == ParsingErrors.Url:
		print "Usage: http://domain.com"
	else:
		print "Error not recognized"

# ------------------------------
# |                            |
# |  Arguments for run         |
# |  function                  |
# |                            |
# ------------------------------
class Formats:
	Json = 'json'+'-'*5

class Storages:
	FireBase = 'fb'+'-'*5
	StdOut = 'stdout'+'-'*5

class ImageStorages:
	Imgur = 'imgur'+'-'*5

class Paginations:
	ScrollDown = 'ScrollDown'+'-'*5




# ------------------------------
# |                            |
# |  Holder classes for        |
# |  information in the spider |
# |                            |
# ------------------------------
class Login:
	def __init__(self, username, password):
		self.username = username
		self.password = password

class Field:
	def __init__(self, selector, name, callback):
		self.selector = selector
		self.name = name
		self.callback_temp = callback
		self.attribute = None
	def callback(self, element):
		if self.attribute != None:
			assert type(self.attribute) == types.StringType, "The attribute must be a string"
			tempAttr = element.get_attribute(self.attribute)
			if tempAttr == None:
				return ParsingErrors.AttributeNotPresent
			return self.callback_temp(tempAttr)
		else:
			return self.callback_temp(element.text)

# ------------------------------
# |                            |
# | Main Spider Class          |
# |                            |
# ------------------------------
class Spider:
	def __init__(self):
		self.fields = []
		self.driver = None
		self.html_tags = ["a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist", "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "iframe", "img", "input", "ins", "kbd", "keygen", "label", "legend", "li", "link", "main", "map", "mark", "menu", "menuitem", "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rb", "rp", "rt", "rtc", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr"]
		self.driver = None
	def generate_driver(self):
		tempDriver = webdriver.Firefox()
		tempDriver.set_script_timeout(10)
		tempDriver.set_page_load_timeout(10)
		tempDriver.implicitly_wait(10)
		return tempDriver
	def waitUntilElementAppears(self, selector, father = None):
		father = self.driver if father == None else father
		if selector == "":
			return father
		elif (selector[0] == '.' and './/' not in selector) or selector[0] == '#' or selector in self.html_tags:
			return father.find_element_by_css_selector(selector)
		else:
			return father.find_element_by_xpath(selector)
	def waitUntilElementsAppear(self, selector, father = None):
		father = self.driver if father == None else father
		if selector == "":
			return [father]
		elif (selector[0] == '.' and './/' not in selector) or selector[0] == '#' or selector in self.html_tags:
			return father.find_elements_by_css_selector(selector)
		else:
			return father.find_elements_by_xpath(selector)
	def store(self, data, storage, node = None):
		if storage == Storages.StdOut:
			print data
		else:
			if node != None:
				storage.post_data(data, node)
			else:
				storage.post_data(data)
	def paginate(self, type):
		try:
			if type == Paginations.ScrollDown:
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				return True
			else:
				return False
		except:
			return False
	def field(self, selector, name, callback):
		# Receives the selector, the name of the field and the callback after the information is retrieved
		self.fields.append(  Field(selector, name, callback   ) )
	def login(self, loginAttr):
		inputElements = self.driver.find_elements_by_css_selector("input")
		if loginAttr != None:
			for i in range(len(inputElements)):
				if inputElements[i].get_attribute('type') == 'password' and i != 0:
					try:
						inputElements[i].send_keys(loginAttr.password)
						inputElements[i-1].send_keys(loginAttr.username)
						inputElements[i].submit()
						break
					except:
						continue
		return True
	def end(self):
		self.driver.close()
	def run(self, **kwargs):
		# Set up attributes according to presence because I do not like setting them up according to position.
		# What if you want to set an argument but you have to set a bunch to get to it ?
		url = "" if "url" not in kwargs else kwargs["url"]
		nodeOfType = "" if "nodeOfType" not in kwargs else kwargs["nodeOfType"]
		formatAttr = Formats.Json if "format" not in kwargs else kwargs["format"]
		storage = Storages.StdOut if "storage" not in kwargs else kwargs["storage"]
		pagination = Paginations.ScrollDown if "pagination" not in kwargs else kwargs["pagination"]
		imageStorage = ImageStorages.Imgur if "imageStorage" not in kwargs else kwargs["imageStorage"]
		loginAttr = None if "login" not in kwargs else kwargs["login"]
		# Check the parameters conform to my specifications
		assert url != "", Instructions(ParsingErrors.Url)
		if self.driver == None:
			self.driver = self.generate_driver()
		self.driver.get(url)
		self.login(loginAttr)
		paginationPossible = True
		quitAll = False
		skipLength = 0
		self.driver.get(url)
		while paginationPossible:
			nodes = None
			if nodeOfType == "":
				# The node is not a css selctor
				result = {}
				for field in self.fields:
					fieldElements = self.waitUntilElementsAppear(field.selector)
					result[ field.name ] = []
					for element in fieldElements:
						tempResult = field.callback(  element  )
						if tempResult != ParsingErrors.AttributeNotPresent:
							result[ field.name ].append(tempResult)
					self.store(result, storage)
			else:
				# The node is an actual css selctor
				currentIndex = 0
				skipLengthLocal = skipLength
				nodes = self.waitUntilElementsAppear(nodeOfType)
				skipLength = len(nodes)
				for node in nodes:
					if currentIndex < skipLengthLocal:
						currentIndex += 1
						continue
					currentIndex += 1
					result = {}
					nodeTitle = None
					for field in self.fields:
						fieldElements = self.waitUntilElementsAppear(field.selector, node)
						result[ field.name ] = []
						for element in fieldElements:
							tempTempResult = field.callback(  element  )
							tempResult = None
							if type(tempTempResult) == types.TupleType:
								tempResult = tempTempResult[0]
								nodeTitle = str(tempTempResult[1])
							else:
								tempResult = tempTempResult
							if tempResult == RunningErrors.LimitFound:
								quitAll = True
								break
							elif tempResult != ParsingErrors.AttributeNotPresent:
								result[ field.name ].append(tempResult)
						if quitAll:
							break
						if len(result[ field.name ]) == 1:
							result[ field.name ] = result[ field.name ][0]
					if quitAll:
						break
					self.store(result, storage, nodeTitle)
				if quitAll:
					break
			if quitAll:
				break
			paginationPossible = self.paginate(pagination)
			time.sleep(2)


default_spider = Spider()

# ------------------------------
# |                            |
# |  Decorators that act upon  |
# |  the default_spider        |
# |                            |
# ------------------------------

def field(selector, **kwargs):
	assert "name" in kwargs, "Every field should have a name"
	def wrapper(filterFunction):
		default_spider.field(selector, kwargs["name"], filterFunction)
		if "attr" in kwargs:
			default_spider.fields[-1].attribute = kwargs["attr"]
	return wrapper

def run_spider(*args, **kwargs):
	default_spider.run(*args , **kwargs)



# ------------------------------
# |                            |
# |  Deamonizer class for the  |
# |   deamonize deocrator      |
# |                            |
# ------------------------------
class Deamonizer:
	def __init__(self):
		self.main_functionality = {"function":None,"args":None,"kwargs":None}
		self.pre_functionality = {"function":None,"args":None,"kwargs":None}
		self.print_text = None
		self.visibility = False
		self.display = None
	def format_log(self, priority, description, text):
		"""
			DEBUG - for genuinely debug-level info; will not be seen in production or shipped product, as INFO will be the minimum level; good for capturing timings, number of occurrences of events, etc

			INFO - minimum level for production/shipped usage; record data likely to be useful in forensic investigations and to confirm successful outcomes ("stored 999 items in DB OK"); all info here must be such that you would be OK with end users/customers seeing it and sending you it, if need be (no secrets, no profanity!)

			WARN - not an error level as such, but useful to know the system may be entering dodgy territory, e.g. business logic stuff like "number of ordered products < 0" which suggests a bug somewhere, but isn't a system exception; I tend not to use it that much to be honest, finding things tend to be more natural fits to INFO or ERROR

			ERROR - use this for exceptions (unless there's a good reason to reduce to WARN or INFO); log full stacktraces along with important variable values without which diagnosis is impossible; use only for app/system errors, not bad business logic circumstances

			FATAL - only use this for an error of such high severity that it literally prevents the app from starting / continuing
			(http://stackoverflow.com/questions/7486596/commons-logging-priority-best-practices) Retrieved 1453177472
		"""
		start_color = ''
		end_color = bcolors.ENDC
		priotity = priority.lower()
		if 'info' in priority:
			start_color = bcolors.OKBLUE
		elif 'warn' in priority:
			start_color = bcolors.WARNING
		elif 'error' in priority:
			start_color = bcolors.FAIL
		elif 'fatal' in priority:
			start_color = bcolors.FAIL
		else:
			end_color = ''
		if len(description) > 30:
			description = description[:27]+'...'
		return '{4}{0!s:30} {1!s:20} {2!s:30} {3}{5}'.format(time.ctime(time.time()), priority, description, text, start_color, end_color)
	def parse_command_line(self):
		output_deamonizer = 'stdout'
		self.print_text = print_optional(output_deamonizer)
		# ------------------------------------------------------------------------------
		# |      Routines for parsing the command line                                 |
		# |                                                                            |
		# |   Usage: python name_of_file.py [stdout|file_name] [visible|nonvisible]    |
		# ------------------------------------------------------------------------------
		if len(sys.argv) == 2:
			if sys.argv[1] == 'compile':
				# Saving of the run file
				fileTmpName = os.path.basename(__file__)
				filenameRun = 'run_'+fileTmpName.replace('.py','')+'.sh'
				result_string = ''
				result_string += 'cd '+os.path.dirname(os.path.abspath(fileTmpName))+' && '+sys.executable+' '+fileTmpName+' '+fileTmpName.replace('.py','')+'.log nonvisible 2>&1'
				f = open(filenameRun, 'w')
				f.write(result_string)
				f.close()
				# Saving of the crontab script
				filename = 'crontab_'+fileTmpName.replace('.py','')+'.txt'
				result_string = ''
				result_string += '30 7 * * * sh '+os.path.dirname(os.path.abspath(fileTmpName))+'/'+filenameRun
				print result_string
				f = open(filename, 'w')
				f.write(result_string)
				f.close()
				sys.exit()
			else:
				sys.stdout = open(sys.argv[1], 'a')
				output_deamonizer = 'file'
				self.print_text = print_optional(output_deamonizer)
		elif len(sys.argv) == 3:
			if sys.argv[1] != 'stdout':
				sys.stdout = open(sys.argv[1], 'a')
				output_deamonizer = 'file'
				self.print_text = print_optional(output_deamonizer)
			self.visibility = sys.argv[2] == 'visible'
		sys.stderr = sys.stdout
		if not self.visibility:
			from pyvirtualdisplay import Display
			self.display = Display(visible = 0, size=(1024, 768))
			self.display.start()
			self.print_text(self.format_log('debug','message','Using virtual display.'))
		else:
			self.print_text(self.format_log('debug','message','Not using virtual display.'))
	def run(self):
		self.parse_command_line()
		# Try to set up a counter for exceptions.
		exceptionsTimeouts = 0
		# Run Pre
		if self.pre_functionality["function"] != None:
			self.pre_functionality["function"](*self.pre_functionality["args"], **self.pre_functionality["kwargs"])
		while True:
			self.print_text(self.format_log('debug','message','Inside the infinite loop.'))
			# Scape the fate of no internet
			self.print_text(self.format_log('info','current time', str(datetime.now())))
			while not connected_to_internet():
				self.print_text(self.format_log('warning','connection error','Not connected to the internet. Going to sleep for five minutes'))
				time.sleep(60*5)
			self.print_text(self.format_log('debug','message','About to start the try except'))
			try:
				if self.main_functionality["function"] != None:
					self.main_functionality["function"](*self.main_functionality["args"], **self.main_functionality["kwargs"])
			except TimeoutException as e:
				self.print_text(self.format_log('error','exception','Timeout exception of selenium. Trying again.'))
				exceptionsTimeouts += 1
				# if exceptionsTimeouts % 6 == 0:
				# 	os.system("python send_text.py \"Error in quickbooks Too many timeouts. "+str(e)+"\"")
			except Exception as e:
				self.print_text(self.format_log('fatal','exception','Unrecognized exception.'))
			self.print_text(self.format_log('debug','message','Going to sleep for five minutes'))
			time.sleep(60*5)
		if not self.visibility:
			self.display.stop()


default_deamon = Deamonizer()

# ------------------------------
# |                            |
# |  Decorators that act upon  |
# |  default deamon instance   |
# |                            |
# ------------------------------

def deamonize(*args, **kwargs):
	def wrapper(filterFunction):
		default_deamon.main_functionality =  { "function": filterFunction,"args":args,"kwargs":kwargs}
	return wrapper

def pre_deamon(*args, **kwargs):
	def wrapper(filterFunction):
		default_deamon.pre_functionality =  { "function": filterFunction,"args":args,"kwargs":kwargs}
	return wrapper

def run_deamon():
	default_deamon.run()
