#!/usr/bin/env python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2013 Christopher Bratusek		#
#							#
#########################################################

MODULES = [ 'os', 'os.path', 'sys', 'locale', 'gettext', 'string', 'shutil',
            'ctypes', 'optparse', 'subprocess', 'undobuffer', 'commands',
	   'i18n', 'misc', 'lockfile', 'config', 'widgethandler', 'dicts',
	   'prompts' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

try:
	from gi.repository import Gtk
except ImportError:
	FAILED.append("Gtk (from gi.repository)")

if FAILED:
    print "The following modules failed to import: %s" % (" ".join(FAILED))
    sys.exit(1)

PREFIX = os.getenv('BSNG_UI_PREFIX')

parser = optparse.OptionParser("bashstyle <option> [value]\
				\n\nBashStyle-NG (c) 2007 - 2013 Christopher Bratusek\
				\nLicensed under the GNU GENERAL PUBLIC LICENSE v3")

if sys.platform == 'linux2':
	try:
		libc = ctypes.CDLL('libc.so.6')
		libc.prctl(15, 'bashstyle', 0, 0, 0)
	except:
		pass

parser.add_option("-v", "--version", dest="version",
                  action="store_true", default=False, help="print version and exit")

parser.add_option("-p", "--prefix", dest="prefix",
                  action="store_true", default=False, help="print prefix and exit")

parser.add_option("-g", "--group", dest="group", default="style",
                  help="display a given group of options at startup, one of:\
                  \nstyle, alias, advanced, readline, vim, nano, ls or custom")

(options, args) = parser.parse_args()

if options.version:
		print "%s" % os.getenv('BSNG_UI_VERSION')
		sys.exit(0)

if options.prefix:
		print "%s" % os.getenv('BSNG_UI_PREFIX')
		sys.exit(0)

groups = {
	  "style" : "0",
	  "alias" : "1",
	  "advanced" : "2",
	  "readline" : "3",
	  "vim" : "5",
	  "nano" : "6",
	  "ls" : "7",
	  "custom" : "8",
	 }

initial_page = groups[options.group]
app_ini_version = 2

lock = lockfile.LockFile()
config = config.Config()

class BashStyleNG(object):

	def __init__(self):
		lock.Write()

		######################## handle ConfigObj ##########################################
		config.InitConfig()
		config.LoadConfig()
		config.UpdateConfig()

		######################## cd into $HOME #############################################
		os.chdir(os.getenv("HOME"))

		######################## load translations & widgethandler #########################
		gtkbuilder = widgethandler.gtkbuilder
		lang = i18n.Gettext()
		lang.SetLang()
		
		WidgetHandler = widgethandler.WidgetHandler()

		####################### Style Options ##############################################
		WidgetHandler.InitWidget("use_bashstyle", "Style", "use_bashstyle", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("colored_prompts", "Style", "enable_colors", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_color", "Style", "colored_ls", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("manpage_color", "Style", "colored_man", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("grep_color", "Style", "colored_grep", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("random_style", "Style", "random_style", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("prompt_style", "Style", "prompt_style", "combo", dicts.prompt_styles, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("color_style", "Style", "color_style", "combo", dicts.color_styles, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("terminfo", "Style", "man_style", "combo", dicts.man_styles, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("grep_colour", "Style", "grep_color", "combo", dicts.grep_colors, config.cfo, config.udc, config.fdc)

		# special combobox not (yet) handled by widgethandler.py
		self.color_of = gtkbuilder.get_object("color_of")
		self.color_to = gtkbuilder.get_object("color_to")

		self.color_of.set_active(0)
		self.color_to.set_active(0)

		def change_color(widget, data=None):
			color_set = self.color_of.get_active()
			color_is = self.color_to.get_active()
			if color_set != 0 and color_is != 0:
				config.cfo["Style"][dicts.color_keys[color_set]] = dicts.colors[color_is]
				self.color_to.set_active(0)
				self.color_of.set_active(0)

		self.color_of.connect("changed", change_color)
		self.color_to.connect("changed", change_color)

		####################### Aliases ####################################################
		WidgetHandler.InitWidget("alias1", "Alias", "alias_one", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias2", "Alias", "alias_two", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias3", "Alias", "alias_three", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias4", "Alias", "alias_four", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias5", "Alias", "alias_five", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias6", "Alias", "alias_six", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias7", "Alias", "alias_seven", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias8", "Alias", "alias_eight", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias9", "Alias", "alias_nine", "text", None, config.cfo, config.udc, config.fdc)

		####################### Advanced Stuff #############################################
		WidgetHandler.InitWidget("history_blacklist", "Advanced", "history_ignore", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("separator", "Advanced", "separator", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ps234", "Advanced", "ps234", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("pwd_cutter", "Advanced", "pwdcut", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("cdpath", "Advanced", "cdpath", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("completion_blacklist", "Advanced", "completion_ignore", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("fcedit", "Advanced", "fcedit", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("welcome", "Advanced", "welcome_message", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("path", "Advanced", "path", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("history_size", "Advanced", "history_size", "int", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("pwd_len", "Advanced", "pwdlength", "int", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("timeout", "Advanced", "timeout", "int", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("history_control", "Advanced", "history_control", "combo", dicts.history_types, config.cfo, config.udc, config.fdc)

		self.reset_history = gtkbuilder.get_object("reset_history")

		def do_reset_history(widget, data=None):
			os.remove(os.path.expanduser("~/.bash_history"))

		self.reset_history.connect("clicked", do_reset_history)

		####################### Readline stuff #############################################
		WidgetHandler.InitWidget("readline", "Readline", "use_readlinecfg", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("completion", "Readline", "completion", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ambiguous", "Readline", "ambiguous_show", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("match_hidden", "Readline", "complete_hidden", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ignore_case", "Readline", "ignore_case", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("query_items", "Readline", "query_items", "int", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("completion_hz", "Readline", "complete_horizontal", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("mark_dirs", "Readline", "mark_directories", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("mark_symdirs", "Readline", "mark_symbolic_directories", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vstats", "Readline", "visible_stats", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("scroll_hz", "Readline", "scroll_horizontal", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("modlines", "Readline", "mark_modified", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("bellstyle", "Readline", "bellstyle", "combo", dicts.bell_styles, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("editmode", "Readline", "editing_mode", "combo", dicts.edit_modes, config.cfo, config.udc, config.fdc)

		######################## Separator Stuff ###########################################
		WidgetHandler.InitWidget("show_files_amount", "Separator", "files_amount", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_uptime", "Separator", "uptime", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_file_size", "Separator", "files_size", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_tty", "Separator", "tty", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_processes", "Separator", "processes", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_load", "Separator", "load", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_battery", "Separator", "battery_load", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("show_mem", "Separator", "mem", "combo", dicts.memory_types, config.cfo, config.udc, config.fdc)

		######################## Extra Stuff ###############################################
		WidgetHandler.InitWidget("dirchar", "Extra", "directory_indicator", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("tabrotate", "Extra", "tab_rotation", "bool", None, config.cfo, config.udc, config.fdc)
		
		######################## Shopt Stuff ###############################################
		WidgetHandler.InitWidget("histappend", "Shopt", "histappend", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("cdspell", "Shopt", "cdspell", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("cdable_vars", "Shopt", "cdable_vars", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("checkhash", "Shopt", "checkhash", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("cmdhist", "Shopt", "cmdhist", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("force_fignore", "Shopt", "force_fignore", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("histreedit", "Shopt", "histreedit", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("no_empty_cmd", "Shopt", "no_empty_cmd_completion", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("autocd", "Shopt", "autocd", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("checkjobs", "Shopt", "checkjobs", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("globstar", "Shopt", "globstar", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("dirspell", "Shopt", "dirspell", "bool", None, config.cfo, config.udc, config.fdc)

		######################## VimCFG Stuff ##############################################
		WidgetHandler.InitWidget("use_vimcfg", "Vim", "use_vimcfg", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_backup", "Vim", "vim_backup", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_jump", "Vim", "jump_back", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_sline", "Vim", "start_line", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_tabstop", "Vim", "tab_length", "int", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_autowrap", "Vim", "wrap_length", "int", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_wrap", "Vim", "wrap_line", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_cd", "Vim", "chdir", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_indent", "Vim", "filetype_indent", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_cmd", "Vim", "show_command", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_match", "Vim", "highlight_matches", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_syntax", "Vim", "syntax_hilight", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_bg", "Vim", "dark_background", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_icase", "Vim", "ignore_case", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_scase", "Vim", "smart_case", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_isearch", "Vim", "incremental_search", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_hilight", "Vim", "highlight_brackets", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_number", "Vim", "show_lineno", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_save", "Vim", "autosave", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_hiline", "Vim", "highlight_line", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_hicol", "Vim", "highlight_column", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_ruler", "Vim", "ruler", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_rulerformat", "Vim", "rulerformat", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_colorscheme", "Vim", "colorscheme", "combo", dicts.vim_colors, config.cfo, config.udc, config.fdc)

		######################## NanoCFG Stuff #############################################
		WidgetHandler.InitWidget("use_nanocfg", "Nano", "use_nanocfg", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_backup", "Nano", "nano_backup", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_const", "Nano", "show_position", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_indent", "Nano", "auto_indent", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_colors", "Nano", "syntax_highlight", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_nohelp", "Nano", "hide_help", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_case", "Nano", "case_sensitive", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_boldtext", "Nano", "bold_text", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_morespace", "Nano", "more_space", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_history", "Nano", "history", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_rbdel", "Nano", "rebind_delete", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("nano_rbkp", "Nano", "rebind_keypad", "bool", None, config.cfo, config.udc, config.fdc)

		######################## LS Colors Stuff ###########################################
		WidgetHandler.InitWidget("ls_custom", "LSColors", "custom", "text", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("use_lscolors", "LSColors", "use_lscolors", "bool", None, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_exec", "LSColors", "exec", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_gen", "LSColors", "generic", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_log", "LSColors", "logs", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_deb", "LSColors", "deb", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_rpm", "LSColors", "rpm", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_dirs", "LSColors", "dirs", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_jpeg", "LSColors", "jpeg", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_png", "LSColors", "png", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_gif", "LSColors", "gif", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_mp3", "LSColors", "mp3", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_ogg", "LSColors", "ogg", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_flac", "LSColors", "flac", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_tar", "LSColors", "tar", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_targz", "LSColors", "targz", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_tarbz2", "LSColors", "tarbz2", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_zip", "LSColors", "zip", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ls_rar", "LSColors", "rar", "combo", dicts.ls_colors, config.cfo, config.udc, config.fdc)

		######################## Custom Prompt Builder #####################################
		WidgetHandler.InitWidget("use_custom_prompt", "Custom", "use_custom_prompt", "bool", None, config.cfo, config.udc, config.fdc)

		self.prompt_command = gtkbuilder.get_object("prompt_command")

		self.prompt_command_buffer = undobuffer.UndoableBuffer()
		self.prompt_command.set_buffer(self.prompt_command_buffer)
		self.prompt_command_buffer.set_text("%s" % config.cfo["Custom"]["command"])

		def set_prompt_command(widget, data=None):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			config.cfo["Custom"]["command"] = widget.get_text(start, end, False)

		self.prompt_command_buffer.connect("changed", set_prompt_command)

		self.active_buffer = "P_C"

		self.custom_prompt = gtkbuilder.get_object("custom_prompt")

		self.custom_prompt_buffer = undobuffer.UndoableBuffer()
		self.custom_prompt.set_buffer(self.custom_prompt_buffer)
		self.custom_prompt_buffer.set_text("%s" % config.cfo["Custom"]["prompt"])

		def set_custom_prompt(widget, data=None):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			config.cfo["Custom"]["prompt"] = widget.get_text(start, end, False)

		self.custom_prompt_buffer.connect("changed", set_custom_prompt)

		self.place_p_c = gtkbuilder.get_object("place_p_c")

		def do_place_p_c(widget, data=None):
			self.prompt_command.set_sensitive(1)
			self.custom_prompt.set_sensitive(0)
			self.active_buffer = "P_C"

		self.place_p_c.connect("clicked", do_place_p_c)

		self.place_ps1 = gtkbuilder.get_object("place_ps1")

		def do_place_ps1(widget, data=None):
			self.prompt_command.set_sensitive(0)
			self.custom_prompt.set_sensitive(1)
			self.active_buffer = "PS1"

		self.place_ps1.connect("clicked", do_place_ps1)

		def prompt_add(text):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.insert_at_cursor(text)
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.insert_at_cursor(text)

		def prompt_set(text):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.set_text(text)
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.set_text(text)

		self.show_toolbox = gtkbuilder.get_object("show_toolbox")

		def do_show_toolbox(widget, data=None):
			toolbox = gtkbuilder.get_object("Toolbox")
			toolbox.show_all()
			toolbox.connect("delete-event", lambda w, e: w.hide() or True)

		self.show_toolbox.connect("clicked", do_show_toolbox)

		self.username = gtkbuilder.get_object("username")

		def set_username(widget, data=None):
			prompt_add("\\u")

		self.username.connect("clicked", set_username)

		self.hostname = gtkbuilder.get_object("hostname")

		def set_hostname(widget, data=None):
			prompt_add("\\h")

		self.hostname.connect("clicked", set_hostname)

		self.fhostname = gtkbuilder.get_object("fhostname")

		def set_fhostname(widget, data=None):
			prompt_add("\\H")

		self.fhostname.connect("clicked", set_fhostname)

		self.time = gtkbuilder.get_object("time")

		def set_time(widget, data=None):
			prompt_add("\\t")

		self.time.connect("clicked", set_time)

		self.date = gtkbuilder.get_object("date")

		def set_date(widget, data=None):
			prompt_add("\\d")

		self.date.connect("clicked", set_date)

		self.sign = gtkbuilder.get_object("sign")

		def set_sign(widget, data=None):
			prompt_add("\\$")

		self.sign.connect("clicked", set_sign)

		self.fworkdir = gtkbuilder.get_object("fworkdir")

		def set_fworkdir(widget, data=None):
			prompt_add("\\w")

		self.fworkdir.connect("clicked", set_fworkdir)

		self.workdir = gtkbuilder.get_object("workdir")

		def set_workdir(widget, data=None):
			prompt_add("\\W")

		self.workdir.connect("clicked", set_workdir)

		self.euid = gtkbuilder.get_object("euid")

		def set_euid(widget, data=None):
			prompt_add("\\$EUID")

		self.euid.connect("clicked", set_euid)

		self.jobs = gtkbuilder.get_object("jobs")

		def set_jobs(widget, data=None):
			prompt_add("\\j")

		self.jobs.connect("clicked", set_jobs)

		self.bang = gtkbuilder.get_object("bang")

		def set_bang(widget, data=None):
			prompt_add("\\!")

		self.bang.connect("clicked", set_bang)

		self.number = gtkbuilder.get_object("number")

		def set_number(widget, data=None):
			prompt_add("\\#")

		self.number.connect("clicked", set_number)

		self.pid = gtkbuilder.get_object("pid")

		def set_pid(widget, data=None):
			prompt_add("$BASHPID")

		self.pid.connect("clicked", set_pid)

		self.shlvl = gtkbuilder.get_object("shlvl")

		def set_shlvl(widget, data=None):
			prompt_add("$SHLVL")

		self.shlvl.connect("clicked", set_shlvl)

		self.truncpwd = gtkbuilder.get_object("truncpwd")

		def set_truncpwd(widget, data=None):
			prompt_add("\\$(trunc_pwd)")

		self.truncpwd.connect("clicked", set_truncpwd)

		self.showsize = gtkbuilder.get_object("showsize")

		def set_showsize(widget, data=None):
			prompt_add("\\$(show_size)")

		self.showsize.connect("clicked", set_showsize)

		self.countfiles = gtkbuilder.get_object("countfiles")
		self.countfiles.set_active(0)

		def set_countfiles(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(dicts.counters[selection])

		self.countfiles.connect("changed", set_countfiles)

		self.countprocesses = gtkbuilder.get_object("countprocesses")

		def set_countprocesses(widget, data=None):
			prompt_add("\\$(count_processes)")

		self.countprocesses.connect("clicked", set_countprocesses)

		self.showuptime = gtkbuilder.get_object("showuptime")

		def set_showuptime(widget, data=None):
			prompt_add("\\$(show_uptime)")

		self.showuptime.connect("clicked", set_showuptime)

		self.showload = gtkbuilder.get_object("showload")
		self.showload.set_active(0)

		def set_showload(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(dicts.load_getters[selection])

		self.showload.connect("changed", set_showload)

		self.showtty = gtkbuilder.get_object("showtty")

		def set_showtty(widget, data=None):
			prompt_add("\\$(showtty)")

		self.showtty.connect("clicked", set_showtty)

		self.showmem = gtkbuilder.get_object("showmem")
		self.showmem.set_active(0)

		def set_showmem(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(dicts.memory_getters[selection])

		self.showmem.connect("changed", set_showmem)

		self.showcpuload = gtkbuilder.get_object("showcpuload")

		def set_showcpuload(widget, data=None):
			prompt_add("\\$(show_cpu_load)")

		self.showcpuload.connect("clicked", set_showcpuload)

		self.showbatteryload = gtkbuilder.get_object("showbatteryload")
		self.showbatteryload.set_active(0)

		def set_showbatteryload(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(dicts.battery_getters[selection])

		self.showbatteryload.connect("changed", set_showbatteryload)

		self.showspace = gtkbuilder.get_object("showspace")
		self.showspace.set_active(0)

		def set_showspace(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(dicts.space_getters[selection])

		self.showspace.connect("changed", set_showspace)

		self.showseconds = gtkbuilder.get_object("showseconds")

		def set_showseconds(widget, data=None):
			prompt_add("${SECONDS}")

		self.showseconds.connect("clicked", set_showseconds)

		self.empty_pc = gtkbuilder.get_object("empty_pc")

		def do_empty_pc(widget, data=None):
			self.prompt_command_buffer.set_text("")

		self.empty_pc.connect("clicked", do_empty_pc)

		self.undo_pc = gtkbuilder.get_object("undo_pc")

		def do_undo_pc(widget, data=None):
			self.prompt_command_buffer.undo()

		self.undo_pc.connect("clicked", do_undo_pc)

		self.redo_pc = gtkbuilder.get_object("redo_pc")

		def do_redo_pc(widget, data=None):
			self.prompt_command_buffer.redo()

		self.redo_pc.connect("clicked", do_redo_pc)

		self.empty_ps1 = gtkbuilder.get_object("empty_ps1")

		def do_empty_ps1(widget, data=None):
			self.custom_prompt_buffer.set_text("")

		self.empty_ps1.connect("clicked", do_empty_ps1)

		self.undo_ps1 = gtkbuilder.get_object("undo_ps1")

		def do_undo_ps1(widget, data=None):
			self.custom_prompt_buffer.undo()

		self.undo_ps1.connect("clicked", do_undo_ps1)

		self.redo_ps1 = gtkbuilder.get_object("redo_ps1")

		def do_redo_ps1(widget, data=None):
			self.custom_prompt_buffer.redo()

		self.redo_ps1.connect("clicked", do_redo_ps1)

		self.insert_color = gtkbuilder.get_object("insert_color")
		self.insert_color.set_active(0)

		def do_insert_color(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(dicts.symbolic_colors[selection])

		self.insert_color.connect("changed", do_insert_color)

		self.insert_prompt = gtkbuilder.get_object("insert_prompt")
		self.insert_prompt.set_active(0)

		styles_pc = {
			      1 : prompts.empty_pc,
			      2 : prompts.empty_pc,
			      3 : prompts.floating_clock_pc,
			      4 : prompts.clock_advanced_pc,
			      5 : prompts.empty_pc,
			      6 : prompts.poweruser_pc,
			      7 : prompts.empty_pc,
			      8 : prompts.empty_pc,
			      9 : prompts.empty_pc,
			     10 : prompts.empty_pc,
			     11 : prompts.empty_pc,
			     12 : prompts.ayoli_pc,
			    }

		styles_ps1 = {
			       1 : prompts.separator_ps,
			       2 : prompts.vector_ps,
			       3 : prompts.floating_clock_ps,
			       4 : prompts.clock_advanced_ps,
			       5 : prompts.elite_ps,
			       6 : prompts.poweruser_ps,
			       7 : prompts.dirks_ps,
			       8 : prompts.dotprompt_ps,
			       9 : prompts.sepang_ps,
			      10 : prompts.quirk_ps,
			      11 : prompts.sputnik_ps,
			      12 : prompts.ayoli_ps,
			     }

		def do_insert_prompt(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				self.prompt_command_buffer.set_text(styles_pc[selection])
				self.custom_prompt_buffer.set_text(styles_ps1[selection])

		self.insert_prompt.connect("changed", do_insert_prompt)

		######################## Load the Main-Window ######################################
		self.bashstyle = gtkbuilder.get_object("bashstyle")

		def destroy(self, widget):
			config.WriteConfig()
			lock.Remove()
			Gtk.main_quit()

		self.bashstyle.connect("destroy", destroy, None)

		######################## Load the Notebook #########################################
		notebook = gtkbuilder.get_object("notebook")
		notebook.set_current_page(int(initial_page))

		######################## Load last two buttons #####################################
		self.show_doc = gtkbuilder.get_object("show_doc")

		def show_documentation(widget, data=None):
			subprocess.Popen("x-www-browser " + PREFIX + "/share/doc/bashstyle-ng/index.html", shell=True)

		self.show_doc.connect("clicked", show_documentation, None)

		self.show_about = gtkbuilder.get_object("show_about")

		def show_aboutdialog(widget, data=None):
			aboutdialog = gtkbuilder.get_object("aboutdialog")
			aboutdialog.show_all()
			aboutdialog.connect("response", lambda w, e: w.hide() or True)
			aboutdialog.connect("delete-event", lambda w, e: w.hide() or True)

		self.show_about.connect("clicked", show_aboutdialog, None)

		self.bashstyle.show

if __name__ == "__main__":
	lock.Check()
	hwg = BashStyleNG()
	Gtk.main()
