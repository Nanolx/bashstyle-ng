#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2019 Christopher Bratusek		#
#							#
#########################################################

import gettext, os
lang = gettext.translation('bashstyle', fallback=True)
lang.install(names=['_'])

import args
args.CmdArgs()

print(_("\nBashStyle-NG Version %s starting" % os.getenv('BSNG_VERSION')))

MODULES = [ 'os.path', 'sys', 'string', 'shutil', 'optparse', 'subprocess',
            'undobuffer', 'lockfile', 'config', 'widgethandler', 'configui',
            'dicts', 'prompts', 'promptbuilder', 'iconbook', 'keybindings' ]

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
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

lock = lockfile.LockFile()
config = config.Config()

class BashStyleNG(object):

	def __init__(self):
		lock.Write()

		######################## handle ConfigObj ##########################################
		config.InitConfig()
		config.LoadConfig()
		config.CheckConfig()

		######################## load translations & widgethandler #########################
		gtkbuilder = widgethandler.gtkbuilder
		WidgetHandler = widgethandler.WidgetHandler(config.cfo, config.udc, config.fdc)

		####################### Style Options ##############################################
		WidgetHandler.InitWidget("use_bashstyle", "Style", "use_bashstyle", "switch", None)
		WidgetHandler.InitWidget("colored_prompts", "Style", "enable_colors", "bool", None)
		WidgetHandler.InitWidget("dark_terminal", "Style", "dark_terminal", "bool", None)
		WidgetHandler.InitWidget("ls_color", "Style", "colored_ls", "bool", None)
		WidgetHandler.InitWidget("grep_color", "Style", "colored_grep", "bool", None)
		WidgetHandler.InitWidget("random_style", "Style", "random_style", "bool", None)
		WidgetHandler.InitWidget("prompt_style", "Style", "prompt_style", "combo", dicts.prompt_styles)
		WidgetHandler.InitWidget("color_style", "Style", "color_style", "combo", dicts.color_styles)
		WidgetHandler.InitWidget("grep_colour", "Style", "grep_color", "combo", dicts.grep_colors)
		WidgetHandler.InitWidget("colorshell", "Style", "colorshell", "bool", None)
		WidgetHandler.InitWidget("colorshell_reset", "Style", "colorshell_reset", "bool", None)
		WidgetHandler.InitWidget("color_date", "Style", "color_date", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_font", "Style", "color_font", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_host", "Style", "color_host", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_ps", "Style", "color_ps", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_ps0", "Style", "color_ps0", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_ps2", "Style", "color_ps2", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_ps3", "Style", "color_ps3", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_ps4", "Style", "color_ps4", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_separator", "Style", "color_separator", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_time", "Style", "color_time", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_uptime", "Style", "color_uptime", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_user", "Style", "color_user", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_wdir", "Style", "color_wdir", "combo", dicts.colors)

		WidgetHandler.InitWidget("show_files_amount", "Style", "files_amount", "bool", None)
		WidgetHandler.InitWidget("show_uptime", "Style", "uptime", "bool", None)
		WidgetHandler.InitWidget("show_file_size", "Style", "files_size", "bool", None)
		WidgetHandler.InitWidget("show_tty", "Style", "tty", "bool", None)
		WidgetHandler.InitWidget("show_processes", "Style", "processes", "bool", None)
		WidgetHandler.InitWidget("show_load", "Style", "load", "bool", None)
		WidgetHandler.InitWidget("show_battery", "Style", "battery_load", "bool", None)
		WidgetHandler.InitWidget("show_mem", "Style", "mem", "combo", dicts.memory_types)

		WidgetHandler.InitWidget("equinox_systemload", "Style", "equinox_systemload", "bool", None)
		WidgetHandler.InitWidget("equinox_cpuload", "Style", "equinox_cpuload", "bool", None)
		WidgetHandler.InitWidget("equinox_ram", "Style", "equinox_ram", "bool", None)
		WidgetHandler.InitWidget("equinox_proc", "Style", "equinox_proc", "bool", None)
		WidgetHandler.InitWidget("equinox_lastcmd", "Style", "equinox_lastcmd", "bool", None)
		WidgetHandler.InitWidget("equinox_uptime", "Style", "equinox_uptime", "bool", None)

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

		####################### Termcap Colors #############################################
		WidgetHandler.InitWidget("termcap_colors", "Termcap", "less_termcap_color", "switch", None)
		WidgetHandler.InitWidget("termcap_mb", "Termcap", "less_blink", "combo", dicts.less_foreground_colors)
		WidgetHandler.InitWidget("termcap_md", "Termcap", "less_bold", "combo", dicts.less_foreground_colors)
		WidgetHandler.InitWidget("termcap_us", "Termcap", "less_underline", "combo", dicts.less_foreground_colors)
		WidgetHandler.InitWidget("termcap_rs", "Termcap", "less_reverse", "combo", dicts.less_foreground_colors)
		WidgetHandler.InitWidget("termcap_mh", "Termcap", "less_dim", "combo", dicts.less_foreground_colors)
		WidgetHandler.InitWidget("termcap_sof", "Termcap", "less_standout_foreground", "combo", dicts.less_foreground_colors)
		WidgetHandler.InitWidget("termcap_sob", "Termcap", "less_standout_background", "combo", dicts.less_background_colors)

		####################### Advanced Stuff #############################################
		WidgetHandler.InitWidget("history_blacklist", "Advanced", "history_ignore", "text", None)
		WidgetHandler.InitWidget("separator", "Advanced", "separator", "text", None)
		WidgetHandler.InitWidget("ps0", "Advanced", "ps0", "text", None)
		WidgetHandler.InitWidget("ps2", "Advanced", "ps2", "text", None)
		WidgetHandler.InitWidget("ps3", "Advanced", "ps3", "text", None)
		WidgetHandler.InitWidget("ps4", "Advanced", "ps4", "text", None)
		WidgetHandler.InitWidget("pwd_cutter", "Advanced", "pwdcut", "text", None)
		WidgetHandler.InitWidget("cdpath", "Advanced", "cdpath", "text", None)
		WidgetHandler.InitWidget("completion_blacklist", "Advanced", "completion_ignore", "text", None)
		WidgetHandler.InitWidget("fcedit", "Advanced", "fcedit", "text", None)
		WidgetHandler.InitWidget("welcome", "Advanced", "welcome_message", "text", None)
		WidgetHandler.InitWidget("path", "Advanced", "path", "text", None)
		WidgetHandler.InitWidget("path_pwd", "Advanced", "path_wd", "bool", None)
		WidgetHandler.InitWidget("history_size", "Advanced", "history_size", "int", None)
		WidgetHandler.InitWidget("pwd_len", "Advanced", "pwdlength", "int", None)
		WidgetHandler.InitWidget("timeout", "Advanced", "timeout", "int", None)
		WidgetHandler.InitWidget("history_control", "Advanced", "history_control", "combo", dicts.history_types)
		WidgetHandler.InitWidget("history_timeformat", "Advanced", "history_timeformat", "text", None)
		WidgetHandler.InitWidget("dirchar", "Advanced", "directory_indicator", "text", None)
		WidgetHandler.InitWidget("enable_lscd", "Advanced", "use_lscd", "bool", None)
		WidgetHandler.InitWidget("enable_treecd", "Advanced", "use_treecd", "bool", None)
		WidgetHandler.InitWidget("customcd_mkdir", "Advanced", "customcd_mkdir", "bool", None)
		WidgetHandler.InitWidget("lscd_options", "Advanced", "lscd_opts", "text", None)
		WidgetHandler.InitWidget("treecd_options", "Advanced", "treecd_opts", "text", None)
		WidgetHandler.InitWidget("color_cd_banner", "Style", "color_cd_banner", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_cd_empty", "Style", "color_cd_empty", "combo", dicts.colors)
		WidgetHandler.InitWidget("color_cd_mkdir", "Style", "color_cd_mkdir", "combo", dicts.colors)
		WidgetHandler.InitWidget("birthday", "Advanced", "user_birthday", "text", None)
		WidgetHandler.InitWidget("dd_noerror", "Advanced", "dd_noerror", "bool", None)
		WidgetHandler.InitWidget("dd_progress", "Advanced", "dd_progress", "bool", None)
		WidgetHandler.InitWidget("restore_pwd", "Advanced", "restore_directory", "bool", None)
		WidgetHandler.InitWidget("debug_verbose", "Advanced", "debug_verbose", "bool", None)
		WidgetHandler.InitWidget("execignore", "Advanced", "exec_ignore", "text", None)
		WidgetHandler.InitWidget("globignore", "Advanced", "glob_ignore", "text", None)
		WidgetHandler.InitWidget("history_sync", "Advanced", "history_sync", "bool", None)
		WidgetHandler.InitWidget("history_isolate", "Advanced", "history_isolate", "bool", None)
		WidgetHandler.InitWidget("user_char", "Style", "user_char", "text", None)
		WidgetHandler.InitWidget("return_good", "Style", "return_good", "text", None)
		WidgetHandler.InitWidget("return_bad", "Style", "return_bad", "text", None)
		WidgetHandler.InitWidget("return_other", "Style", "return_other", "text", None)

		####################### Readline stuff #############################################
		WidgetHandler.InitWidget("use_readline", "Readline", "use_readlinecfg", "switch", None)
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
		WidgetHandler.InitWidget("cstats", "Readline", "colored_stats", "bool", None)
		WidgetHandler.InitWidget("skipcomptext", "Readline", "skip_completed_text", "bool", None)
		WidgetHandler.InitWidget("use_readline70", "Readline", "use_readline70", "switch", None)
		WidgetHandler.InitWidget("colored_completion_prefix", "Readline", "colored_completion_prefix", "bool", None)
		WidgetHandler.InitWidget("enable_bracketed_paste", "Readline", "enable_bracketed_paste", "bool", None)
		WidgetHandler.InitWidget("vi_cmd_string", "Readline", "vi_cmd_mode_string", "text", None)
		WidgetHandler.InitWidget("vi_ins_string", "Readline", "vi_ins_mode_string", "text", None)
		WidgetHandler.InitWidget("emacs_string", "Readline", "emacs_mode_string", "text", None)

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
		WidgetHandler.InitWidget("dotglob", "Shopt", "dotglob", "bool", None)
		WidgetHandler.InitWidget("extglob", "Shopt", "extglob", "bool", None)
		WidgetHandler.InitWidget("nocaseglob", "Shopt", "nocaseglob", "bool", None)
		WidgetHandler.InitWidget("nocasematch", "Shopt", "nocasematch", "bool", None)
		WidgetHandler.InitWidget("localvar_inherit", "Shopt", "localvar_inherit", "bool", None)

		######################## Git Stuff #################################################
		WidgetHandler.InitWidget("use_git", "Git", "use_gitcfg", "switch", None)
		WidgetHandler.InitWidget("git_user", "Git", "git_user_name", "text", None)
		WidgetHandler.InitWidget("git_mail", "Git", "git_user_mail", "text", None)
		WidgetHandler.InitWidget("git_editor", "Git", "git_editor", "text", None)
		WidgetHandler.InitWidget("git_signkey", "Git", "git_signkey", "text", None)
		WidgetHandler.InitWidget("git_color", "Git", "git_color", "bool", None)
		WidgetHandler.InitWidget("git_aliases", "Git", "git_aliases", "bool", None)
		WidgetHandler.InitWidget("git_ssh_remember", "Git", "git_ssh_remember", "bool", None)
		WidgetHandler.InitWidget("git_ssh_timeout", "Git", "git_ssh_timeout", "int", None)
		WidgetHandler.InitWidget("git_ssh_keyfile", "Git", "git_ssh_keyfile", "text", None)

		######################## VimCFG Stuff ##############################################
		WidgetHandler.InitWidget("use_vim", "Vim", "use_vimcfg", "switch", None)
		WidgetHandler.InitWidget("vim_backup", "Vim", "vim_backup", "bool", None)
		WidgetHandler.InitWidget("vim_jump", "Vim", "jump_back", "bool", None)
		WidgetHandler.InitWidget("vim_sline", "Vim", "start_line", "bool", None)
		WidgetHandler.InitWidget("vim_tabstop", "Vim", "tab_length", "int", None)
		WidgetHandler.InitWidget("vim_expandtab", "Vim", "expandtab", "bool", None)
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
		WidgetHandler.InitWidget("vim_wildmenu", "Vim", "wildmenu", "bool", None)
		WidgetHandler.InitWidget("vim_foldenable", "Vim", "foldenable", "bool", None)
		WidgetHandler.InitWidget("vim_foldlevelstart", "Vim", "foldlevelstart", "int", None)
		WidgetHandler.InitWidget("vim_foldnestmax", "Vim", "foldnestmax", "int", None)
		WidgetHandler.InitWidget("vim_foldmethod", "Vim", "foldmethod", "combo", dicts.vim_foldmethods)

		######################## NanoCFG Stuff #############################################
		WidgetHandler.InitWidget("use_nano", "Nano", "use_nanocfg", "switch", None)
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
		WidgetHandler.InitWidget("nano_mouse", "Nano", "enable_mouse",  "bool", None)
		WidgetHandler.InitWidget("nano_logpos",  "Nano", "log_position", "bool", None)
		WidgetHandler.InitWidget("nano_nowrap", "Nano", "no_wrap", "bool", None)
		WidgetHandler.InitWidget("nano_tabspace", "Nano", "tab_to_spaces", "bool", None)
		WidgetHandler.InitWidget("nano_tabwidth", "Nano", "tab_size", "int", None)
		WidgetHandler.InitWidget("nano_colorui", "Nano", "set_uicolors", "bool", None)
		WidgetHandler.InitWidget("nano_functions_fg", "Nano", "function_color_fg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_functions_bg", "Nano", "function_color_bg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_keys_fg", "Nano", "key_color_fg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_keys_bg", "Nano", "key_color_bg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_status_fg", "Nano", "status_color_fg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_status_bg", "Nano", "status_color_bg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_title_fg", "Nano", "title_color_fg", "combo", dicts.nano_colors)
		WidgetHandler.InitWidget("nano_title_bg", "Nano", "title_color_bg", "combo", dicts.nano_colors)

		######################## LS Colors Stuff ###########################################
		WidgetHandler.InitWidget("use_lscolors", "LSColors", "use_lscolors", "switch", None)
		WidgetHandler.InitWidget("ls_custom", "LSColors", "custom", "text", None)
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
		WidgetHandler.InitWidget("ls_tarxz", "LSColors", "tarxz", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_zip", "LSColors", "zip", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_rar", "LSColors", "rar", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_link", "LSColors", "link", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_socket", "LSColors", "socket", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_pipe", "LSColors", "pipe", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_blockdev", "LSColors", "blockdev", "combo", dicts.ls_colors)
		WidgetHandler.InitWidget("ls_chardev", "LSColors", "chardev", "combo", dicts.ls_colors)

		######################## Keybindings ###############################################
		keytree = keybindings.KeyTree(config.cfo, config.udc, config.fdc)
		keytree.InitTree()

		######################## Custom Prompt Builder #####################################
		WidgetHandler.InitWidget("use_customprompt", "Custom", "use_custom_prompt", "switch", None)
		pbuilder = promptbuilder.PromptBuilder(config.cfo, config.udc, config.fdc)
		pbuilder.InitPromptBuilder()

		######################## Load the IconView and Notebook ############################
		view = iconbook.IconBook()
		view.InitIconBook()

		######################## Load the configuration handling UI ########################
		cfgui = configui.ConfigUI(config.cfo, config.udc, config.fdc)
		cfgui.InitConfigUI()

		######################## About Dialog non-static strings ###########################
		WidgetHandler.InitWidget("about.prefix", None, os.getenv('BSNG_PREFIX'), "label", None)
		WidgetHandler.InitWidget("about.version", None, "%s (%s)" %(os.getenv('BSNG_VERSION'), os.getenv('BSNG_CODENAME')), "label", None)

		######################## Load the first start information UI #######################
		suui = configui.StartupUI(config.cfo, config.udc, config.fdc)
		suui.InitStartupUI()

		######################## Load the Main-Window ######################################
		self.bashstyle = gtkbuilder.get_object("bashstyle")

		def destroy(self, widget):
			config.WriteConfig()
			lock.Remove()
			Gtk.main_quit()

		self.bashstyle.connect("destroy", destroy, None)

		self.bashstyle.show

if __name__ == "__main__":
	lock.Check()
	hwg = BashStyleNG()
	Gtk.main()
