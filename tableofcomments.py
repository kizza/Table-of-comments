"""
Plugin to create a quick panel lookup that lets you jump between comment
titles
"""

import os
import imp
import time
import sys
import sublime
import sublime_plugin
import re


#
# > Plugin command
#
class table_of_comments_command(sublime_plugin.TextCommand):

    def run(self, edit, move=None, fold=None, unfold=None):
        toc = TableOfComments(self.view, edit)
        if move is not None:
            self.traverse_comments(toc, move)
        elif fold is not None or unfold is not None:
            self.fold_comments(toc, fold, unfold)
        else:
            self.show_quick_panel(toc)

    # >> Quick panel
    def show_quick_panel(self, toc):
        view = self.view
        toc._debug_start('Show quick panel')
        toc.create_toc()
        # Get current section from cursor
        show_index = 0
        current_section = toc.get_section_from_cursor()
        if current_section:
            show_index = current_section['index']
        # Store position for returning to
        return_to = []
        for each in view.sel():
            return_to.append(each)
        toc.return_to = return_to
        # Pop up the panel
        titles = toc.get_comment_titles('string')
        self.window = sublime.active_window()
        if sys.version_info < (3, 0):
            self.window.show_quick_panel(titles, toc.on_list_selected_done)
        else:
            self.window.show_quick_panel(  # Pass on_highlighted callback
                titles, toc.on_list_selected_done, False, show_index,
                toc.on_list_selected_done)
        toc._debug_stop('Show quick panel')

    # >> Up down
    # Allows moving up and down through comments
    def traverse_comments(self, toc, move):
        view = self.view
        titles = toc.get_comment_titles()
        sel = view.sel()
        if len(sel) == 1:
            current_line_no, col_no = view.rowcol(sel[0].b)
            for x in range(len(titles)):
                item = titles[x]
                if move == 'up':  # moving up
                    if item['line'] < current_line_no:
                        if x+1 < len(titles):
                            if titles[x+1]['line'] >= current_line_no:
                                return toc.on_list_selected_done(x)
                        else:
                            return toc.on_list_selected_done(x)
                else:  # moving down
                    if item['line'] > current_line_no:
                        return toc.on_list_selected_done(x)

    # >> Fold comments
    def fold_comments(self, toc, fold, unfold):
        comments = self.view.find_by_selector('comment')
        titles = toc.get_comment_titles()
        is_all = fold == 'all' or unfold == 'all'
        # Current selection
        sels = self.view.sel()
        for each in sels:
            sel = each
        # Get content regions to fold
        fold_regions = []
        sections = toc.get_plugin_sections()
        for each in sections:
            title_region = each['title_region']
            content_region = each['content_region']
            if title_region.contains(sel) or is_all:
                fold_regions.append(content_region)
            elif content_region.contains(sel):
                fold_regions.append(content_region)
        # Fold, unfold or toggle
        if fold is not None:
            self.view.fold(fold_regions)
        elif unfold is not None:
            self.view.unfold(fold_regions)
        elif self.view.fold(fold_regions) is False:
            self.view.unfold(fold_regions)


#
# > Plugin class
#
class TableOfComments:

    def __init__(self, view, edit):
        self.view = view
        self.edit = edit

#
# Debug timing functions
#
#
    timers = {}

    def _debug_start(self, ref):
        self.timers[ref] = time.time()

    def _debug_stop(self, ref):
        start_time = self.timers[ref]
        duration = time.time() - start_time
        self.timers[ref] = duration

#
# Table TOC tag
#

    def get_toc_region(self, view):
        title = get_setting('toc_title', str)
        pattern = r'\/\*(\s|\*)*'+title+r'[^\/]*\/'
        matches = view.find_all(pattern)
        for region in (matches):
            if self.is_scope_or_comment(view, region):
                return region
        return None

    def is_in_toc_region(self, view, region):
        toc_region = self.get_toc_region(view)
        if toc_region:
            if region.a > toc_region.a and region.a < toc_region.b:
                return True
        return False

    def create_toc(self):
        view = self.view
        edit = self.edit
        region = self.get_toc_region(view)
        if region:
            toc = self.compile_toc(view)
            existing = view.substr(region)
            if existing != toc:
                view.replace(edit, region, toc)

    def compile_toc(self, view):
        self._debug_start('compile-toc')
        titles = self.get_comment_titles('string')
        title = get_setting('toc_title', str)
        start = get_setting('toc_start', str)
        line = get_setting('toc_line', str)
        end = get_setting('toc_end', str)
        front = "\n" + line
        output = start + front + title + front.rstrip()
        for title in titles:
            comment_level = title.count('-') + 1
            try:
                level = int(get_setting('toc_level', int))
                if level >= comment_level:
                    output += front + title
            except TypeError:
                output += front + title
        output += "\n"+end
        self._debug_stop('compile-toc')
        return output

#
# >> Quick panel
#

    # Jump list quick menu selected
    def on_list_selected_done(self, picked):
        if picked == -1:
            self.view.sel().clear()
            for each in self.return_to:
                self.view.sel().add(each)
            self.view.show(self.view.sel())
        else:
            titles = self.get_comment_titles()
            title = titles[picked]
            row = title['line']
            point = self.view.text_point(row, 0)
            line_region = self.view.line(point)
            # Reference the 'text' within the line only
            text = title['text']
            text = re.escape(text)
            text = text.replace('\>', '>')  # ">" does not work when escaped
            text_region = self.view.find(text, line_region.a)
            # Use goto_line to move the document then highlight
            if sublime.active_window().active_view():
                sublime.active_window().active_view().run_command(
                    "goto_line", {"line": int(title['line'])}
                    )
            self.view.sel().clear()
            self.view.sel().add(text_region)

#
# >> Parse
#

    # Core parse function (returned as dict or list)
    def get_comment_titles(self, format='dict', test=None):
        self._debug_start('get-comment-titles')
        view = self.view
        level_char = get_setting('level_char', str)
        comment_chars = get_setting('comment_chars', str)
        escaped_chars = re.escape(comment_chars)
        comment = list(comment_chars)
        comment = 'DIV'.join(comment_chars)
        start = r'\s|'+re.escape(comment).replace('DIV', '|')
        # build the pattern to match the comment
        pattern = r'^('+start+')*?('+format_pattern(level_char)+'+)\s*' + \
            r'([^'+escaped_chars+']+)('+start+')*?$'

        matches = view.find_all(pattern)
        results = []
        toc_title = get_setting('toc_title', str)

        for match in matches:
            bits = view.lines(match)  # go through each line
            for region in bits:
                # Ensure it's comment or source
                if not self.is_scope_or_comment(view, region):
                    continue
                # Ensure not in toc region already
                if self.is_in_toc_region(view, region):
                    continue

                line = view.substr(region)
                line_match = re.match(pattern, line)

                if not line_match:
                    continue

                if level_char in line:
                    # Add the level chars
                    label = line_match.group(2)

                    # Replace level char with toc char
                    label = self.replace_level_chars(label)
                    if label != '':
                        label += ' '

                    # append the heading text
                    text = line_match.group(3).strip()
                    label += text

                    # Get the position
                    if line != '' and line != toc_title:
                        line_no, col_no = view.rowcol(region.b)
                        if format == 'dict':
                            results.append(
                                {'label': label, 'text': text,
                                    'region': region, 'line': line_no})
                        else:
                            results.append(label)
        self._debug_stop('get-comment-titles')
        return results

#
# >> Plugin sections (regions)
#

    # Returns list of sections dicts with all related values
    def get_plugin_sections(self):
        comments = self.view.find_by_selector('comment')
        titles = self.get_comment_titles()
        # Only get comment blocks with titles within them
        sections = []
        for i in range(len(comments)):
            comment = comments[i]
            for title in titles:
                if comment.contains(title['region']):
                    title['title_region'] = comment
                    sections.append(title)
        # Get the fold regions (content blocks)
        output = []
        for i in range(len(sections)):
            section = sections[i]
            section['index'] = i
            region = section['title_region']
            for title in titles:
                if region.contains(title['region']):
                    fold_start = region.b + 1
                    fold_end = self.view.size()
                    if i < len(sections)-1:
                        fold_end = sections[i+1]['region'].a - 1
                    content_region = sublime.Region(fold_start, fold_end)
                    section['content_region'] = content_region
            output.append(section)
        return output

    # Returns the title and content region from cursor
    def get_section_from_cursor(self):
        # Current selection
        sels = self.view.sel()
        for each in sels:
            sel = each
        # Find within sections
        sections = self.get_plugin_sections()
        for section in sections:
            if section['title_region'].contains(sel) \
                    or section['content_region'].contains(sel):
                return section
        return False

    # Only find titles within genuine comments
    # This will no doubt need to be improved over time for various syntaxes
    # ('string.quoted' makes python """ comments """ not trigger)
    def is_scope_or_comment(self, view, region):
        line = view.substr(region)
        # Trim to scope
        # If line starts with whitespace, the syntax returned is "source" not
        # "comment" for the initial char
        trimmed = line.lstrip()
        diff = len(line) - len(trimmed)
        scope = view.scope_name(region.a + diff)
        # Check out scope
        comments_scope = ['comment']
        disallow = ['string.quoted']
        for each in comments_scope:
            if scope.find(each) < 0:
                return False
        for each in disallow:
            if scope.find(each) > 0:
                return False
        return True

    def replace_level_chars(self, line):
        level_char = get_setting('level_char', str)
        toc_char = get_setting('toc_char', str)
        # remove the last char so level one has no indent
        line = line[:-1].replace(level_char, toc_char)
        return line


#
# Helpers
#

def format_pattern(pattern):
    pattern = re.escape(pattern)
    pattern = pattern.replace('\>', '>')
    return pattern


def get_setting(name, typeof=str):
    settings = sublime.load_settings('tableofcomments.sublime-settings')
    setting = settings.get(name)
    if setting:
        if typeof == str:
            return setting
        if typeof == bool:
            return setting is True
        elif typeof == int:
            return int(settings.get(name, 500))
    else:
        if typeof == str:
            return ''
        else:
            return None


#
# Testing infrastructure
#

if sys.version_info < (3, 0):
    import tests
else:
    from . import tests


class table_of_comments_run_tests_command(sublime_plugin.TextCommand):
    def run(self, edit):
        reload_test_bootstrap()
        tests.run(self.view, edit)


# For developing, reload tests.* which in turn reloads it's sub packages
basedir = os.getcwd()


def reload_test_bootstrap():
    os.chdir(basedir)
    path = 'tests'
    if sys.version_info < (3, 0):
        __import__(path)
        sys.modules[path] = reload(sys.modules[path])
    else:
        imp.reload(eval(path))
