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

class PromptBuilder(object):

	def __init__(self, config):
		######################## load translations & widgethandler #########################
		gtkbuilder = widgethandler.gtkbuilder
		lang = i18n.Gettext()
		lang.SetLang()
		
		self.prompt_command = gtkbuilder.get_object("prompt_command")

		self.prompt_command_buffer = undobuffer.UndoableBuffer()
		self.prompt_command.set_buffer(self.prompt_command_buffer)
		self.prompt_command_buffer.set_text("%s" % config["Custom"]["command"])

		def set_prompt_command(widget, data=None):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			config["Custom"]["command"] = widget.get_text(start, end, False)

		self.prompt_command_buffer.connect("changed", set_prompt_command)

		self.active_buffer = "P_C"

		self.custom_prompt = gtkbuilder.get_object("custom_prompt")

		self.custom_prompt_buffer = undobuffer.UndoableBuffer()
		self.custom_prompt.set_buffer(self.custom_prompt_buffer)
		self.custom_prompt_buffer.set_text("%s" % config["Custom"]["prompt"])

		def set_custom_prompt(widget, data=None):
			start = widget.get_start_iter()
			end = widget.get_end_iter()
			config["Custom"]["prompt"] = widget.get_text(start, end, False)

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
