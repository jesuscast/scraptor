
output_deamonizer = 'stdout'
print_text = print_optional(output_deamonizer)

class Deamonizer:
	def __init__(self):
		self.main_functionality = {"function":None,"args":None,"kwargs":None}
		self.pre_functionality = {"function":None,"args":None,"kwargs":None}
		self.after = {"function":None,"args":None,"kwargs":None}
		self.print_text = None
		self.visibility = False
		self.display = None
	def parse_command_line(self):
		output_deamonizer = 'stdout'
		self.print_text = print_optional(output_deamonizer)
		# ------------------------------------------------------------------------------
		# |      Routines for parsing the command line                                 |
		# |                                                                            |
		# |   Usage: python name_of_file.py [stdout|file_name] [visible|nonvisible]    |
		# ------------------------------------------------------------------------------
		if len(sys.argv) == 2:
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
			self.display = Display(visible = 0, size=(1024, 768))
			self.display.start()
			self.print_text( "should not be visible")
		else:
			self.print_text("SHOULD BE VISIBLE")
	def run(self):
		self.parse_command_line()
		# Try to set up a counter for exceptions.
		exceptionsTimeouts = 0
		# Run Pre
		self.pre_functionality["function"](*self.pre_functionality["args"], **self.pre_functionality["kwargs"])
		while True:
			self.print_text('Inside the loop')
			# Scape the fate of no internet
			self.print_text(bcolors.WARNING+"EXECUTION TIME: "+str(datetime.now())+bcolors.ENDC)
			while not connected_to_internet():
				self.print_text("Not connected to the internet. Going to sleep for five minutes")
				time.sleep(60*5)
			self.print_text('About to start the try except')
			try:
				self.main_functionality["function"](*self.main_functionality["args"], **self.main_functionality["kwargs"])
			except TimeoutException as e:
				self.print_text(bcolors.FAIL+'Timeout exception of selenium. Trying again.'+bcolors.ENDC)
				exceptionsTimeouts += 1
				# if exceptionsTimeouts % 6 == 0:
				# 	os.system("python send_text.py \"Error in quickbooks Too many timeouts. "+str(e)+"\"")
			except Exception as e:
				self.print_text(bcolors.FAIL+"Error in quickbooks: "+str(e)+bcolors.ENDC)
				#os.system("python send_text.py \"Error in quickbooks. "+str(e)+"\"")
			self.print_text('Going to sleep for five minutes')
			time.sleep(60*5)
		if not self.visibility:
			self.display.stop()


default_deamon = Deamonizer()

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