
""" Unit Testing framework for sublime plugins """

import sys
import sublime
import os
import imp
from os import walk

#
# Add additional classes as required
#
if sys.version_info < (3, 0):
    from tests.test_get_comment_titles import TestGetCommentTitles
    from tests.test_level_depth import TestLevelDepth
    from tests.test_level_chars import TestLevelChars
    from tests.test_comment_syntax import TestCommentSyntax
    from tests.test_toc_output import TestTocOutput
    from .test_large_file import TestLargeFile
else:
    from .test_get_comment_titles import TestGetCommentTitles
    from .test_level_depth import TestLevelDepth
    from .test_level_chars import TestLevelChars
    from .test_comment_syntax import TestCommentSyntax
    from .test_toc_output import TestTocOutput
    from .test_large_file import TestLargeFile


# Returns list of properties for each test class names matching "test_*.py"
def auto_get_test_modules():
    f = []
    tests_path = os.path.join(
        sublime.packages_path(), "Table of comments", "tests")
    for (dirpath, dirnames, filenames) in walk(tests_path):
        for filename in filenames:
            if filename.startswith('test_') and filename.endswith('.py'):
                path = filename.replace('.py', '')
                classname = ''
                bits = path.split('_')
                for bit in bits:
                    classname += bit.title()
                f.append({
                    'filename': filename,
                    'classname': classname,
                    'path': path
                    })
    return f


#
# Reload module functionality (borrowed from sublimelint for ease when
# developing/debugging)
#
# Sublime Text auto loads the primary plugin module when the file is changed
# but doesn't do this for sub modules
#
def reload_test_modules():
    modules = auto_get_test_modules()
    load_module('testcase')
    for module in modules:
        load_module(module['path'])


def load_module(path):
    basedir = os.getcwd()
    os.chdir(basedir)
    if sys.version_info < (3, 0):
        path = 'tests.'+path
        __import__(path)
        sys.modules[path] = reload(sys.modules[path])
    else:
        imp.reload(eval(path))


#
# Run the tests
#
def run(view, edit):
    reload_test_modules()
    reload_test_modules()
    reload_test_modules()
    view = create_new_view(view)
    view.set_name('Unit Tests')
    output = "Table of Comments Unit Tests\n" + "=" * 50 + "\n"

    # Load and create all the test classes from file system
    tests = []
    modules = auto_get_test_modules()
    for module in modules:
        test_class = eval(module['classname'] + '(view, edit)')
        tests.append(test_class)

    # Customise test run (for specific items or order while developing)
    # tests = [
    #     TestLargeFile(view, edit),
    #     ]

    # Run tests for results
    for test in tests:
        output += get_test_output(test)

    # Append errors
    output += get_test_errors(tests)

    # Output test results
    output = "/*\n\n" + output + "\n\n*/"
    view.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
    view.replace(edit, sublime.Region(0, view.size()), '')
    view.insert(edit, 0, output)
    highlight(view)
    view.set_scratch(True)  # Allow results to close without saivng


# Highlight the test result regions
def highlight(view):
    # regions = view.find_all('\.') # OK regions
    regions = view.find_all('F')  # Error regions
    add = []
    for region in regions:
        line = view.line(region)
        if view.substr(line).find('(') > 0 and view.rowcol(line.a)[0] > 0:
            add.append(region)
    add_region(view, 'table-of-comments-error', 'error', add)


def add_region(view, key, style, add):
    if sys.version_info < (3, 0):
        view.add_regions(key, add, 'storage', sublime.DRAW_EMPTY)
    else:
        view.add_regions(key, add, 'storage', '', sublime.DRAW_NO_OUTLINE)


def unhighlight(view):
    view.erase_regions('table-of-comments-ok')
    view.erase_regions('table-of-comments-error')


def create_new_view(view):
    view = sublime.active_window().new_file()
    return view


def get_test_output(test):
    output = "\nRunning " + test.title + "\n" + "-" * 50 + "\n"
    test.setup()
    output += test.run()
    test.teardown()
    return output


def get_test_errors(tests):
    errors = []
    for test in tests:
        if len(test.errors) > 0:
            errors += test.errors
    if len(errors) > 0:
        return "\n\n"+str(len(errors))+" errors were found\n" + \
            ('=' * 50) + "\n\n - " + "\n - ".join(errors)

    return "\n" + ('=' * 50) + "\n" + "Yes! All tests from " +  \
        str(len(tests)) + " classes passed."
