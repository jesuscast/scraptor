from selenium import webdriver
import time
import types

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'
DEBUG_THIS = False

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

class Formats:
	Json = 'json'

class Storages:
	FireBase = 'fb'

class ImageStorages:
	Imgur = 'imgur'

class Paginations:
	ScrollDown = 'ScrollDown'

class ParsingErrors:
	Url = "url"
	AttributeNotPresent = 'AttributeNotPresent'
def Instructions(errorType):
	if errorType == ParsingErrors.Url:
		print "Usage: http://domain.com"
	else:
		print "Error not recognized"

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

class Spider:
	def __init__(self):
		print "inside init function"
		self.fields = []
		self.driver = webdriver.Firefox()
		self.driver.set_script_timeout(10)
		self.driver.set_page_load_timeout(10)
		self.driver.implicitly_wait(10)
	def waitUntilElementAppears(self, selector, father = None):
		father = self.driver if father == None else father
		if selector == "":
			return father
		return father.find_element_by_css_selector(selector)
	def store(self, data, storage):
		print data
	def paginate(self, type):
		return False
	def waitUntilElementsAppear(self, selector, father = None):
		father = self.driver if father == None else father
		if selector == "":
			return [father]
		return father.find_elements_by_css_selector(selector)
	def field(self, selector, name, callback):
		# Receives the selector, the name of the field and the callback after the information is retrieved
		self.fields.append(  Field(selector, name, callback   ) )
	def run(self, url = "", nodeOfType = "", format = Formats.Json, storage = Storages.FireBase, pagination = Paginations.ScrollDown, imageStorage = ImageStorages.Imgur):
		# Check the parameters conform to my specifications
		assert url != "", Instructions(ParsingErrors.Url)
		paginationPossible = True
		while paginationPossible:
			self.driver.get(url)
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
				nodes = self.waitUntilElementsAppear(nodeOfType)
				for node in nodes:
					result = {}
					for field in self.fields:
						fieldElements = self.waitUntilElementsAppear(field.selector, node)
						result[ field.name ] = []
						for element in fieldElements:
							tempResult = field.callback(  element  )
							if tempResult != ParsingErrors.AttributeNotPresent:
								result[ field.name ].append(tempResult)
						if len(result[ field.name ]) == 1:
							result[ field.name ] = result[ field.name ][0]
					self.store(result, storage)
			paginationPossible = self.paginate(pagination)
			time.sleep(2)
		self.driver.close()


default_spider = Spider()

def field(selector, **kwargs):
	assert "name" in kwargs, "Every field should have a name"
	def wrapper(filterFunction):
		default_spider.field(selector, kwargs["name"], filterFunction)
		if "attr" in kwargs:
			default_spider.fields[-1].attribute = kwargs["attr"]
	return wrapper

def run(*args, **kwargs):
	default_spider.run(*args , **kwargs)