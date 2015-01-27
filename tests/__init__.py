import sys, sublime

#
# Import test classes to run
# Add additional classes as required
#
if sys.version_info < (3, 0):
	from tests.test_get_comment_titles import TestGetCommentTitles
	from tests.test_level_depth import TestLevelDepth
	from tests.test_level_chars import TestLevelChars
	from tests.test_comment_syntax import TestCommentSyntax
	from tests.test_toc_output import TestTocOutput
else:
	from .test_get_comment_titles import TestGetCommentTitles
	from .test_level_depth import TestLevelDepth
	from .test_level_chars import TestLevelChars
	from .test_comment_syntax import TestCommentSyntax
	from .test_toc_output import TestTocOutput




#
# Run the tests
#
def run(view, edit):
	view = create_new_view(view)
	view.set_name('Unit Tests')
	output = "Table of Comments Unit Tests\n" + "=" * 50 + "\n"

	# List test classes to run
	tests = [
		TestGetCommentTitles(view, edit),
		TestLevelDepth(view, edit),
		TestLevelChars(view, edit),
		TestCommentSyntax(view, edit),
		TestTocOutput(view, edit)
		]

	# Run tests for results
	for test in tests:
		output+= get_test_output( test )

	# Append errors
	output+= get_test_errors(tests)

	# Output test results
	output = "/*\n\n" + output + "\n\n*/"
	view.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage') # incase changed
	view.replace(edit, sublime.Region(0, view.size()), '')
	view.insert(edit, 0, output)
	highlight(view)
	view.set_scratch(True) # Allow results to close without saivng

# Highlight the test result regions
def highlight(view):
	# regions = view.find_all('\.') # OK regions
	regions = view.find_all('F') # Error regions
	add = []
	for region in regions:
		line = view.line(region)
		if view.substr(line).find('(') > 0 and view.rowcol(line.a)[0] > 0:
			add.append(region)
	add_region(view, 'table-of-comments-error', 'error', add)

def add_region(view, key, style, add):
	if sys.version_info < (3, 0):
		view.add_regions(key, add, 'storage', sublime.DRAW_EMPTY) # sublime.DRAW_OUTLINED if outline else 
	else:
		view.add_regions(key, add, 'storage', '', sublime.DRAW_NO_OUTLINE) # sublime.DRAW_OUTLINED if outline else 

		
def unhighlight(view):
	view.erase_regions('table-of-comments-ok')
	view.erase_regions('table-of-comments-error')

def create_new_view(view):
	view = sublime.active_window().new_file()
	return view

def get_test_output(test):
	output = test.setup()
	output+= test.run()
	test.teardown()
	return output

def get_test_errors(tests):
	errors = []
	for test in tests:
		if len(test.errors) > 0:
			errors+= test.errors
	if len(errors)> 0:
		return "\n\n"+str(len(errors))+" errors were found\n" + ('=' * 50) + "\n\n - " + "\n - ".join(errors)
	return "\n" + ('=' * 50) + "\n" + "Yes! All tests from "+ str(len(tests)) + " classes passed." 




