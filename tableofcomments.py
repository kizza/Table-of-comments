import sublime, sublime_plugin, re

""" Plugin to create a quick panel lookup that lets you jump between comment titles"""

#
# Text Commands
#
#from datetime import date
class table_of_comments_command(sublime_plugin.TextCommand):
	def run(self, edit):
		view = self.view
		self.create_toc(view, edit);
		titles = self.get_comment_titles(view, 'string')
		self.disabled_packages = titles
		self.window = sublime.active_window()
		self.window.show_quick_panel(self.disabled_packages, self.on_list_selected_done)

	def create_toc(self, view, edit):
		title = get_setting('toc_title', str)
		pattern = r'\/\*(\s|\*)*'+title+r'[^\/]*\/'
		matches = view.find_all(pattern)
		for region in (matches):
			toc = self.compile_toc(view)
			view.replace(edit, sublime.Region(region.a, region.b), toc)

	def compile_toc(self, view):
		titles = self.get_comment_titles(view, 'string')
		title  = get_setting('toc_title', str)
		start  = get_setting('toc_start', str)
		line   = get_setting('toc_line', str)
		end    = get_setting('toc_end', str)
		level  = get_setting('toc_level', int)
		front  = "\n"+ line
		output = start + front + title + front	
		for title in titles:
			l = 1
			if ' -- ' in title:
				l = 3
			elif ' - ' in title:
				l = 2;
			if level >= l:
				output+= front + title
		output+= "\n"+end
		return output

	def on_list_selected_done(self, picked):
		if picked == -1:
			return
		titles = self.get_comment_titles(self.view)
		row = titles[picked]['line']
		point = self.view.text_point(row, 0)
		line_region = self.view.line(point)
		self.view.sel().clear()
		self.view.sel().add(line_region.b)
		self.view.show_at_center(line_region.b)	

	def get_comment_titles(self, view, format='dict'):
		level1 = get_setting('level_1_char', str)
		level2 = get_setting('level_2_char', str)
		level3 = get_setting('level_3_char', str)

		comment_chars = get_setting('comment_chars', str)
		comment_chars = list(comment_chars)
		comment       = '|'.join(comment_chars)
		start         = '\s|'+re.escape(comment).replace('\|', '|')

		pattern = '^('+start+')*?('+format_pattern(level1)+'|'+format_pattern(level2)+'|'+format_pattern(level3)+')\s*?(\w|\s)+('+start+')*?$'
		matches = view.find_all(pattern)
		results = []
		for region in matches:
			# Ensure it's comment or source
			scope = view.scope_name(region.a)
			if scope.find('comment.') < 0 and scope.find('source.') < 0:
				continue
			line = view.substr(view.line(region.b))
			line = view.substr(sublime.Region(region.a, view.line(region.b).b))
			if level1 in line or level2 in line or level3 in line:

				# Format the line as a label
				line = line.replace('/*', '').replace('*/', '')
				for char in comment_chars:
					line = line.replace(char, '')
				if level3 in line:
					line = ' -- '+line.replace(level3, '').strip()
				elif level2 in line:
					line = ' - '+line.replace(level2, '').strip()
				elif level1 in line:
					line = ''+line.replace(level1, '').strip()

				# Get the position
				line_no, col_no = view.rowcol(region.b)
				if format == 'dict':
					results.append( {'label':line, 'line':line_no} )
				else:
					results.append( line )
		return results

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
			return setting == True
		elif typeof == int:
			return int(settings.get(name, 500))
	else:
		if typeof == str:
			return ''
		else:
			return None