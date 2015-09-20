#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2015 Christopher Bratusek		#
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

class PromptBuilder(object):

	def __init__(self, config, userconfig, factoryconfig):
		######################## load translations & widgethandler #########################
		gtkbuilder = widgethandler.gtkbuilder

		######################## GtkTextView ###############################################

		self.prompt_command = gtkbuilder.get_object("prompt_command")

		self.prompt_command_buffer = undobuffer.UndoableBuffer()
		self.prompt_command.set_buffer(self.prompt_command_buffer)
		self.prompt_command_buffer.set_text("%s" % config["Custom"]["command"])

		self.custom_prompt = gtkbuilder.get_object("custom_prompt")

		self.custom_prompt_buffer = undobuffer.UndoableBuffer()
		self.custom_prompt.set_buffer(self.custom_prompt_buffer)
		self.custom_prompt_buffer.set_text("%s" % config["Custom"]["prompt"])

		def set_custom_prompt(widget, setting):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			config["Custom"]["{}".format(setting)] = widget.get_text(start, end, False)

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
				if self.active_buffer == "P_C":
					text = dict_p_c[widget.get_active()]
				elif self.active_buffer == "PS1":
					text = dict_ps1[widget.get_active()]
				prompt_add(widget, text)
				widget.set_active(0)

		######################## GtkButtons ################################################

		self.empty = gtkbuilder.get_object("cpb_empty")
		self.undo = gtkbuilder.get_object("cpb_undo")
		self.redo = gtkbuilder.get_object("cpb_redo")
		self.reset = gtkbuilder.get_object("cpb_reset")
		self.factory = gtkbuilder.get_object("cpb_factory")

		def do_empty(widget):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.set_text("")
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.set_text("")

		def do_undo(widget):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.undo()
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.undo()

		def do_redo(widget):
			if self.active_buffer == "P_C":
				self.prompt_command_buffer.redo()
			elif self.active_buffer == "PS1":
				self.custom_prompt_buffer.redo()

		def do_reset(widget):
			self.prompt_command_buffer.set_text("%s" % userconfig["Custom"]["command"])
			self.custom_prompt_buffer.set_text("%s" % userconfig["Custom"]["prompt"])

		def do_revert(widget):
			self.prompt_command_buffer.set_text("%s" % factoryconfig["Custom"]["command"])
			self.custom_prompt_buffer.set_text("%s" % factoryconfig["Custom"]["prompt"])

		self.empty.connect("clicked", do_empty)
		self.undo.connect("clicked", do_undo)
		self.redo.connect("clicked", do_redo)
		self.reset.connect("clicked", do_reset)
		self.factory.connect("clicked", do_revert)

		######################## Toolbox ###################################################

		self.show_toolbox = gtkbuilder.get_object("show_toolbox")

		def do_show_toolbox(widget, data=None):
                        toolbox = gtkbuilder.get_object("Toolbox")
                        toolbox_close = gtkbuilder.get_object("toolbox.close")
                        toolbox.show_all()
                        toolbox_close.connect("clicked", lambda w: toolbox.hide() or True)
                        toolbox.connect("delete-event", lambda w, e: w.hide() or True)

		self.show_toolbox.connect("clicked", do_show_toolbox)

		######################## Toolbox Buttons ###########################################

		def load_toolbutton(object, text_p_c, text_ps1):
			widget = gtkbuilder.get_object("%s" % object)
			widget.connect("clicked", prompt_add, text_p_c, text_ps1)

		load_toolbutton("username", "${USER}", "\\u")
		load_toolbutton("hostname", "${HOSTNAME/.*}", "\\h")
		load_toolbutton("fhostname", "${HOSTNAME}", "\\H")
		load_toolbutton("time", "$(date +%H:%M:%S)", "\\t")
		load_toolbutton("date", "$(date date +%d.%m.%Y)", "\\d")
		load_toolbutton("sign", "", "\\$")
		load_toolbutton("fworkdir", "${PWD}", "\\w")
		load_toolbutton("workdir", "${PWD/*\/}", "\\W")
		load_toolbutton("euid", "${EUID}", "${EUID}")
		load_toolbutton("jobs", "$(jobs -pr)", "\\j")
		load_toolbutton("bang", "", "\\!")
		load_toolbutton("number", "", "\\#")
		load_toolbutton("pid", "${BAHSPID}", "${BASHPID}")
		load_toolbutton("shlvl", "${SHLVL}", "${SHLVL}")
		load_toolbutton("truncpwd", "$(truncpwd)", "\\$(truncpwd)")
		load_toolbutton("showsize", "$(systemkit dirsize)", "\\$(systemkit dirsize)")
		load_toolbutton("countprocesses", "$(systemkit processes)", "\\$(systemkit processes)")
		load_toolbutton("showuptime", "$(systemkit uptime)", "\\$(systemkit uptime)")
		load_toolbutton("showtty", "$(systemkit tty)", "\\$(systemkit tty)")
		load_toolbutton("showcpuload", "$(systemkit cpuload)", "\\$(systemkit cpuload)")
		load_toolbutton("showseconds", "${SECONDS}", "${SECONDS}")
		load_toolbutton("showbatteryload", "$(systemkit battery)", "\\$(systemkit battery)")
		load_toolbutton("showexit", "${lastexit}", "${lastexit}")
		load_toolbutton("showlastcmd", "${lastcommand}", "${lastcommand}")
		load_toolbutton("showlastcmd_cut", "${lastcommandprintable}", "${lastcommandprintable}")

		######################## Toolbox Comboboxes ########################################

		def load_toolcombo(object, dict_p_c, dict_ps1):
			widget = gtkbuilder.get_object("%s" % object)
			widget.set_active(0)
			widget.connect("changed", prompt_add_combo, dict_p_c, dict_ps1)

		load_toolcombo("showmem", dicts.memory_getters_p_c, dicts.memory_getters_ps1)
		load_toolcombo("showspace", dicts.space_getters_p_c, dicts.space_getters_ps1)
		load_toolcombo("countfiles", dicts.counters_p_c, dicts.counters_ps1)
		load_toolcombo("showload", dicts.load_getters_p_c, dicts.load_getters_ps1)
		load_toolcombo("insert_color", dicts.symbolic_colors_p_c, dicts.symbolic_colors_ps1)

		######################## Default Styles ############################################

		self.insert_prompt = gtkbuilder.get_object("insert_prompt")
		self.insert_prompt.set_active(0)

		styles_pc = {
			      1 : prompts.empty_pc,
			      2 : prompts.empty_pc,
			      3 : prompts.floating_clock_pc,
			      4 : prompts.equinox_pc,
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
			       4 : prompts.equinox_ps,
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
