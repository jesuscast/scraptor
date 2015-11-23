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

def spider(function):
	def 

class Spider:
	def __init__(self):
		print "inside init function"
		self.fields = []
	def field(self, selector, name, callback):
		self.fields.append(  ( Field(selector), name, callback   ) )
	def run(self):
		names = ["fuck fuck replacfuck in here", "leave this clean"]
		for name in names:
			for field in self.fields:
				print field[2](name)

class Field:
	def __init__(self, selector):
		self.selector = selector

default_spider = Spider()

def field(selector, name):
	def wrapper(filterFunction):
		default_spider.field(selector, name, filterFunction)
	return wrapper

def run():
	default_spider.run()

@field(".a > hr", name = "Names")
def cleanName(name):
	return name.replace("fuck","")

