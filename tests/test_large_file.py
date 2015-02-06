import sys
if sys.version_info < (3, 0):
    import testcase
else:
    from . import testcase


#
# This test function tests the duration for a large file
#
class TestLargeFile(testcase.TestCase):

    title = "Large amount of content"

    # Create a large text file, runs the plugin with the output time
    def test_large_file(self):
        text = ''
        depth = 1
        for i in range(100):
            text += self._test_text_title(depth) + '\n'
            text += self._test_text_body() + '\n'
            depth = 1 if depth == 5 else depth + 1
        self.set_settings({'level_char': '>'})
        self.set_syntax('javascript')
        self.set_text(text)
        toc = self.get_plugin()
        toc.get_comment_titles()
        timers = toc.timers
        for key in timers:
            duration = "{0:.6f}".format(timers[key])
            self.assert_true(
                timers[key] < 0.9,
                '"'+key+'" takes too long ('+duration+' seconds)'
                )


#
# Initial text used in above test
#

    def _test_text_title(self, depth):
        return '/* ' + (depth * '>') + ' Lorem ipsum dolor sit amet */'

    def _test_text_body(self):
        return """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt
in culpa qui officia deserunt mollit anim id est laborum.
"""
