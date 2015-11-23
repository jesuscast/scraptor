from selenium import webdriver

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
		return father.get_element_by_css_selector(selector)
	def store(self, data):
		print data
	def paginate(self, type):
		return False
	def waitUntilElementsAppear(self, selector, father = None):
		father = self.driver if father == None else father
		if selector == "":
			return father
		return father.get_elements_by_css_selector(selector)
	def field(self, selector, name, callback):
		# Receives the selector, the name of the field and the callback after the information is retrieved
		self.fields.append(  ( Field(selector), name, callback   ) )
	def run(self, url = "", nodeOfType = "", format = Formats.Json, storage = Storages.FireBase, pagination = Paginations.ScrollDown, imageStorage = ImageStorages.Imgur):
		# Check the parameters conform to my specifications
		assert url != "", Instructions(ParsingErrors.Url)
		paginationPossible = True
		while paginationPossible:
			self.driver.get(url)
			nodes = waitUntilElementsAppear(nodeOfType)
			#waitUntilElementAppears(nodeOfType)
			for node in nodes:
				result = {}
				for field in self.fields:
					fieldElement = waitUntilElementAppears(field[0].selector, father = node)
					result[ field[1] ] = field[1](  fieldElement.text  )
				store(result, storage)
			paginationPossible = paginate(pagination)
			time.sleep(2)


default_spider = Spider()

def field(selector, name):
	def wrapper(filterFunction):
		default_spider.field(selector, name, filterFunction)
	return wrapper

def run(*args, **kwargs):
	default_spider.run(*args , **kwargs)