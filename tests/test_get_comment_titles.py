import sys
if sys.version_info < (3, 0):
    import testcase
    from tableofcomments import TableOfComments
else:
    from . import testcase
    from ..tableofcomments import TableOfComments


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
        toc = TableOfComments(self.view, self.edit)
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
