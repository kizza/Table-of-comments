import sys
if sys.version_info < (3, 0):
	import testcase
else:
	from . import testcase

#
# Tests that the TOC output list is correct
#
class TestTocOutput(testcase.TestCase):

	title = "TOC Output"

	# Using find() to check if result is correct
	def test_toc_basic(self):
		# Setup environment
		self.set_text( self.text() )
		self.set_settings({ 'level_char':'>' })
		self.set_settings({ 'toc_char':'-' })
		self.run_plugin()

		# This checks that the headings appear
		self.find('* Heading 1')
		self.find('* - Heading 2')
		self.find('* -- Heading 3')

		# This is a full text output test (which )
		self.text_equals(self.result())

	def test_toc_different_toc_char(self):
		# Setup environment
		self.set_text( self.text() )
		self.set_settings({ 'level_char':'>' })
		self.set_settings({ 'toc_char':'+' })
		self.run_plugin()
		self.find('* + Heading 2')

	# Text used to perform tests on
	def text(self):
		return """
/*
* TOC
*/

// > Heading 1

// >> Heading 2

// >>> Heading 3
"""

	def result(self):
		return """
/*
* TOC
* 
* Heading 1
* - Heading 2
* -- Heading 3
*/

// > Heading 1

// >> Heading 2

// >>> Heading 3
"""