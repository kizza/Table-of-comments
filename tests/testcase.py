import sublime, inspect, re

#
# Default class inherited by all test classes
# Provides basic behaviour to write a test class easily
#
class TestCase():

	output = ''
	errors = []
	
	def __init__(self, view, edit):
		self.output = ''
		self.errors = []
		self.view = view
		self.edit = edit

	# Called before class is run
	def setup(self):
		self.view.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
		return "\nRunning " + self.title + "\n" + "-" * 50 + "\n"

	# Runs all test methods
	def run(self):
		self.backup_plugin_settings()
		methods = self.get_test_methods()
		for testname in methods:
			self.output+= ''+ testname + '() '
			eval('self.'+testname+'()')
			self.output+= '\n'
		self.restore_plugin_settings()
		return self.output

	# Called after class is run
	def teardown(self):
		pass

#
# Helper functions
#

	def get_test_methods(self):
		test_methods = []
		members = inspect.getmembers(self, predicate=inspect.ismethod)
		for name, func in members:
			if name.find("test_") == 0:
				test_methods.append(name)
		return test_methods

	def set_text(self, text):
		self.view.replace(self.edit, sublime.Region(0, self.view.size()), '')
		self.view.insert(self.edit, 0, text)

	def get_text(self):
		return self.view.substr(sublime.Region(0, self.view.size()))

	def run_plugin(self):
		self.view.run_command('table_of_comments')	

#
# Settings functions 
# (allows us to have differnt settings for different tests - and restore to normal afterwards)
#

	def backup_plugin_settings(self):
		self.settings = sublime.load_settings('tableofcomments.sublime-settings')
		self._original_settings = {}
		for name in [ 'toc_char', 'level_char', 'toc_level' ]:
			if self.settings.has(name):
				self._original_settings[name] = self.settings.get(name)

	def restore_plugin_settings(self):
		if self._original_settings:
			values = self._original_settings
			for name in values:
				self.settings.set( name, values[name] )
			sublime.save_settings('tableofcomments.sublime-settings')

	def set_settings(self, settings):
		for name in settings:
			self.settings.set(name, settings[name])
		sublime.save_settings('tableofcomments.sublime-settings')

#
# Result functions
#

	def error(self, text):
		self.errors.append(text)
		self.output+= 'F'

	def ok(self):
		self.output+= '.'

#
# Assert functions for unit tests
#

	# Assert function to see if entire result text equals the sent text
	def text_equals(self, sent):
		text = self.get_text()
		if text.strip() == sent.strip():
			self.ok()
		else:
			self.error( "Text not equal betwen \n# : From..."+"\n---"+text + "\n---\nto...\n---"+sent+"\n---" )

	# Assert function to check for sent text witin result text
	def find(self, text):
		result = self.get_text()
		match  = result.find(text)
		if match >= 0:
			self.ok()
			return True
		else:
			self.error( "Couldn't find \""+ text + "\"" )
			return False