#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2014 Christopher Bratusek		#
#							#
#########################################################

MODULES = [ 'os', 'os.path', 'sys', 'locale', 'gettext', 'string', 'shutil',
            'ctypes', 'optparse', 'subprocess', 'undobuffer', 'i18n', 'misc',
	    'lockfile', 'config', 'widgethandler', 'dicts', 'prompts',
	    'promptbuilder', 'args' ]

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
    print("The following modules failed to import: %s" % (" ".join(FAILED)))
    sys.exit(1)

PREFIX = os.getenv('BSNG_UI_PREFIX')
DOCDIR = os.getenv('BSNG_DOCDIR')
DATDIR = os.getenv('BSNG_DATADIR')

args.CmdArgs()
initial_page = dicts.groups[args.CmdArgs.options.group]

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

		WidgetHandler = widgethandler.WidgetHandler(config.cfo, config.udc, config.fdc)

		####################### Style Options ##############################################
		WidgetHandler.InitWidget("use_bashstyle", "Style", "use_bashstyle", "bool", None)
		WidgetHandler.InitWidget("colored_prompts", "Style", "enable_colors", "bool", None)
		WidgetHandler.InitWidget("ls_color", "Style", "colored_ls", "bool", None)
		WidgetHandler.InitWidget("manpage_color", "Style", "colored_man", "bool", None)
		WidgetHandler.InitWidget("grep_color", "Style", "colored_grep", "bool", None)
		WidgetHandler.InitWidget("random_style", "Style", "random_style", "bool", None)
		WidgetHandler.InitWidget("prompt_style", "Style", "prompt_style", "combo", dicts.prompt_styles)
		WidgetHandler.InitWidget("color_style", "Style", "color_style", "combo", dicts.color_styles)
		WidgetHandler.InitWidget("terminfo", "Style", "man_style", "combo", dicts.man_styles)
		WidgetHandler.InitWidget("grep_colour", "Style", "grep_color", "combo", dicts.grep_colors)
		WidgetHandler.InitWidget("colorshell", "Style", "colorshell", "bool", None)
		WidgetHandler.InitWidget("colorshell_reset", "Style", "colorshell_reset", "bool", None)

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
		WidgetHandler.InitWidget("alias1", "Alias", "alias_one", "text", None)
		WidgetHandler.InitWidget("alias2", "Alias", "alias_two", "text", None)
		WidgetHandler.InitWidget("alias3", "Alias", "alias_three", "text", None)
		WidgetHandler.InitWidget("alias4", "Alias", "alias_four", "text", None)
		WidgetHandler.InitWidget("alias5", "Alias", "alias_five", "text", None)
		WidgetHandler.InitWidget("alias6", "Alias", "alias_six", "text", None)
		WidgetHandler.InitWidget("alias7", "Alias", "alias_seven", "text", None)
		WidgetHandler.InitWidget("alias8", "Alias", "alias_eight", "text", None)
		WidgetHandler.InitWidget("alias9", "Alias", "alias_nine", "text", None)

		####################### Advanced Stuff #############################################
		WidgetHandler.InitWidget("history_blacklist", "Advanced", "history_ignore", "text", None)
		WidgetHandler.InitWidget("separator", "Advanced", "separator", "text", None)
		WidgetHandler.InitWidget("ps234", "Advanced", "ps234", "text", None)
		WidgetHandler.InitWidget("pwd_cutter", "Advanced", "pwdcut", "text", None)
		WidgetHandler.InitWidget("cdpath", "Advanced", "cdpath", "text", None)
		WidgetHandler.InitWidget("completion_blacklist", "Advanced", "completion_ignore", "text", None)
		WidgetHandler.InitWidget("fcedit", "Advanced", "fcedit", "text", None)
		WidgetHandler.InitWidget("welcome", "Advanced", "welcome_message", "text", None)
		WidgetHandler.InitWidget("path", "Advanced", "path", "text", None)
		WidgetHandler.InitWidget("history_size", "Advanced", "history_size", "int", None)
		WidgetHandler.InitWidget("pwd_len", "Advanced", "pwdlength", "int", None)
		WidgetHandler.InitWidget("timeout", "Advanced", "timeout", "int", None)
		WidgetHandler.InitWidget("history_control", "Advanced", "history_control", "combo", dicts.history_types)

		self.reset_history = gtkbuilder.get_object("reset_history")

		def do_reset_history(widget, data=None):
			os.remove(os.path.expanduser("~/.bash_history"))

		self.reset_history.connect("clicked", do_reset_history)

		####################### Readline stuff #############################################
		WidgetHandler.InitWidget("readline", "Readline", "use_readlinecfg", "bool", None)
		WidgetHandler.InitWidget("completion", "Readline", "completion", "bool", None)
		WidgetHandler.InitWidget("ambiguous", "Readline", "ambiguous_show", "bool", None)
		WidgetHandler.InitWidget("match_hidden", "Readline", "complete_hidden", "bool", None)
		WidgetHandler.InitWidget("ignore_case", "Readline", "ignore_case", "bool", None)
		WidgetHandler.InitWidget("query_items", "Readline", "query_items", "int", None)
		WidgetHandler.InitWidget("completion_hz", "Readline", "complete_horizontal", "bool", None)
		WidgetHandler.InitWidget("mark_dirs", "Readline", "mark_directories", "bool", None)
		WidgetHandler.InitWidget("mark_symdirs", "Readline", "mark_symbolic_directories", "bool", None)
		WidgetHandler.InitWidget("vstats", "Readline", "visible_stats", "bool", None)
		WidgetHandler.InitWidget("scroll_hz", "Readline", "scroll_horizontal", "bool", None)
		WidgetHandler.InitWidget("modlines", "Readline", "mark_modified", "bool", None)
		WidgetHandler.InitWidget("bellstyle", "Readline", "bellstyle", "combo", dicts.bell_styles)
		WidgetHandler.InitWidget("editmode", "Readline", "editing_mode", "combo", dicts.edit_modes)
		WidgetHandler.InitWidget("show_editmode", "Readline", "show_editmode", "bool", None)

		######################## Separator Stuff ###########################################
		WidgetHandler.InitWidget("show_files_amount", "Separator", "files_amount", "bool", None)
		WidgetHandler.InitWidget("show_uptime", "Separator", "uptime", "bool", None)
		WidgetHandler.InitWidget("show_file_size", "Separator", "files_size", "bool", None)
		WidgetHandler.InitWidget("show_tty", "Separator", "tty", "bool", None)
		WidgetHandler.InitWidget("show_processes", "Separator", "processes", "bool", None)
		WidgetHandler.InitWidget("show_load", "Separator", "load", "bool", None)
		WidgetHandler.InitWidget("show_battery", "Separator", "battery_load", "bool", None)
		WidgetHandler.InitWidget("show_mem", "Separator", "mem", "combo", dicts.memory_types)

		######################## Extra Stuff ###############################################
		WidgetHandler.InitWidget("dirchar", "Extra", "directory_indicator", "text", None)
		WidgetHandler.InitWidget("tabrotate", "Extra", "tab_rotation", "bool", None)

		######################## Shopt Stuff ###############################################
		WidgetHandler.InitWidget("histappend", "Shopt", "histappend", "bool", None)
		WidgetHandler.InitWidget("cdspell", "Shopt", "cdspell", "bool", None)
		WidgetHandler.InitWidget("cdable_vars", "Shopt", "cdable_vars", "bool", None)
		WidgetHandler.InitWidget("checkhash", "Shopt", "checkhash", "bool", None)
		WidgetHandler.InitWidget("cmdhist", "Shopt", "cmdhist", "bool", None)
		WidgetHandler.InitWidget("force_fignore", "Shopt", "force_fignore", "bool", None)
		WidgetHandler.InitWidget("histreedit", "Shopt", "histreedit", "bool", None)
		WidgetHandler.InitWidget("no_empty_cmd", "Shopt", "no_empty_cmd_completion", "bool", None)
		WidgetHandler.InitWidget("autocd", "Shopt", "autocd", "bool", None)
		WidgetHandler.InitWidget("checkjobs", "Shopt", "checkjobs", "bool", None)
		WidgetHandler.InitWidget("globstar", "Shopt", "globstar", "bool", None)
		WidgetHandler.InitWidget("dirspell", "Shopt", "dirspell", "bool", None)
		WidgetHandler.InitWidget("direxpand", "Shopt", "direxpand", "bool", None)
		WidgetHandler.InitWidget("globasciiranges", "Shopt", "globasciiranges", "bool", None)

		######################## Extra Stuff ###############################################
		WidgetHandler.InitWidget("enable_lscd", "Extra", "use_lscd", "bool", None)
		WidgetHandler.InitWidget("lscd_options", "Extra", "lscd_opts", "text", None)
		WidgetHandler.InitWidget("cdwriter", "Extra", "cd_writer", "text", None)
		WidgetHandler.InitWidget("birthday", "Extra", "user_birthday", "text", None)
		WidgetHandler.InitWidget("dd_noerror", "Extra", "dd_noerror", "bool", None)
		WidgetHandler.InitWidget("restore_pwd", "Extra", "restore_directory", "bool", None)
		WidgetHandler.InitWidget("debug_verbose", "Extra", "debug_verbose", "bool", None)

		######################## GIT Stuff #################################################
		WidgetHandler.InitWidget("git_user", "Git", "git_user_name", "text", None)
		WidgetHandler.InitWidget("git_mail", "Git", "git_user_mail", "text", None)
		WidgetHandler.InitWidget("git_editor", "Git", "git_editor", "text", None)
		WidgetHandler.InitWidget("git_signkey", "Git", "git_signkey", "text", None)
		WidgetHandler.InitWidget("git_color", "Git", "git_color", "bool", None)
		WidgetHandler.InitWidget("git_aliases", "Git", "git_aliases", "bool", None)

		######################## VimCFG Stuff ##############################################
		WidgetHandler.InitWidget("use_vimcfg", "Vim", "use_vimcfg", "bool", None)
		WidgetHandler.InitWidget("vim_backup", "Vim", "vim_backup", "bool", None)
		WidgetHandler.InitWidget("vim_jump", "Vim", "jump_back", "bool", None)
		WidgetHandler.InitWidget("vim_sline", "Vim", "start_line", "bool", None)
		WidgetHandler.InitWidget("vim_tabstop", "Vim", "tab_length", "int", None)
		WidgetHandler.InitWidget("vim_autowrap", "Vim", "wrap_length", "int", None)
		WidgetHandler.InitWidget("vim_wrap", "Vim", "wrap_line", "bool", None)
		WidgetHandler.InitWidget("vim_cd", "Vim", "chdir", "bool", None)
		WidgetHandler.InitWidget("vim_indent", "Vim", "filetype_indent", "bool", None)
		WidgetHandler.InitWidget("vim_cmd", "Vim", "show_command", "bool", None)
		WidgetHandler.InitWidget("vim_match", "Vim", "highlight_matches", "bool", None)
		WidgetHandler.InitWidget("vim_syntax", "Vim", "syntax_hilight", "bool", None)
		WidgetHandler.InitWidget("vim_bg", "Vim", "dark_background", "bool", None)
		WidgetHandler.InitWidget("vim_icase", "Vim", "ignore_case", "bool", None)
		WidgetHandler.InitWidget("vim_scase", "Vim", "smart_case", "bool", None)
		WidgetHandler.InitWidget("vim_isearch", "Vim", "incremental_search", "bool", None)
		WidgetHandler.InitWidget("vim_hilight", "Vim", "highlight_brackets", "bool", None)
		WidgetHandler.InitWidget("vim_number", "Vim", "show_lineno", "bool", None)
		WidgetHandler.InitWidget("vim_save", "Vim", "autosave", "bool", None)
		WidgetHandler.InitWidget("vim_hiline", "Vim", "highlight_line", "bool", None)
		WidgetHandler.InitWidget("vim_hicol", "Vim", "highlight_column", "bool", None)
		WidgetHandler.InitWidget("vim_ruler", "Vim", "ruler", "bool", None)
		WidgetHandler.InitWidget("vim_rulerformat", "Vim", "rulerformat", "text", None)
		WidgetHandler.InitWidget("vim_colorscheme", "Vim", "colorscheme", "combo", dicts.vim_colors)

		######################## NanoCFG Stuff #############################################
		WidgetHandler.InitWidget("use_nanocfg", "Nano", "use_nanocfg", "bool", None)
		WidgetHandler.InitWidget("nano_backup", "Nano", "nano_backup", "bool", None)
		WidgetHandler.InitWidget("nano_const", "Nano", "show_position", "bool", None)
		WidgetHandler.InitWidget("nano_indent", "Nano", "auto_indent", "bool", None)
		WidgetHandler.InitWidget("nano_colors", "Nano", "syntax_highlight", "bool", None)
		WidgetHandler.InitWidget("nano_nohelp", "Nano", "hide_help", "bool", None)
		WidgetHandler.InitWidget("nano_case", "Nano", "case_sensitive", "bool", None)
		WidgetHandler.InitWidget("nano_boldtext", "Nano", "bold_text", "bool", None)
		WidgetHandler.InitWidget("nano_morespace", "Nano", "more_space", "bool", None)
		WidgetHandler.InitWidget("nano_history", "Nano", "history", "bool", None)
		WidgetHandler.InitWidget("nano_rbdel", "Nano", "rebind_delete", "bool", None)
		WidgetHandler.InitWidget("nano_rbkp", "Nano", "rebind_keypad", "bool", None)

		######################## LS Colors Stuff ###########################################
		WidgetHandler.InitWidget("ls_custom", "LSColors", "custom", "text", None)
		WidgetHandler.InitWidget("use_lscolors", "LSColors", "use_lscolors", "bool", None)
		WidgetHandler.InitWidget("ls_exec", "LSColors", "exec", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_gen", "LSColors", "generic", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_log", "LSColors", "logs", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_deb", "LSColors", "deb", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_rpm", "LSColors", "rpm", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_dirs", "LSColors", "dirs", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_jpeg", "LSColors", "jpeg", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_png", "LSColors", "png", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_gif", "LSColors", "gif", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_mp3", "LSColors", "mp3", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_ogg", "LSColors", "ogg", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_flac", "LSColors", "flac", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_tar", "LSColors", "tar", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_targz", "LSColors", "targz", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_tarbz2", "LSColors", "tarbz2", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_zip", "LSColors", "zip", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_rar", "LSColors", "rar", "combo", dicts.ls_colors)

		######################## Custom Prompt Builder #####################################
		WidgetHandler.InitWidget("use_custom_prompt", "Custom", "use_custom_prompt", "bool", None)
		promptbuilder.PromptBuilder(config.cfo)

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
			subprocess.Popen("x-www-browser " + DOCDIR + "/bashstyle-ng/index.html", shell=True)

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
