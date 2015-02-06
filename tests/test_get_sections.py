import sys
import sublime
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
class TestGetSections(testcase.TestCase):

    title = "Test Sections"

    # Using find() to check if result is correct
    def test_get_sections(self):
        self.set_text(self.text_javascript())
        self.set_settings({'level_char': '>'})
        toc = self.get_plugin()
        sections = toc.get_sections()

        # Should be 3 sections
        self.assert_true(len(sections) == 3)

        # Match up values
        test_regions = [
            {'title': [1, 20], 'content': [21, 30], 'text': 'Heading 1'},
            {'title': [31, 49], 'content': [50, 58], 'text': 'Heading 2'},
            {'title': [59, 76], 'content': [77, 83], 'text': 'Heading 3'}
            ]

        for i in range(len(sections)):
            # Test title regions match
            self.assert_true(
                sections[i]['title_region'] == sublime.Region(
                    test_regions[i]['title'][0],
                    test_regions[i]['title'][1]
                ),
                'Title region mismatch for item '+str(i)
            )
            # Test content regions match
            self.assert_true(
                sections[i]['content_region'] == sublime.Region(
                    test_regions[i]['content'][0],
                    test_regions[i]['content'][1]
                ),
                'Content region mismatch for item '+str(i)
            )
            # Test section text matches
            self.assert_true(
                sections[i]['text'] == test_regions[i]['text'],
                'Section "text" mismatch'
            )

    # Text used to perform tests on
    def text_javascript(self):
        return """
/*
* > Heading 1
*/
body {

}
/* >> Heading 2 */
div {

}
// >>> Heading 3
a {

}
"""
