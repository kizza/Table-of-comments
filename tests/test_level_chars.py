import sys
if sys.version_info < (3, 0):
    import testcase
else:
    from . import testcase


#
# This test function tests elements of the heading levels
#
class TestLevelChars(testcase.TestCase):

    title = "Heading Level Characters"

    def test_level_chars(self):
        # Check for "#" as level char
        self.set_text(self._test_text1())
        self.set_settings({'level_char': '#'})
        self.run_plugin()
        self.find('* Heading 1')

        # Check for "-" as level char
        self.set_text(self._test_text2())
        self.set_settings({'level_char': '-'})
        self.run_plugin()
        self.find('* Heading 1')

        # Check for ":" as level char
        self.set_text(self._test_text3())
        self.set_settings({'level_char': ':'})
        self.run_plugin()
        self.find('* Heading 1')


#
# Initial text used in above tests
#

    def _test_text1(self):
        return """
/*
* TOC
*/

// # Heading 1

// ## Heading 2

"""

    def _test_text2(self):
        return """
/*
* TOC
*/

// - Heading 1

// -- Heading 2

"""

    def _test_text3(self):
        return """
/*
* TOC
*/

// : Heading 1

// :: Heading 2

"""
