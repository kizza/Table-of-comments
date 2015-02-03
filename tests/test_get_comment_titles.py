import sys
if sys.version_info < (3, 0):
    import testcase
else:
    from . import testcase


#
# This is an example text function
#
# - Every function starting with "test_" is run within this testclass
# - You set the input set_text() as well as any particular settings with
#   set_settings()
# - Finally you can run find() or text_equals() to check results which appear
#   in the test output summary
#
class TestGetCommentTitles(testcase.TestCase):

    title = "Get Comment Titles (Core)"

    # Using find() to check if result is correct
    def test_get_basic(self):

        # Setup environment
        self.set_text(self.text_javascript())
        self.set_settings({'level_char': '>'})

        # Run the basic parse function and check them
        toc = self.get_plugin()
        titles = toc.get_comment_titles('string')
        for title in ['Heading 1', '- Heading 2', '-- Heading 3']:
            if title in titles:
                self.ok()
            else:
                self.error('Missing title '+title)

    # Text used to perform tests on
    def text_javascript(self):
        return """
/*
* > Heading 1
*/

/* >> Heading 2 */

// >>> Heading 3

"""

    # Fix for #26
    def test_comment_char_within_comment(self):
        self.set_syntax('javascript')
        toc = self.get_plugin()

        # Check with "-" char
        self.set_settings({'level_char': '-'})
        self.set_text('/* - Foo - Bar */')
        titles = toc.get_comment_titles('string')
        self.assert_true('Foo - Bar' in titles)

        # Check with ">" char
        self.set_settings({'level_char': '>'})
        self.set_text('/* > Modules => My Module (Test 4) */')
        titles = toc.get_comment_titles('string')
        self.assert_true('Modules => My Module (Test 4)' in titles)
