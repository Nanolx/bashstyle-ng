#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2020 Christopher Bratusek		#
#							#
#########################################################

MODULES = [ 'sys', 'undobuffer', 'widgethandler', 'dicts', 'prompts' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

try:
	from gi.repository import Gtk
except ImportError:
	FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

gtkbuilder = widgethandler.gtkbuilder

class PromptBuilder(object):

	def __init__(self, cfo, udc, fdc):
		self.config = cfo
		self.userdefault = udc
		self.factorydefault = fdc

	def InitPromptBuilder(self):

		WidgetHandler = widgethandler.WidgetHandler(self.config, self.userdefault, self.factorydefault)

		######################## GtkTextView ###############################################

		self.prompt_command = gtkbuilder.get_object("prompt_command")

		self.prompt_command_buffer = undobuffer.UndoableBuffer()
		self.prompt_command.set_buffer(self.prompt_command_buffer)
		self.prompt_command_buffer.set_text("%s" % self.config["Custom"]["command"])

		self.custom_prompt = gtkbuilder.get_object("custom_prompt")

		self.custom_prompt_buffer = undobuffer.UndoableBuffer()
		self.custom_prompt.set_buffer(self.custom_prompt_buffer)
		self.custom_prompt_buffer.set_text("%s" % self.config["Custom"]["prompt"])

		def set_custom_prompt(widget, setting):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			self.config["Custom"]["{}".format(setting)] = widget.get_text(start, end, False)

		self.prompt_command_buffer.connect("changed", set_custom_prompt, "command")
		self.custom_prompt_buffer.connect("changed", set_custom_prompt, "prompt")

		self.active_buffer = "P_C"

		def set_active_buffer(widget, data, buffer):
			self.active_buffer = buffer

		self.prompt_command.connect("focus-in-event", set_active_buffer, "P_C")
		self.custom_prompt.connect("focus-in-event", set_active_buffer, "PS1")

		######################## Helper Functions ##########################################

		def prompt_add(widget, text_p_c, text_ps1):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.insert_at_cursor(text_p_c)
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.insert_at_cursor(text_ps1)

		def prompt_add_combo(widget, dict_p_c, dict_ps1):
			if widget.get_active() != 0:
				prompt_add(widget, dict_p_c[widget.get_active()], dict_ps1[widget.get_active()])
				widget.set_active(0)

		######################## GtkButtons ################################################

		def do_empty(widget, data):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.set_text("")
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.set_text("")

		def do_undo(widget, data):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.undo()
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.undo()

		def do_redo(widget, data):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.redo()
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.redo()

		def do_reset(widget, data):
			self.prompt_command_buffer.set_text("%s" % self.userdefault["Custom"]["command"])
			self.custom_prompt_buffer.set_text("%s" % self.userdefault["Custom"]["prompt"])

		def do_revert(widget, data):
			self.prompt_command_buffer.set_text("%s" % self.factorydefault["Custom"]["command"])
			self.custom_prompt_buffer.set_text("%s" % self.factorydefault["Custom"]["prompt"])

		WidgetHandler.InitWidget("cpb_empty", do_empty, None, "button", None)
		WidgetHandler.InitWidget("cpb_undo", do_undo, None, "button", None)
		WidgetHandler.InitWidget("cpb_redo", do_redo, None, "button", None)
		WidgetHandler.InitWidget("cpb_reset", do_reset, None, "button", None)
		WidgetHandler.InitWidget("cpb_factory", do_revert, None, "button", None)

		######################## Toolbox ###################################################

		def do_show_toolbox(widget, data):
			toolbox = gtkbuilder.get_object("Toolbox")
			toolbox_close = gtkbuilder.get_object("toolbox.close")
			toolbox.show_all()
			toolbox_close.connect("clicked", lambda w: toolbox.hide() or True)
			toolbox.connect("delete-event", lambda w, e: w.hide() or True)

		WidgetHandler.InitWidget("show_toolbox", do_show_toolbox, None, "button", None)

		######################## Toolbox Buttons ###########################################

		WidgetHandler.InitWidget("username", "${USER}", "\\u", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("hostname", "${HOSTNAME/.*}", "\\h", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("fhostname", "${HOSTNAME}", "\\H", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("time", "$(date +%H:%M:%S)", "\\t", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("date", "$(date date +%d.%m.%Y)", "\\d", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("sign", "", "\\$", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("fworkdir", "${PWD}", "\\w", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("workdir", "${PWD/*\/}", "\\W", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("euid", "${EUID}", "${EUID}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("jobs", "$(jobs -pr)", "\\j", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("bang", "", "\\!", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("number", "", "\\#", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("pid", "${BAHSPID}", "${BASHPID}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("shlvl", "${SHLVL}", "${SHLVL}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("truncpwd", "$(truncpwd)", "\\$(truncpwd)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showsize", "$(systemkit dirsize)", "\\$(systemkit dirsize)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("countprocesses", "$(systemkit processes)", "\\$(systemkit processes)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showuptime", "$(systemkit uptime)", "\\$(systemkit uptime)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showtty", "$(systemkit tty)", "\\$(systemkit tty)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showcpuload", "$(systemkit cpuload)", "\\$(systemkit cpuload)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showseconds", "${SECONDS}", "${SECONDS}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showbatteryload", "$(systemkit battery)", "\\$(systemkit battery)", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showexit", "${lastexit}", "${lastexit}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showlastcmd", "${lastcommand}", "${lastcommand}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showlastcmd_cut", "${lastcommandprintable}", "${lastcommandprintable}", "cpb_button", prompt_add)
		WidgetHandler.InitWidget("showuser", "${showuser}", "\\$(showuser)", "cpb_button", prompt_add)

		######################## Toolbox Comboboxes ########################################

		WidgetHandler.InitWidget("showmem", dicts.memory_getters_p_c, dicts.memory_getters_ps1, "cpb_combo", prompt_add_combo)
		WidgetHandler.InitWidget("showspace", dicts.space_getters_p_c, dicts.space_getters_ps1, "cpb_combo", prompt_add_combo)
		WidgetHandler.InitWidget("countfiles", dicts.counters_p_c, dicts.counters_ps1, "cpb_combo", prompt_add_combo)
		WidgetHandler.InitWidget("showload", dicts.load_getters_p_c, dicts.load_getters_ps1, "cpb_combo", prompt_add_combo)
		WidgetHandler.InitWidget("insert_color", dicts.symbolic_colors_p_c, dicts.symbolic_colors_ps1, "cpb_combo", prompt_add_combo)

		######################## Default Styles ############################################

		self.insert_prompt = gtkbuilder.get_object("insert_prompt")
		self.insert_prompt.set_active(0)

		def do_insert_prompt(widget, data=None):
			selection = widget.get_active()
			if selection != 0:
				self.prompt_command_buffer.set_text(prompts.styles_pc[selection])
				self.custom_prompt_buffer.set_text(prompts.styles_ps1[selection])

		self.insert_prompt.connect("changed", do_insert_prompt)
