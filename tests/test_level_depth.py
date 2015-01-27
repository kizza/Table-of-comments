import sys
if sys.version_info < (3, 0):
	import testcase
else:
	from . import testcase

#
# Tests elements of the heading levels
#
class TestLevelDepth(testcase.TestCase):

	title = "Test Level Depth"

	# Test that headings can go at least to 
	def test_level_depth_unlimited(self):
		self.set_settings({'toc_level':0});
		self.set_text( self.text() )
		self.run_plugin()
		self.find('* Heading 1')
		self.find('----- Heading 6')

	# Test that the the "toc_level" setting 
	def test_level_depth_limited(self):
		self.set_settings({'toc_level':2});
		self.set_text( self.text() )
		self.run_plugin()
		if self.get_text().find('----- Heading 6') == -1:
			self.ok()
		else:
			self.error('Should not find heading level 6')

	def text(self):
		return """
/*
* TOC
*/

// > Heading 1

// >>>>>> Heading 6

"""