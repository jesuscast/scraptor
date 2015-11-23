from selenium import webdriver
import time

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

def Instructions(errorType):
	if errorType == ParsingErrors.Url:
		print "Usage: http://domain.com"
	else:
		print "Error not recognized"

class Field:
	def __init__(self, selector):
		self.selector = selector

class Spider:
	def __init__(self):
		print "inside init function"
		self.fields = []
		self.driver = webdriver.Firefox()
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
		self.fields.append(  ( Field(selector), name, callback   ) )
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
					fieldElements = self.waitUntilElementsAppear(field[0].selector)
					print "LEN OF ELEMENTS: "+str(len(fieldElements))
					result[ field[1] ] = []
					for element in fieldElements:
						result[ field[1] ].append(field[2](  element.text  ))
					self.store(result, storage)
			else:
				# The node is an actual css selctor
				nodes = self.waitUntilElementsAppear(nodeOfType)
				for node in nodes:
					result = {}
					for field in self.fields:
						fieldElement = self.waitUntilElementAppears(field[0].selector, father = node)
						result[ field[1] ] = field[2](  fieldElement.text  )
					self.store(result, storage)
			paginationPossible = self.paginate(pagination)
			time.sleep(2)
		self.driver.close()


default_spider = Spider()

def field(selector, name):
	def wrapper(filterFunction):
		default_spider.field(selector, name, filterFunction)
	return wrapper

def run(*args, **kwargs):
	default_spider.run(*args , **kwargs)