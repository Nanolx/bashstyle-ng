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
	   'i18n', 'misc', 'lockfile', 'config', 'widgethandler' ]

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

		config.InitConfig()
		config.LoadConfig()
		config.UpdateConfig()

		####################### blacklist / gtkBuilder #####################################

		blacklist = ['\'', '\"']
		gtkbuilder = widgethandler.gtkbuilder

		####################### cd into $HOME ##############################################
		os.chdir(os.getenv("HOME"))

		lang = i18n.Gettext()
		lang.SetLang()
		
		WidgetHandler = widgethandler.WidgetHandler()

		###################### Load Use-Bashstyle Button ##################################

		self.use_bashstyle = gtkbuilder.get_object("use_bashstyle")
		self.use_bashstyle.set_active(config.cfo["Style"].as_bool("use_bashstyle"))

		def set_use_bashstyle(widget, data=None):
			config.cfo["Style"]["use_bashstyle"] = widget.get_active()
			misc.EnableBashstyleNG(widget.get_active())

		self.use_bashstyle.connect("toggled", set_use_bashstyle)

		####################### Load the Colored Prompts Button ###########################

		self.colored_prompts = gtkbuilder.get_object("colored_prompts")
		self.colored_prompts.set_active(config.cfo["Style"].as_bool("enable_colors"))

		def set_colored_prompts(widget, data=None):
			config.cfo["Style"]["enable_colors"] = widget.get_active()

		self.colored_prompts.connect("toggled", set_colored_prompts)

		####################### Load the Colored ls Button ################################

		self.ls_color = gtkbuilder.get_object("ls_color")
		self.ls_color.set_active(config.cfo["Style"].as_bool("colored_ls"))

		def set_colored_ls(widget, data=None):
			config.cfo["Style"]["colored_ls"] =  widget.get_active()

		self.ls_color.connect("toggled", set_colored_ls)

		####################### Lad the Colored Manpages Button ###########################

		self.manpage_color = gtkbuilder.get_object("manpage_color")
		self.manpage_color.set_active(config.cfo["Style"].as_bool("colored_man"))

		def set_colored_man(widget, data=None):
			config.cfo["Style"]["colored_man"] = widget.get_active()

		self.manpage_color.connect("toggled", set_colored_man)

		####################### Load the Colored Grep Button #############################

		self.grep_color = gtkbuilder.get_object("grep_color")
		self.grep_color.set_active(config.cfo["Style"].as_bool("colored_grep"))

		def set_colored_grep(widget, data=None):
			config.cfo["Style"]["colored_grep"] = widget.get_active()

		self.grep_color.connect("toggled", set_colored_grep)

		####################### Load the Random Style Button ##############################

		self.random_style = gtkbuilder.get_object("random_style")
		self.random_style.set_active(config.cfo["Style"].as_bool("random_style"))

		def set_random_style(widget, data=None):
			config.cfo["Style"]["random_style"] = widget.get_active()

		self.random_style.connect("toggled", set_random_style)

		####################### Load the Color Style Combobox #############################

		self.color_style = gtkbuilder.get_object("color_style")

		color_styles = {
				 0 : "normal",
				 1 : "bright",
				 2 : "dimmed",
				 3 : "inverted",
				 4 : "underlined",
			        }

		self.color_style.set_active(misc.SwapDictionary(color_styles)[config.cfo["Style"]["color_style"]])

		def set_color_style(widget, data=None):
			selection = widget.get_active()
			config.cfo["Style"]["color_style"] = color_styles[selection]

		self.color_style.connect("changed", set_color_style)

		####################### Load the Terminfo Combobox ################################

		self.terminfo = gtkbuilder.get_object("terminfo")

		man_styles = {
			      0 : "mostlike",
			      1 : "bold",
			      2 : "nebula",
			     }

		self.terminfo.set_active(misc.SwapDictionary(man_styles)[config.cfo["Style"]["man_style"]])

		def set_man_style(widget, data=None):
			selection = widget.get_active()
			config.cfo["Style"]["man_style"] = man_styles[selection]

		self.terminfo.connect("changed", set_man_style)

		####################### Load the Grep Color Combobox ##############################

		self.grep_colour = gtkbuilder.get_object("grep_colour")

		grep_colors = {
			        0 : "01;38;5;0",
			        1 : "01;38;5;1",
			        2 : "01;38;5;2",
			        3 : "01;38;5;3",
			        4 : "01;38;5;4",
			        5 : "01;38;5;5",
			        6 : "01;38;5;6",
			        7 : "01;38;5;7",
			        8 : "01;38;5;33",
			        9 : "01;38;5;111",
			       10 : "01;38;5;45",
			       11 : "01;38;5;60",
			       12 : "01;38;5;42",
			       13 : "01;38;5;637",
			       14 : "01;38;5;684",
			       15 : "01;38;5;761",
			       16 : "01;38;5;690",
			       17 : "01;38;5;714",
			       18 : "01;38;5;604",
			       19 : "01;38;5;213",
			       20 : "01;38;5;5344",
			      }

		self.grep_colour.set_active(misc.SwapDictionary(grep_colors)[config.cfo["Style"]["grep_color"]])

		def set_grep_color(widget, data=None):
			selection = widget.get_active()
			config.cfo["Style"]["color/grep"] = grep_colors[selection]

		self.grep_colour.connect("changed", set_grep_color)

		####################### Load the Color Changer Comboboxes #########################

		self.color_of = gtkbuilder.get_object("color_of")
		self.color_to = gtkbuilder.get_object("color_to")

		self.color_of.set_active(0)
		self.color_to.set_active(0)

		color_keys = {
			      1 : "color_user",
			      2 : "color_host",
			      3 : "color_date",
			      4 : "color_time",
			      5 : "color_wdir",
			      6 : "color_font",
			      7 : "color_separator",
			      8 : "color_uptime",
			      9 : "color_ps234",
			     }

		colors = {
			   1 : "$black",
			   2 : "$red",
			   3 : "$green",
			   4 : "$yellow",
			   5 : "$blue",
			   6 : "$magenta",
			   7 : "$cyan",
			   8 : "$white",
			   9 : "$coldblue",
			  10 : "$smoothblue",
			  11 : "$iceblue",
			  12 : "$turqoise",
			  13 : "$smoothgreen",
			  14 : "$winered",
			  15 : "$brown",
			  16 : "$silver",
			  17 : "$ocher",
			  18 : "$orange",
			  19 : "$purple",
			  20 : "$pink",
			  21 : "$cream",
			 }

		def change_color(widget, data=None):
			color_set = self.color_of.get_active()
			color_is = self.color_to.get_active()
			if color_set != 0 and color_is != 0:
				config.cfo["Style"][color_keys[color_set]] = colors[color_is]
				self.color_to.set_active(0)
				self.color_of.set_active(0)

		self.color_of.connect("changed", change_color)
		self.color_to.connect("changed", change_color)

		####################### Load the Prompt Style Button ##############################

		self.prompt_style = gtkbuilder.get_object("prompt_style")

		prompt_styles = {
				  0 : "separator",
				  1 : "vector",
				  2 : "clock",
				  3 : "clock-ad",
				  4 : "elite",
				  5 : "poweruser",
				  6 : "dirks",
				  7 : "dot_prompt",
				  8 : "sepa_ng",
				  9 : "quirk",
				 10 : "sputnik",
				 11 : "ayoli",
				}

		self.prompt_style.set_active(misc.SwapDictionary(prompt_styles)[config.cfo["Style"]["prompt_style"]])

		def set_prompt_style(widget, data=None):
			selection = widget.get_active()
			config.cfo["Style"]["prompt_style"] =  prompt_styles[selection]

		self.prompt_style.connect("changed", set_prompt_style)

		####################### Load the Alias #1 Entry ###################################

		WidgetHandler.InitWidget("alias1", "Alias", "alias_one", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias2", "Alias", "alias_two", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias3", "Alias", "alias_three", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias4", "Alias", "alias_four", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias5", "Alias", "alias_five", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias6", "Alias", "alias_six", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias7", "Alias", "alias_seven", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias8", "Alias", "alias_eight", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("alias9", "Alias", "alias_nine", "text", config.cfo, config.udc, config.fdc)

		####################### Load the Reset History Button #############################

		self.reset_history = gtkbuilder.get_object("reset_history")

		def do_reset_history(widget, data=None):
			os.remove(os.path.expanduser("~/.bash_history"))

		self.reset_history.connect("clicked", do_reset_history)

		####################### Load the History Control Combobox #########################

		self.history_control = gtkbuilder.get_object("history_control")

		history_types = {
				 0 : "erasedups",
				 1 : "ignoredups",
				 2 : "ignorespace",
				 3 : "ignoreboth",
				}

		self.history_control.set_active(misc.SwapDictionary(history_types)[config.cfo["Advanced"]["history_control"]])

		def set_history_control(widget, data=None):
			selection = widget.get_active()
			config.cfo["Advanced"]["hist_control"] = history_types[selection]

		self.history_control.connect("changed", set_history_control)

		####################### Advanced Stuff ############################################

		WidgetHandler.InitWidget("history_blacklist", "Advanced", "history_ignore", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("separator", "Advanced", "separator", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("ps234", "Advanced", "ps234", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("pwd_cutter", "Advanced", "pwdcut", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("cdpath", "Advanced", "cdpath", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("completion_blacklist", "Advanced", "completion_ignore", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("fcedit", "Advanced", "fcedit", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("welcome", "Advanced", "welcome_message", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("path", "Advanced", "path", "text", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("history_size", "Advanced", "history_size", "int", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("pwd_len", "Advanced", "pwdlength", "int", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("timeout", "Advanced", "timeout", "int", config.cfo, config.udc, config.fdc)

		####################### Connect the Use Readlinecfg Button ########################

		self.readline = gtkbuilder.get_object("readline")
		self.readline.set_active(config.cfo["Readline"].as_bool("use_readlinecfg"))

		def set_readline(widget, data=None):
			config.cfo["Readline"]["use_readlinecfg"] = widget.get_active()

		self.readline.connect("clicked", set_readline)

		####################### Connect the Completion Button #############################

		self.completion = gtkbuilder.get_object("completion")
		self.completion.set_active(config.cfo["Readline"].as_bool("completion"))

		def set_completion(widget, data=None):
			config.cfo["Readline"]["completion"] = widget.get_active()

		self.completion.connect("clicked", set_completion)

		####################### Connect the Bellstyle Combobox ############################

		self.bellstyle = gtkbuilder.get_object("bellstyle")

		bell_styles = {
				0 : "audible",
				1 : "visible",
				2 : "none",
			      }

		self.bellstyle.set_active(misc.SwapDictionary(bell_styles)[config.cfo["Readline"]["bellstyle"]])

		def set_bellstyle(widget, data=None):
			selection = widget.get_active()
			config.cfo["Readline"]["bellstyle"] = bell_styles[selection]

		self.bellstyle.connect("changed", set_bellstyle)

		####################### Connect the Editing Mode Combobox #########################

		self.editmode = gtkbuilder.get_object("editmode")

		edit_modes = {
			      0 : "emacs",
			      1 : "vi",
			     }

		self.editmode.set_active(misc.SwapDictionary(edit_modes)[config.cfo["Readline"]["editing_mode"]])

		def set_editmode(widget, data=None):
			selection = widget.get_active()
			config.cfo["Readline"]["editing_mode"] = edit_modes[selection]

		self.editmode.connect("changed", set_editmode)

		####################### Connect the Ambiguous Button ##################################

		self.ambiguous = gtkbuilder.get_object("ambiguous")
		self.ambiguous.set_active(config.cfo["Readline"].as_bool("ambiguous_show"))

		def set_ambiguous(widget, data=None):
			config.cfo["Readline"]["ambiguous_show"] = widget.get_active()

		self.ambiguous.connect("clicked", set_ambiguous)

		####################### Connect the Match Hidden Button ###########################

		self.match_hidden = gtkbuilder.get_object("match_hidden")
		self.match_hidden.set_active(config.cfo["Readline"].as_bool("complete_hidden"))

		def set_match_hidden(widget, data=None):
			config.cfo["Readline"]["complete_hidden"] = widget.get_active()

		self.match_hidden.connect("clicked", set_match_hidden)

		####################### Connect the Ignore Case Button ############################

		self.ignore_case = gtkbuilder.get_object("ignore_case")
		self.ignore_case.set_active(config.cfo["Readline"].as_bool("ignore_case"))

		def set_ignore_case(widget, data=None):
			config.cfo["Readline"]["ignore_case"] = widget.get_active()

		self.ignore_case.connect("clicked", set_ignore_case)

		####################### Connect the Query Items Button ############################

		WidgetHandler.InitWidget("query_items", "Readline", "query_items", "int", config.cfo, config.udc, config.fdc)

		####################### Connect the Horizontal Completion Button ##################

		self.completion_hz = gtkbuilder.get_object("completion_hz")
		self.completion_hz.set_active(config.cfo["Readline"].as_bool("complete_horizontal"))

		def set_completion_hz(widget, data=None):
			config.cfo["Readline"]["complete_horizontal"] = widget.get_active()

		self.completion_hz.connect("clicked", set_completion_hz)

		####################### Connect the Mark Directories Button #######################

		self.mark_dirs = gtkbuilder.get_object("mark_dirs")
		self.mark_dirs.set_active(config.cfo["Readline"].as_bool("mark_directories"))

		def set_mark_dirs(widget, data=None):
			config.cfo["Readline"]["mark_directories"] = widget.get_active()

		self.mark_dirs.connect("clicked", set_mark_dirs)

		####################### Connect the Mark Symbolic Directories Button ##############

		self.mark_symdirs = gtkbuilder.get_object("mark_symdirs")
		self.mark_symdirs.set_active(config.cfo["Readline"].as_bool("mark_symbolic_directories"))

		def set_mark_symdirs(widget, data=None):
			config.cfo["Readline"]["mark_symbolic_directories"] = widget.get_active()

		self.mark_symdirs.connect("clicked", set_mark_symdirs)

		####################### Connect the Visible Stats Button ##########################

		self.vstats = gtkbuilder.get_object("vstats")
		self.vstats.set_active(config.cfo["Readline"].as_bool("visible_stats"))

		def set_vstats(widgets, data=None):
			config.cfo["Readline"]["visible_stats"] = widgets.get_active()

		self.vstats.connect("clicked", set_vstats)

		####################### Connect the Horizontal Scroll Button ######################

		self.scroll_hz = gtkbuilder.get_object("scroll_hz")
		self.scroll_hz.set_active(config.cfo["Readline"].as_bool("scroll_horizontal"))

		def set_scroll_hz(widget, data=None):
			config.cfo["Readline"]["scroll_horizontal"] = widget.get_active()

		self.scroll_hz.connect("clicked", set_scroll_hz)

		####################### Connect the Mark Modified Lines Button ####################

		self.modlines = gtkbuilder.get_object("modlines")
		self.modlines.set_active(config.cfo["Readline"].as_bool("mark_modified"))

		def set_modlines(widget, data=None):
			config.cfo["Readline"]["mark_modified"] = widget.get_active()

		self.modlines.connect("clicked", set_modlines)

		####################### Connect the Show Files Amount Button ######################

		self.show_files_amount = gtkbuilder.get_object("show_files_amount")
		self.show_files_amount.set_active(config.cfo["Separator"].as_bool("files_amount"))

		def set_show_files_amount(widget, data=None):
			config.cfo["Separator"]["files_amount"] = widget.get_active()

		self.show_files_amount.connect("clicked", set_show_files_amount)

		####################### Connect the Show Uptime Button ############################

		self.show_uptime = gtkbuilder.get_object("show_uptime")
		self.show_uptime.set_active(config.cfo["Separator"].as_bool("uptime"))

		def set_show_uptime(widget, data=None):
			config.cfo["Separator"]["uptime"] = widget.get_active()

		self.show_uptime.connect("clicked", set_show_uptime)

		####################### Connect the Show Files Size Button ########################

		self.show_file_size = gtkbuilder.get_object("show_file_size")
		self.show_file_size.set_active(config.cfo["Separator"].as_bool("files_size"))

		def set_show_file_size(widget, data=None):
			config.cfo["Separator"]["files_size"] = widget.get_active()

		self.show_file_size.connect("clicked", set_show_file_size)

		####################### Connect the Show TTY Button ##############################

		self.show_tty = gtkbuilder.get_object("show_tty")
		self.show_tty.set_active(config.cfo["Separator"].as_bool("tty"))

		def set_show_tty(widget, data=None):
			config.cfo["Separator"]["tty"] = widget.get_active()

		self.show_tty.connect("clicked", set_show_tty)

		####################### Connect the Show Running Processes Button #################

		self.show_processes = gtkbuilder.get_object("show_processes")
		self.show_processes.set_active(config.cfo["Separator"].as_bool("processes"))

		def set_show_processes(widget, data=None):
			config.cfo["Separator"]["processes"] = widget.get_active()

		self.show_processes.connect("clicked", set_show_processes)

		####################### Connect the Show Systemload Button ########################

		self.show_load = gtkbuilder.get_object("show_load")
		self.show_load.set_active(config.cfo["Separator"].as_bool("load"))

		def set_show_load(widget, data=None):
			config.cfo["Separator"]["load"] = widget.get_active()

		self.show_processes.connect("clicked", set_show_load)

		####################### Connect the Show Batteryload Button #######################

		self.show_battery = gtkbuilder.get_object("show_battery")
		self.show_battery.set_active(config.cfo["Separator"].as_bool("battery_load"))

		def set_show_battery(widget, data=None):
			config.cfo["Separator"]["battery_load"] = widget.get_active()

		self.show_battery.connect("clicked", set_show_battery)

		####################### Connect the Show Memory Combobox ##########################

		self.show_mem = gtkbuilder.get_object("show_mem")

		memory_types = {
				0 : "free",
				1 : "used",
				2 : "both",
				3 : "none",
			       }

		self.show_mem.set_active(misc.SwapDictionary(memory_types)[config.cfo["Separator"]["mem"]])

		def set_show_mem(widget, data=None):
			selection = widget.get_active()
			config.cfo["Separator"]["mem"] = memory_types[selection]

		self.show_mem.connect("changed", set_show_mem)

		####################### Connect the Dirchar Entry #################################

		WidgetHandler.InitWidget("dirchar", "Extra", "directory_indicator", "text", config.cfo, config.udc, config.fdc)

		####################### Connect the Tab Rotation Button ###########################

		self.tabrotate = gtkbuilder.get_object("tabrotate")
		self.tabrotate.set_active(config.cfo["Extra"].as_bool("tab_rotation"))

		def set_tabrotate(widget, data=None):
			config.cfo["Extra"]["tab_rotation"] = widget.get_active()

		self.tabrotate.connect("clicked", set_tabrotate)

		####################### Connect the histappend Button ###########################

		self.histappend = gtkbuilder.get_object("histappend")
		self.histappend.set_active(config.cfo["Shopt"].as_bool("histappend"))

		def set_histappend(widget, data=None):
			config.cfo["Shopt"]["histappend"] = widget.get_active()

		self.histappend.connect("clicked", set_histappend)

		####################### Connect the cdspell Button ###########################

		self.cdspell = gtkbuilder.get_object("cdspell")
		self.cdspell.set_active(config.cfo["Shopt"].as_bool("cdspell"))

		def set_cdspell(widget, data=None):
			config.cfo["Shopt"]["cdspell"] = widget.get_active()

		self.cdspell.connect("clicked", set_cdspell)

		####################### Connect the cdable_vars Button ###########################

		self.cdable_vars = gtkbuilder.get_object("cdable_vars")
		self.cdable_vars.set_active(config.cfo["Shopt"].as_bool("cdable_vars"))

		def set_cdable_vars(widget, data=None):
			config.cfo["Shopt"]["cdable_vars"] = widget.get_active()

		self.cdable_vars.connect("clicked", set_cdable_vars)

		####################### Connect the checkhash Button ###########################

		self.checkhash = gtkbuilder.get_object("checkhash")
		self.checkhash.set_active(config.cfo["Shopt"].as_bool("checkhash"))

		def set_checkhash(widget, data=None):
			config.cfo["Shopt"]["checkhash"] = widget.get_active()

		self.checkhash.connect("clicked", set_checkhash)

		####################### Connect the cmdhist Button ###########################

		self.cmdhist = gtkbuilder.get_object("cmdhist")
		self.cmdhist.set_active(config.cfo["Shopt"].as_bool("cmdhist"))

		def set_cmdhist(widget, data=None):
			config.cfo["Shopt"]["cmdhist"] = widget.get_active()

		self.cmdhist.connect("clicked", set_cmdhist)

		####################### Connect the force_fignore Button ###########################

		self.force_fignore = gtkbuilder.get_object("force_fignore")
		self.force_fignore.set_active(config.cfo["Shopt"].as_bool("force_fignore"))

		def set_force_fignore(widget, data=None):
			config.cfo["Shopt"]["force_fignore"] = widget.get_active()

		self.force_fignore.connect("clicked", set_force_fignore)

		####################### Connect the histreedit Button ###########################

		self.histreedit = gtkbuilder.get_object("histreedit")
		self.histreedit.set_active(config.cfo["Shopt"].as_bool("histreedit"))

		def set_histreedit(widget, data=None):
			config.cfo["Shopt"]["histreedit"] = widget.get_active()

		self.histreedit.connect("clicked", set_histreedit)

		####################### Connect the no_empty_cmd Button ###########################

		self.no_empty_cmd = gtkbuilder.get_object("no_empty_cmd")
		self.no_empty_cmd.set_active(config.cfo["Shopt"].as_bool("no_empty_cmd_completion"))

		def set_no_empty_cmd(widget, data=None):
			config.cfo["Shopt"]["no_empty_cmd_completion"] = widget.get_active()

		self.no_empty_cmd.connect("clicked", set_no_empty_cmd)

		####################### Connect the autocd Button ###########################

		self.autocd = gtkbuilder.get_object("autocd")
		self.autocd.set_active(config.cfo["Shopt"].as_bool("autocd"))

		def set_autocd(widget, data=None):
			config.cfo["Shopt"]["autocd"] = widget.get_active()

		self.autocd.connect("clicked", set_autocd)

		####################### Connect the checkjobs Button ###########################

		self.checkjobs = gtkbuilder.get_object("checkjobs")
		self.checkjobs.set_active(config.cfo["Shopt"].as_bool("checkjobs"))

		def set_checkjobs(widget, data=None):
			config.cfo["Shopt"]["checkjobs"] = widget.get_active()

		self.checkjobs.connect("clicked", set_checkjobs)

		####################### Connect the globstar Button ###########################

		self.globstar = gtkbuilder.get_object("globstar")
		self.globstar.set_active(config.cfo["Shopt"].as_bool("globstar"))

		def set_globstar(widget, data=None):
			config.cfo["Shopt"]["globstar"] = widget.get_active()

		self.globstar.connect("clicked", set_globstar)

		####################### Connect the dirspell Button ###########################

		self.dirspell = gtkbuilder.get_object("dirspell")
		self.dirspell.set_active(config.cfo["Shopt"].as_bool("dirspell"))

		def set_dirspell(widget, data=None):
			config.cfo["Shopt"]["dirspell"] = widget.get_active()

		self.dirspell.connect("clicked", set_dirspell)

		####################### Connect the Use VimCFG Button #############################

		self.use_vimcfg = gtkbuilder.get_object("use_vimcfg")
		self.use_vimcfg.set_active(config.cfo["Vim"].as_bool("use_vimcfg"))

		def set_use_vimcfg(widget, data=None):
			config.cfo["Vim"]["use_vimcfg"] = widget.get_active()

		self.use_vimcfg.connect("clicked", set_use_vimcfg)

		####################### Connect the Vim/Backup files Button #######################

		self.vim_backup = gtkbuilder.get_object("vim_backup")
		self.vim_backup.set_active(config.cfo["Vim"].as_bool("vim_backup"))

		def set_vim_backup(widget, data=None):
			config.cfo["Vim"]["vim_backup"] = widget.get_active()

		self.vim_backup.connect("clicked", set_vim_backup)

		####################### Connect the Vim/Jump Back Button ##########################

		self.vim_jump = gtkbuilder.get_object("vim_jump")
		self.vim_jump.set_active(config.cfo["Vim"].as_bool("jump_back"))

		def set_vim_jump(widget, data=None):
			config.cfo["Vim"]["jump_back"] = widget.get_active()

		self.vim_jump.connect("clicked", set_vim_jump)

		###################### Connect the Vim/Jump to start of line Button ##############

		self.vim_sline = gtkbuilder.get_object("vim_sline")
		self.vim_sline.set_active(config.cfo["Vim"].as_bool("start_line"))

		def set_vim_sline(widget, data=None):
			config.cfo["Vim"]["start_line"] = widget.get_active()

		self.vim_sline.connect("clicked", set_vim_sline)

		WidgetHandler.InitWidget("vim_tabstop", "Vim", "tab_length", "int", config.cfo, config.udc, config.fdc)
		WidgetHandler.InitWidget("vim_autowrap", "Vim", "wrap_length", "int", config.cfo, config.udc, config.fdc)

		####################### Connect the Vim/Wrap line Button ##########################

		self.vim_wrap = gtkbuilder.get_object("vim_wrap")
		self.vim_wrap.set_active(config.cfo["Vim"].as_bool("wrap_line"))

		def set_vim_wrap(widget, data=None):
			config.cfo["Vim"]["wrap_line"] = widget.get_active()

		self.vim_wrap.connect("clicked", set_vim_wrap)

		###################### Connect the Vim/Autochdir Button ##########################

		self.vim_cd = gtkbuilder.get_object("vim_cd")
		self.vim_cd.set_active(config.cfo["Vim"].as_bool("chdir"))

		def set_vim_cd(widget, data=None):
			config.cfo["Vim"]["chdir"] = widget.get_active()

		self.vim_cd.connect("clicked", set_vim_cd)

		####################### Connect the Vim/Indention Button ##########################

		self.vim_indent = gtkbuilder.get_object("vim_indent")
		self.vim_indent.set_active(config.cfo["Vim"].as_bool("filetype_indent"))

		def set_vim_indent(widget, data=None):
			config.cfo["Vim"]["filetype_indent"] = widget.get_active()

		self.vim_indent.connect("clicked", set_vim_indent)

		####################### Connect the Vim/Show (partial) command Button #############

		self.vim_cmd = gtkbuilder.get_object("vim_cmd")
		self.vim_cmd.set_active(config.cfo["Vim"].as_bool("show_command"))

		def set_vim_cmd(widget, data=None):
			config.cfo["Vim"]["show_command"] = widget.get_active()

		self.vim_cmd.connect("clicked", set_vim_cmd)

		####################### Connect the Vim/Match Brackets Button #####################

		self.vim_match = gtkbuilder.get_object("vim_match")
		self.vim_match.set_active(config.cfo["Vim"].as_bool("highlight_matches"))

		def set_vim_match(widget, data=None):
			config.cfo["Vim"]["highlight_matches"] = widget.get_active()

		self.vim_match.connect("clicked", set_vim_match)

		####################### Connect the Vim/Syntax Highlight Button ###################

		self.vim_syntax = gtkbuilder.get_object("vim_syntax")
		self.vim_syntax.set_active(config.cfo["Vim"].as_bool("syntax_hilight"))

		def set_vim_syntax(widget, data=None):
			config.cfo["Vim"]["syntax_hilight"] = widget.get_active()

		self.vim_syntax.connect("clicked", set_vim_syntax)

		####################### Connect the Vim/Background Button #########################

		self.vim_bg = gtkbuilder.get_object("vim_bg")
		self.vim_bg.set_active(config.cfo["Vim"].as_bool("dark_background"))

		def set_vim_bg(widget, data=None):
			config.cfo["Vim"]["dark_background"] = widget.get_active()

		self.vim_bg.connect("clicked", set_vim_bg)

		####################### Connect the Vim/Case-Insensitive Button ###################

		self.vim_icase = gtkbuilder.get_object("vim_icase")
		self.vim_icase.set_active(config.cfo["Vim"].as_bool("ignore_case"))

		def set_vim_icase(widget, data=None):
			config.cfo["Vim"]["ignore_case"] = widget.get_active()

		self.vim_icase.connect("clicked", set_vim_icase)

		####################### Connect the Vim/Smart-Case Button #########################

		self.vim_scase = gtkbuilder.get_object("vim_scase")
		self.vim_scase.set_active(config.cfo["Vim"].as_bool("smart_case"))

		def set_vim_scase(widget, data=None):
			config.cfo["Vim"]["smart_case"] = widget.get_active()

		self.vim_scase.connect("clicked", set_vim_scase)

		####################### Connect the Vim/Incremental Search Button #################

		self.vim_isearch = gtkbuilder.get_object("vim_isearch")
		self.vim_isearch.set_active(config.cfo["Vim"].as_bool("incremental_search"))

		def set_vim_isearch(widget, data=None):
			config.cfo["Vim"]["incremental_search"] = widget.get_active()

		self.vim_isearch.connect("clicked", set_vim_isearch)

		####################### Connect the Vim/Hilight Matches Button ####################

		self.vim_hilight = gtkbuilder.get_object("vim_hilight")
		self.vim_hilight.set_active(config.cfo["Vim"].as_bool("highlight_brackets"))

		def set_vim_hilight(widget, data=None):
			config.cfo["Vim"]["highlight_brackets"] = widget.get_active()

		self.vim_hilight.connect("clicked", set_vim_hilight)

		####################### Connect the Vim/Linenumber Button #########################

		self.vim_number = gtkbuilder.get_object("vim_number")
		self.vim_number.set_active(config.cfo["Vim"].as_bool("show_lineno"))

		def set_vim_number(widget, data=None):
			config.cfo["Vim"]["show_lineno"] = widget.get_active()

		self.vim_number.connect("clicked", set_vim_number)

		####################### Connect the Vim/Autosave Button ###########################

		self.vim_save = gtkbuilder.get_object("vim_save")
		self.vim_save.set_active(config.cfo["Vim"].as_bool("autosave"))

		def set_vim_save(widget, data=None):
			config.cfo["Vim"]["autosave"] = widget.get_active()

		self.vim_save.connect("clicked", set_vim_save)

		####################### Connect the Vim/Highlight Line Button #####################

		self.vim_hiline = gtkbuilder.get_object("vim_hiline")
		self.vim_hiline.set_active(config.cfo["Vim"].as_bool("highlight_line"))

		def set_vim_hiline(widget, data=None):
			config.cfo["Vim"]["highlight_line"] = widget.get_active()

		self.vim_hiline.connect("clicked", set_vim_hiline)

		####################### Connect the Vim/Highlight Column Button ###################

		self.vim_hicol = gtkbuilder.get_object("vim_hicol")
		self.vim_hicol.set_active(config.cfo["Vim"].as_bool("highlight_column"))

		def set_vim_hicol(widget, data=None):
			config.cfo["Vim"]["highlight_column"] = widget.get_active()

		self.vim_hicol.connect("clicked", set_vim_hicol)

		####################### Connect the Vim/Show Ruler Button #########################

		self.vim_ruler = gtkbuilder.get_object("vim_ruler")
		self.vim_ruler.set_active(config.cfo["Vim"].as_bool("ruler"))

		def set_vim_ruler(widget, data=None):
			config.cfo["Vim"]["ruler"] = widget.get_active()

		self.vim_ruler.connect("clicked", set_vim_ruler)

		####################### Connect the Vim/Colorscheme Combobox ######################

		self.vim_colorscheme = gtkbuilder.get_object("vim_colorscheme")

		vim_colors = {
			       0 : "default",
			       1 : "adaryn",
			       2 : "advantage",
			       3 : "desert",
			       4 : "gobo",
			       5 : "impact",
			       6 : "nightshade",
			       7 : "nightwish",
			       8 : "wombat",
			       9 : "asu1dark",
			      10 : "candycode",
			      11 : "dw_orange",
			      12 : "fruit",
			      13 : "relaxedgreen",
			      14 : "tango",
			     }

		self.vim_colorscheme.set_active(misc.SwapDictionary(vim_colors)[config.cfo["Vim"]["colorscheme"]])

		def set_vim_colorscheme(widget, data=None):
			selection = widget.get_active()
			config.cfo["Vim"]["colorscheme"] = vim_colors[selection]

		self.vim_colorscheme.connect("changed", set_vim_colorscheme)

		WidgetHandler.InitWidget("vim_rulerformat", "Vim", "rulerformat", "text", config.cfo, config.udc, config.fdc)

		####################### Connect the Use Nanocfg Button ############################

		self.use_nanocfg = gtkbuilder.get_object("use_nanocfg")
		self.use_nanocfg.set_active(config.cfo["Nano"].as_bool("use_nanocfg"))

		def set_use_nanocfg(widget, data=None):
			config.cfo["Nano"]["use_nanocfg"] = widget.get_active()

		self.use_nanocfg.connect("clicked", set_use_nanocfg)

		####################### Connect the Nano/Backup Button ############################

		self.nano_backup = gtkbuilder.get_object("nano_backup")
		self.nano_backup.set_active(config.cfo["Nano"].as_bool("nano_backup"))

		def set_nano_backup(widget, data=None):
			config.cfo["Nano"]["nano_backup"] = widget.get_active()

		self.nano_backup.connect("clicked", set_nano_backup)

		####################### Connect the Nano/Display Cursor Position Button ###########

		self.nano_const = gtkbuilder.get_object("nano_const")
		self.nano_const.set_active(config.cfo["Nano"].as_bool("show_position"))

		def set_nano_const(widget, data=None):
			config.cfo["Nano"]["show_position"] = widget.get_active()

		self.nano_const.connect("clicked", set_nano_const)

		####################### Connect the Nano/Indention Button #########################

		self.nano_indent = gtkbuilder.get_object("nano_indent")
		self.nano_indent.set_active(config.cfo["Nano"].as_bool("auto_indent"))

		def set_nano_indent(widget, data=None):
			config.cfo["Nano"]["auto_indent"] = widget.get_active()

		self.nano_indent.connect("clicked", set_nano_indent)

		####################### Connect the Nano/Syntax Button ############################

		self.nano_colors = gtkbuilder.get_object("nano_colors")
		self.nano_colors.set_active(config.cfo["Nano"].as_bool("syntax_highlight"))

		def set_nano_colors(widget, data=None):
			config.cfo["Nano"]["syntax_highlight"] = widget.get_active()

		self.nano_colors.connect("clicked", set_nano_colors)

		####################### Connect the Nano/No Help Button ###########################

		self.nano_nohelp = gtkbuilder.get_object("nano_nohelp")
		self.nano_nohelp.set_active(config.cfo["Nano"].as_bool("hide_help"))

		def set_nano_nohelp(widget, data=None):
			config.cfo["Nano"]["hide_help"] = widget.get_active()

		self.nano_nohelp.connect("clicked", set_nano_nohelp)

		####################### Connect the Nano/Case-Sensitive Button ####################

		self.nano_case = gtkbuilder.get_object("nano_case")
		self.nano_case.set_active(config.cfo["Nano"].as_bool("case_sensitive"))

		def set_nano_case(widget, data=None):
			config.cfo["Nano"]["case_sensitive"] = widget.get_active()

		self.nano_case.connect("clicked", set_nano_case)

		####################### Connect the Nano/Bold Text Button #########################

		self.nano_boldtext = gtkbuilder.get_object("nano_boldtext")
		self.nano_boldtext.set_active(config.cfo["Nano"].as_bool("bold_text"))

		def set_nano_boldtext(widget, data=None):
			config.cfo["Nano"]["bold_text"] = widget.get_active()

		self.nano_boldtext.connect("clicked", set_nano_boldtext)

		####################### Connect the Nano/More Space Button ########################

		self.nano_morespace = gtkbuilder.get_object("nano_morespace")
		self.nano_morespace.set_active(config.cfo["Nano"].as_bool("more_space"))

		def set_nano_morespace(widget, data=None):
			config.cfo["Nano"]["more_space"] = widget.get_active()

		self.nano_morespace.connect("clicked", set_nano_morespace)

		####################### Connect the Nano/History Button ############################

		self.nano_history = gtkbuilder.get_object("nano_history")
		self.nano_history.set_active(config.cfo["Nano"].as_bool("history"))

		def set_nano_history(widget, data=None):
			config.cfo["Nano"]["history"] = widget.get_active()

		self.nano_history.connect("clicked", set_nano_history)

		####################### Connect the Nano/Rebind delete Button ######################

		self.nano_rbdel = gtkbuilder.get_object("nano_rbdel")
		self.nano_rbdel.set_active(config.cfo["Nano"].as_bool("rebind_delete"))

		def set_nano_rbdel(widget, data=None):
			config.cfo["Nano"]["rebind_delete"] = widget.get_active()

		self.nano_rbdel.connect("clicked", set_nano_rbdel)

		####################### Connect the Nano/Rebind Keypad Button ######################

		self.nano_rbkp = gtkbuilder.get_object("nano_rbkp")
		self.nano_rbkp.set_active(config.cfo["Nano"].as_bool("rebind_keypad"))

		def set_nano_rbkp(widget, data=None):
			config.cfo["Nano"]["rebind_keypad"] = widget.get_active()

		self.nano_rbkp.connect("clicked", set_nano_rbkp)

		####################### Set the ls color for given filetype #######################

		ls_colors = {
			      0 : "$lblack",
			      1 : "$lred",
			      2 : "$lgreen",
			      3 : "$lyellow",
			      4 : "$lblue",
			      5 : "$lmagenta",
			      6 : "$lcyan",
			      7 : "$lwhite",
			      8 : "$lcoldblue",
			      9 : "$lsmoothblue",
			     10 : "$liceblue",
			     11 : "$lturqoise",
			     12 : "$lsmoothgreen",
			     13 : "$lwinered",
			     14 : "$lbrown",
			     15 : "$lsilver",
			     16 : "$locher",
			     17 : "$lorange",
			     18 : "$lpurple",
			     19 : "$lpink",
			     20 : "$lcream",
			    }

		ls_colors_inv = misc.SwapDictionary(ls_colors)

		def set_ls_color(self, type, selection):
			config.cfo["LSColors"]["%s" % type] = ls_colors[selection]

		####################### Connect the use LS-COLORS Button ##########################

		self.use_lscolors = gtkbuilder.get_object("use_lscolors")
		self.use_lscolors.set_active(config.cfo["LSColors"].as_bool("use_lscolors"))

		def set_use_lscolors(widget, data=None):
			config.cfo["LSColors"]["use_lscolors"] = widget.get_active()

		self.use_lscolors.connect("clicked", set_use_lscolors)

		####################### Connect the Executable Files Combobox #####################

		self.ls_exec = gtkbuilder.get_object("ls_exec")
		self.ls_exec.set_active(ls_colors_inv[config.cfo["LSColors"]["exec"]])

		def set_ls_exec(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "exec", selection)

		self.ls_exec.connect("changed", set_ls_exec)

		####################### Connect the Generic Files Combobox ########################

		self.ls_gen = gtkbuilder.get_object("ls_gen")
		self.ls_gen.set_active(ls_colors_inv[config.cfo["LSColors"]["generic"]])

		def set_ls_gen(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "generic", selection)

		self.ls_gen.connect("changed", set_ls_gen)

		####################### Connect the Log Files Combobox ############################

		self.ls_log = gtkbuilder.get_object("ls_log")
		self.ls_log.set_active(ls_colors_inv[config.cfo["LSColors"]["logs"]])

		def set_ls_log(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "logs", selection)

		self.ls_log.connect("changed", set_ls_log)

		####################### Connect the Deb Files Combobox ############################

		self.ls_deb = gtkbuilder.get_object("ls_deb")
		self.ls_deb.set_active(ls_colors_inv[config.cfo["LSColors"]["deb"]])

		def set_ls_deb(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "deb", selection)

		self.ls_deb.connect("changed", set_ls_deb)

		####################### Connect the RPM Files Combobox ############################

		self.ls_rpm = gtkbuilder.get_object("ls_rpm")
		self.ls_rpm.set_active(ls_colors_inv[config.cfo["LSColors"]["rpm"]])

		def set_ls_rpm(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "rpm", selection)

		self.ls_rpm.connect("changed", set_ls_rpm)

		####################### Connect the Desktop Files Combobox ########################

		self.ls_dirs = gtkbuilder.get_object("ls_dirs")
		self.ls_dirs.set_active(ls_colors_inv[config.cfo["LSColors"]["dirs"]])

		def set_ls_dirs(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "dirs", selection)

		self.ls_dirs.connect("changed", set_ls_dirs)

		####################### Connect the JPEG Files Combobox ###########################

		self.ls_jpeg = gtkbuilder.get_object("ls_jpeg")
		self.ls_jpeg.set_active(ls_colors_inv[config.cfo["LSColors"]["jpeg"]])

		def set_ls_jpeg(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "jpeg", selection)

		self.ls_jpeg.connect("changed", set_ls_jpeg)

		####################### Connect the PNG Files Combobox ############################

		self.ls_png = gtkbuilder.get_object("ls_png")
		self.ls_png.set_active(ls_colors_inv[config.cfo["LSColors"]["png"]])

		def set_ls_png(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "png", selection)

		self.ls_png.connect("changed", set_ls_png)

		####################### Connect the GIF Files Combobox ############################

		self.ls_gif = gtkbuilder.get_object("ls_gif")
		self.ls_gif.set_active(ls_colors_inv[config.cfo["LSColors"]["gif"]])

		def set_ls_gif(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "gif", selection)

		self.ls_gif.connect("changed", set_ls_gif)

		####################### Connect the MP3 Files Combobox ############################

		self.ls_mp3 = gtkbuilder.get_object("ls_mp3")
		self.ls_mp3.set_active(ls_colors_inv[config.cfo["LSColors"]["mp3"]])

		def set_ls_mp3(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "mp3", selection)

		self.ls_mp3.connect("changed", set_ls_mp3)

		####################### Connect the OGG Files Combobox ############################

		self.ls_ogg = gtkbuilder.get_object("ls_ogg")
		self.ls_ogg.set_active(ls_colors_inv[config.cfo["LSColors"]["ogg"]])

		def set_ls_ogg(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "ogg", selection)

		self.ls_ogg.connect("changed", set_ls_ogg)

		####################### Connect the FLAC Files Combobox ###########################

		self.ls_flac = gtkbuilder.get_object("ls_flac")
		self.ls_flac.set_active(ls_colors_inv[config.cfo["LSColors"]["flac"]])

		def set_ls_flac(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "flac", selection)

		self.ls_flac.connect("changed", set_ls_flac)

		####################### Connect the TAR Files Combobox ############################

		self.ls_tar = gtkbuilder.get_object("ls_tar")
		self.ls_tar.set_active(ls_colors_inv[config.cfo["LSColors"]["tar"]])

		def set_ls_tar(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "tar", selection)

		self.ls_tar.connect("changed", set_ls_tar)

		####################### Connect the TARGZ Files Combobox ##########################

		self.ls_targz = gtkbuilder.get_object("ls_targz")
		self.ls_targz.set_active(ls_colors_inv[config.cfo["LSColors"]["targz"]])

		def set_ls_targz(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "targz", selection)

		self.ls_targz.connect("changed", set_ls_targz)

		####################### Connect the TARBZ2 Files Combobox #########################

		self.ls_tarbz2 = gtkbuilder.get_object("ls_tarbz2")
		self.ls_tarbz2.set_active(ls_colors_inv[config.cfo["LSColors"]["tarbz2"]])

		def set_ls_tarbz2(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "tarbz2", selection)

		self.ls_tarbz2.connect("changed", set_ls_tarbz2)

		####################### Connect the ZIP Files Combobox ############################

		self.ls_zip = gtkbuilder.get_object("ls_zip")
		self.ls_zip.set_active(ls_colors_inv[config.cfo["LSColors"]["zip"]])

		def set_ls_zip(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "zip", selection)

		self.ls_zip.connect("changed", set_ls_zip)

		####################### Connect the RAR Files Combobox ############################

		self.ls_rar = gtkbuilder.get_object("ls_rar")
		self.ls_rar.set_active(ls_colors_inv[config.cfo["LSColors"]["rar"]])

		def set_ls_rar(widget, data=None):
			selection = widget.get_active()
			set_ls_color(self, "rar", selection)

		self.ls_rar.connect("changed", set_ls_rar)

		WidgetHandler.InitWidget("ls_custom", "LSColors", "custom", "text", config.cfo, config.udc, config.fdc)

		####################### Connect the PROMPT_COMMAND TextView ########################

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

		####################### Connect the PS1 TextView ##################################

		self.custom_prompt = gtkbuilder.get_object("custom_prompt")

		self.custom_prompt_buffer = undobuffer.UndoableBuffer()
		self.custom_prompt.set_buffer(self.custom_prompt_buffer)
		self.custom_prompt_buffer.set_text("%s" % config.cfo["Custom"]["prompt"])

		def set_custom_prompt(widget, data=None):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			config.cfo["Custom"]["prompt"] = widget.get_text(start, end, False)

		self.custom_prompt_buffer.connect("changed", set_custom_prompt)

		##

		self.place_p_c = gtkbuilder.get_object("place_p_c")

		def do_place_p_c(widget, data=None):
			self.prompt_command.set_sensitive(1)
			self.custom_prompt.set_sensitive(0)
			self.active_buffer = "P_C"

		self.place_p_c.connect("clicked", do_place_p_c)

		##

		self.place_ps1 = gtkbuilder.get_object("place_ps1")

		def do_place_ps1(widget, data=None):
			self.prompt_command.set_sensitive(0)
			self.custom_prompt.set_sensitive(1)
			self.active_buffer = "PS1"

		self.place_ps1.connect("clicked", do_place_ps1)

		##

		def prompt_add(text):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.insert_at_cursor(text)
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.insert_at_cursor(text)

		##

		def prompt_set(text):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.set_text(text)
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.set_text(text)

		####################### Connect the Use Custom Prompt Button #######################

		self.use_custom_prompt = gtkbuilder.get_object("use_custom_prompt")
		self.use_custom_prompt.set_active(config.cfo["Custom"].as_bool("use_custom_prompt"))

		def set_use_custom_prompt(widget, data=None):
			config.cfo["Custom"]["use_custom_prompt"] = widget.get_active()

		self.use_custom_prompt.connect("clicked", set_use_custom_prompt)

		####################### Connect the Show Toolbox Button ###########################

		self.show_toolbox = gtkbuilder.get_object("show_toolbox")

		def do_show_toolbox(widget, data=None):
			toolbox = gtkbuilder.get_object("Toolbox")
			toolbox.show_all()
			toolbox.connect("delete-event", lambda w, e: w.hide() or True)

		self.show_toolbox.connect("clicked", do_show_toolbox)

		####################### Connect the Username Button ###############################

		self.username = gtkbuilder.get_object("username")

		def set_username(widget, data=None):
			prompt_add("\\u")

		self.username.connect("clicked", set_username)

		####################### Connect the Hostname Button ###############################

		self.hostname = gtkbuilder.get_object("hostname")

		def set_hostname(widget, data=None):
			prompt_add("\\h")

		self.hostname.connect("clicked", set_hostname)

		####################### Connect the Fullhostname Button ###########################

		self.fhostname = gtkbuilder.get_object("fhostname")

		def set_fhostname(widget, data=None):
			prompt_add("\\H")

		self.fhostname.connect("clicked", set_fhostname)

		####################### Connect the Time Button ###################################

		self.time = gtkbuilder.get_object("time")

		def set_time(widget, data=None):
			prompt_add("\\t")

		self.time.connect("clicked", set_time)

		####################### Connect the Date Button ###################################

		self.date = gtkbuilder.get_object("date")

		def set_date(widget, data=None):
			prompt_add("\\d")

		self.date.connect("clicked", set_date)

		####################### Connect the Sign Button ###################################

		self.sign = gtkbuilder.get_object("sign")

		def set_sign(widget, data=None):
			prompt_add("\\$")

		self.sign.connect("clicked", set_sign)

		####################### Connect the Full Workdir Button ###########################

		self.fworkdir = gtkbuilder.get_object("fworkdir")

		def set_fworkdir(widget, data=None):
			prompt_add("\\w")

		self.fworkdir.connect("clicked", set_fworkdir)

		####################### Connect the Base Workdir Button ############################

		self.workdir = gtkbuilder.get_object("workdir")

		def set_workdir(widget, data=None):
			prompt_add("\\W")

		self.workdir.connect("clicked", set_workdir)

		####################### Connect the EUID Button ###################################

		self.euid = gtkbuilder.get_object("euid")

		def set_euid(widget, data=None):
			prompt_add("\\$EUID")

		self.euid.connect("clicked", set_euid)

		####################### Connect the Jobs Button ###################################

		self.jobs = gtkbuilder.get_object("jobs")

		def set_jobs(widget, data=None):
			prompt_add("\\j")

		self.jobs.connect("clicked", set_jobs)

		####################### Connect the History Number Button #########################

		self.bang = gtkbuilder.get_object("bang")

		def set_bang(widget, data=None):
			prompt_add("\\!")

		self.bang.connect("clicked", set_bang)

		####################### Connect the Session Number Button #########################

		self.number = gtkbuilder.get_object("number")

		def set_number(widget, data=None):
			prompt_add("\\#")

		self.number.connect("clicked", set_number)

		####################### Connect the Bash PID Button ###############################

		self.pid = gtkbuilder.get_object("pid")

		def set_pid(widget, data=None):
			prompt_add("$BASHPID")

		self.pid.connect("clicked", set_pid)

		####################### Connect the Shelllevel Button #############################

		self.shlvl = gtkbuilder.get_object("shlvl")

		def set_shlvl(widget, data=None):
			prompt_add("$SHLVL")

		self.shlvl.connect("clicked", set_shlvl)

		####################### Connect the TruncPWD Button ###############################

		self.truncpwd = gtkbuilder.get_object("truncpwd")

		def set_truncpwd(widget, data=None):
			prompt_add("\\$(trunc_pwd)")

		self.truncpwd.connect("clicked", set_truncpwd)

		####################### Connect the Showsize Button #############################

		self.showsize = gtkbuilder.get_object("showsize")

		def set_showsize(widget, data=None):
			prompt_add("\\$(show_size)")

		self.showsize.connect("clicked", set_showsize)

		####################### Connect the Countfiles Combobox ###########################

		self.countfiles = gtkbuilder.get_object("countfiles")
		self.countfiles.set_active(0)

		counters = {
			    1 : "\\$(count_files +f)",
			    2 : "\\$(count_files -f)",
			   }

		def set_countfiles(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(counters[selection])

		self.countfiles.connect("changed", set_countfiles)

		####################### Connect the Countprocesses Button #########################

		self.countprocesses = gtkbuilder.get_object("countprocesses")

		def set_countprocesses(widget, data=None):
			prompt_add("\\$(count_processes)")

		self.countprocesses.connect("clicked", set_countprocesses)

		####################### Connect the Showuptime Button #############################

		self.showuptime = gtkbuilder.get_object("showuptime")

		def set_showuptime(widget, data=None):
			prompt_add("\\$(show_uptime)")

		self.showuptime.connect("clicked", set_showuptime)

		####################### Connect the Showload Button ###############################

		self.showload = gtkbuilder.get_object("showload")
		self.showload.set_active(0)

		load_getters = {
				1 : "\\$(show_system_load 1)",
				2 : "\\$(show_system_load 10)",
				3 : "\\$(show_system_load 15)",
			       }

		def set_showload(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(load_getters[selection])

		self.showload.connect("changed", set_showload)

		####################### Connect the ShowTTY Button ################################

		self.showtty = gtkbuilder.get_object("showtty")

		def set_showtty(widget, data=None):
			prompt_add("\\$(showtty)")

		self.showtty.connect("clicked", set_showtty)

		####################### Connect the Showmem Combobox ##############################

		self.showmem = gtkbuilder.get_object("showmem")
		self.showmem.set_active(0)

		memory_getters = {
				  1 : "\\$(show_mem --used)",
				  2 : "\\$(show_mem --free)",
				  3 : "\\$(show_mem --used-percent)",
				  4 : "\\$(show_mem --free-percent)",
				 }

		def set_showmem(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(memory_getters[selection])

		self.showmem.connect("changed", set_showmem)

		####################### Connect the Showcpuload Button #############################

		self.showcpuload = gtkbuilder.get_object("showcpuload")

		def set_showcpuload(widget, data=None):
			prompt_add("\\$(show_cpu_load)")

		self.showcpuload.connect("clicked", set_showcpuload)

		####################### Connect the Showbatteryload Combobox ######################

		self.showbatteryload = gtkbuilder.get_object("showbatteryload")
		self.showbatteryload.set_active(0)

		battery_getters = {
				   1 : "\\$(show_battery_load --acpi)",
				   2 : "\\$(show_battery_load --apm)",
				  }

		def set_showbatteryload(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(battery_getters[selection])

		self.showbatteryload.connect("changed", set_showbatteryload)

		####################### Connect the Showspace Combobox #############################

		self.showspace = gtkbuilder.get_object("showspace")
		self.showspace.set_active(0)

		space_getters = {
				  1 : "\\$(show_space --used <device>)",
				  2 : "\\$(show_space --free <device>)",
				  3 : "\\$(show_space --used-percent <device>)",
				  4 : "\\$(show_space --free-percent <device>)",
				 }

		def set_showspace(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(space_getters[selection])

		self.showspace.connect("changed", set_showspace)

		####################### Connect the bash seconds Button ###########################

		self.showseconds = gtkbuilder.get_object("showseconds")

		def set_showseconds(widget, data=None):
			prompt_add("${SECONDS}")

		self.showseconds.connect("clicked", set_showseconds)

		####################### Connect the empty PROMPT_COMMAND Button ###################

		self.empty_pc = gtkbuilder.get_object("empty_pc")

		def do_empty_pc(widget, data=None):
			self.prompt_command_buffer.set_text("")

		self.empty_pc.connect("clicked", do_empty_pc)

		####################### Connect the undo PROMPT_COMMAND Button ####################

		self.undo_pc = gtkbuilder.get_object("undo_pc")

		def do_undo_pc(widget, data=None):
			self.prompt_command_buffer.undo()

		self.undo_pc.connect("clicked", do_undo_pc)

		####################### Connect the undo PROMPT_COMMAND Button ####################

		self.redo_pc = gtkbuilder.get_object("redo_pc")

		def do_redo_pc(widget, data=None):
			self.prompt_command_buffer.redo()

		self.redo_pc.connect("clicked", do_redo_pc)

		####################### Connect the emtpy PS1 Button ##############################

		self.empty_ps1 = gtkbuilder.get_object("empty_ps1")

		def do_empty_ps1(widget, data=None):
			self.custom_prompt_buffer.set_text("")

		self.empty_ps1.connect("clicked", do_empty_ps1)

		####################### Connect the undo PS1 Button ####################

		self.undo_ps1 = gtkbuilder.get_object("undo_ps1")

		def do_undo_ps1(widget, data=None):
			self.custom_prompt_buffer.undo()

		self.undo_ps1.connect("clicked", do_undo_ps1)

		####################### Connect the redo PS1 Button ####################

		self.redo_ps1 = gtkbuilder.get_object("redo_ps1")

		def do_redo_ps1(widget, data=None):
			self.custom_prompt_buffer.redo()

		self.redo_ps1.connect("clicked", do_redo_ps1)

		####################### Connect the Insert Symbolic Color Combobox ################

		self.insert_color = gtkbuilder.get_object("insert_color")
		self.insert_color.set_active(0)

		symbolic_colors = {
				   1 : "$usercolor",
				   2 : "$hostcolor",
				   3 : "$datecolor",
				   4 : "$timecolor",
				   5 : "$wdircolor",
				   6 : "$fontcolor",
				   7 : "$sepacolor",
				   8 : "$upcolor",
				   9 : "$pscolor",
				  }

		def do_insert_color(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				prompt_add(symbolic_colors[selection])

		self.insert_color.connect("changed", do_insert_color)

				####################### Connect the Insert Style Combobox #########################

		self.insert_prompt = gtkbuilder.get_object("insert_prompt")
		self.insert_prompt.set_active(0)

		styles_pc = {
			      1 : "",
			      2 : "",
			      3 : "let prompt_x=$(tput cols)-29\
\ntput sc\
\ntput cup 0 ${prompt_x}\
\necho -n \"[ $(date '+%a, %d %b %y') :: $(date +%T) ]\"\
\ntput rc",
			      4 : "user=\"whoami\"\
\nhost=$(echo -n $HOSTNAME | sed -e \"s/[\.].*//\")\
\ndirchar=$(ini_get directory_indicator)\
\ntrunc_symbol=$(ini_get pwdcut)\
\ntrunc_length=$(($(echo $trunc_symbol | wc -m)-1))\
\n\
\nj=4 k=6 l=8 m=10 newPWD=\"${PWD}\" fill=\"\"\
\n\
\nlet promptsize=$(echo -n \"--($user @ $host)---(${PWD})-------\" | wc -c | tr -d \" \")\
\nlet fillsize=${COLUMNS}-${promptsize}\
\n\
\nwhile [ \"$fillsize\" -gt \"0\" ]; do\
\n	fill=\"${fill}─\"; let fillsize=${fillsize}-1\
\ndone\
\n\
\nif [ \"$fillsize\" -lt \"0\" ]; then\
\n	let cutt=${trunc_length}-${fillsize}\
\n	xPWD=\"${trunc_symbol}$(echo -n $PWD | sed -e \"s/\(^.\{$cutt\}\)\(.*\)/\\2/\")\"\
\n	newPWD=\"${xPWD//\//$dirchar}\"\
\nelse	newPWD=\"${PWD//\//$dirchar}\"\
\nfi\
\n\
\n_newPWD () {\
\n	echo -e $newPWD \
\n}\
\n\
\necho -en \"\\033[2;$((${COLUMNS}-29))H\"\
\necho -en \"( $(date +%H:%M) : $(date '+%a, %d %b %y') )────┐\"\
\necho -en \"\\033[2;${COLUMNS}H\"\
\ni=${LINES}\
\n\
\nwhile [ $i -ge 4 ]; do\
\n   if [[ $i == $j ]]; then\
\n	echo -en \"\\033[$j;$((${COLUMNS}-29))H\"\
\n	echo -en \"( system-load: $(show_system_load 1) )────────\"\
\n   fi\
\n   if [[ $i == $k ]]; then\
\n	echo -en \"\\033[$k;$((${COLUMNS}-29))H\"\
\n	echo -en \"( cpu-load: $(show_cpu_load) )────────────\"\
\n   fi\
\n   if [[ $i == $l ]]; then\
\n	echo -en \"\\033[$l;$((${COLUMNS}-29))H\"\
\n	echo -en \"( ram: $(show_mem --used)mb / $(show_mem --free)mb )─────\"\
\n   fi\
\n   if [[ $i == $m ]]; then\
\n	echo -en \"\\033[$m;$((${COLUMNS}-29))H\"\
\n	echo -en \"( processes: $(count_processes) )──────────\"\
\n   fi\
\n   echo -en \"\\033[$(($i-1));${COLUMNS}H│\"\
\n   let i=$i-1\
\ndone\
\nlet prompt_line=${LINES}-1",
			      5 : "",
			      6 : "\
\nlocal one=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\)/\\1/\" -e \"s/ //g\")\
\nlocal five=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\).*/\\2/\" -e \"s/ //g\")\
\nlocal diff1_5=$(echo -e \"scale = scale ($one) \\nx=$one - $five\\n if (x>0) {print \\\"up\\\"} else {print \\\"down\\\"}\\n print x \\nquit \\n\" | bc)\
\nloaddiff=\"$(echo -n \"${one}${diff1_5}\" | sed -e 's/down\-/down/g')\"\
\
\nlet files=$(ls -l | grep \"^-\" | wc -l | tr -d \" \")\
\nlet hiddenfiles=$(ls -l -d .* | grep \"^-\" | wc -l | tr -d \" \")\
\nlet executables=$(ls -l | grep ^-..x | wc -l | tr -d \" \")\
\nlet directories=$(ls -l | grep \"^d\" | wc -l | tr -d \" \")\
\nlet hiddendirectories=$(ls -l -d .* | grep \"^d\" | wc -l | tr -d \" \")-2\
\nlet linktemp=$(ls -l | grep \"^l\" | wc -l | tr -d \" \")\
\
\nif [ \"$linktemp\" -eq \"0\" ]\
\nthen\
\nlinks=\"\"\
\nelse\
\nlinks=\" ${linktemp}l\"\
\nfi\
\nunset linktemp\
\nlet devicetemp=$(ls -l | grep \"^[bc]\" | wc -l | tr -d \" \")\
\
\nif [ \"$devicetemp\" -eq \"0\" ]\
\nthen\
\ndevices=\"\"\
\nelse\
\ndevices=\" ${devicetemp}bc\"\
\nfi\
\nunset devicetemp",
			      7 : "",
			      8 : "",
			      9 : "",
			     10 : "",
			     11 : "",
			     12 : "newPWD=\"${PWD}\"\
\nuser=\"whoami\"\
\nhost=$(echo -n $HOSTNAME | sed -e \"s/[\.].*//\")\
\ndatenow=$(date \"+%a, %d %b %y\")\
\nlet promptsize=$(echo -n \"┌( $user @ $host ddd., DD mmm YY)( ${PWD} )┐\" | wc -c | tr -d \" \")\
\n\
\nlet fillsize=${COLUMNS}-${promptsize}\
\n\
\nfill=\"\"\
\nwhile [ \"$fillsize\" -gt \"0\" ]\
\ndo\
\n    fill=\"${fill}─\"\
\n	let fillsize=${fillsize}-1\
\ndone\
\nif [ \"$fillsize\" -lt \"0\" ]\
\nthen\
\n    let cutt=3-${fillsize}\
\n    newPWD=\"...$(echo -n $PWD | sed -e \"s/\(^.\{$cutt\}\)\(.*\)/\2/\")\"\
\nfi",
			    }

		styles_ps1 = {
			       1 : "\\n\u @ \h | \d | \\t | \\$(trunc_pwd)\n$ -> ",
			       2 : "\\n┌( \u @ \h )─( \$(date +%I:%M%P) -:- \$(date +%m)/\$(date +%d) )\\n└( \$(trunc_pwd) )·> ",
			       3 : "[ \u @ \h : \$(trunc_pwd) ] ",
			       4 : "\[\\033[\${prompt_line};0H\]\\n┌─( \u @ \h )─\${fill}─( \$(_newPWD) )────┘\\n└─( uptime: \$(show_uptime) : $ )·> ",
			       5 : "\\n┌─[ \u @ \h ]─[ job #\# ]─[ \$(show_tty) ]─[ \$(date +%H:%M:%S): \$(date +%m/%d/%y) : \$(show_uptime) ]\\n└─[ $ : \$(trunc_pwd) ]·> ",
			       6 : "\\n[ \$(date +%T) - \$(date +%D) ]\
[ \u @ \h ]\ [ \${files}.\${hiddenfiles}-\${executables}x \$(show_size) \
\${directories}.\${hiddendirectories}d\${links}\${devices} ][ \${loaddiff} ][ \
\$(ps ax | wc -l | sed -e \\\"s: ::g\\\")proc ]\\n[ \$(trunc_pwd) ] $ ",
			       7 : "\\n[ \\t ] \u \$(trunc_pwd) $ ",
			       8 : "\\n.:[ \u @ \h ]:. .:[ \$(trunc_pwd) ]:.\n.:[·> ",
			       9: "\\n⊏⁅ \u ⁑ \h ⁆⁅ \d ⁑ \\t ⁑ \$(show_uptime) ⁆⊐\\n⊏⁅ \$(trunc_pwd) ⁆⊐≻ ",
			      10 : "\\n -( \u / \h )-( \$(show_tty) )-( uptime: \$(show_uptime) )-( \$(date +%H:%M) \
\$(date +%d-%b-%y ) )-( files: \$(count_files +f) / folders: \$(count_files -d) )-\\n -< \$(trunc_pwd) >- ",
			      11 : "\\n♦♦( \u @ \h : Space on /: \$(show_space --used /) used of \$(show_space --total /) )♦♦( \$(trunc_pwd) )♦♦\\n♦♦( \$(date +%H:%M) → \$(date \\\"+%a, %d %b %y\\\") : uptime : \$(show_uptime) \$ )♦♦ ",
			      12 : "┌─( \u @ \h \$(date \"+%a, %d %b %y\") )─\${fill}─( \$newPWD \
)─<\n└─( \$(date \"+%H:%M\") \$ )─> ",
			     }

		def do_insert_prompt(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				self.prompt_command_buffer.set_text(styles_pc[selection])
				self.custom_prompt_buffer.set_text(styles_ps1[selection])

		self.insert_prompt.connect("changed", do_insert_prompt)

		####################### Load the Main-Window #######################################
		self.bashstyle = gtkbuilder.get_object("bashstyle")

		def destroy(self, widget):
			config.WriteConfig()
			lock.Remove()
			Gtk.main_quit()

		self.bashstyle.connect("destroy", destroy, None)

		####################### Load the Notebook ##########################################
		notebook = gtkbuilder.get_object("notebook")
		notebook.set_current_page(int(initial_page))

		####################### Load last two buttons ######################################
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
