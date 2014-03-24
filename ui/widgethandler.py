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

MODULES = [ 'os', 'misc', 'sys' ]

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
DATADIR = os.getenv('BSNG_DATADIR')
blacklist = ['', '\"'] #\'
gtkbuilder = Gtk.Builder()
gtkbuilder.set_translation_domain("bs-ng")
gtkbuilder.add_from_file(DATADIR + "/bashstyle-ng/ui/bashstyle8.ui")

class WidgetHandler(object):
		####################### metafuncs for handling widgets ###########################
		def __init__(self, cfo, udc, fdc):
			self.config = cfo
			self.userdefault = udc
			self.factorydefault = fdc

		def InitWidget(self, widget, group, setting, type, dict):

			def LoadWidget():
				object = gtkbuilder.get_object("%s" % widget)
				return object

			def LoadValue():
				if type == "text":
					object.set_text("%s" % self.config["%s" % group]["%s" % setting])
				elif type == "int":
					object.set_value(self.config["%s" % group].as_int("%s" % setting))
				elif type == "bool":
					object.set_active(self.config["%s" % group].as_bool("%s" % setting))
				elif type == "combo":
					object.set_active(misc.SwapDictionary(dict)[self.config["%s" % group]["%s" % setting]])

			def ConnectSignals():
				if type == "text":
					object.connect("insert-text", emit_text)
					object.connect("icon-press", revert_option, type, group, setting)
					object.connect("changed", set_option, type, None, group, setting)
				elif type == "int":
					object.connect("value-changed", set_option, type, None, group, setting)
					object.connect("icon-press", revert_option, type, group, setting)
				elif type == "bool":
					object.connect("toggled", set_option, type, None, group, setting)
				elif type == "combo":
					object.connect("changed", set_option, type, dict, group, setting)

			def revert_option(widget, pos, event, type, widget_group, widget_setting):
				if type == "text" or type == "int":
					if pos == Gtk.EntryIconPosition.SECONDARY:
						opt = self.factorydefault["%s" % widget_group]["%s" % widget_setting]
					else:
						opt = self.userdefault["%s" % widget_group]["%s" % widget_setting]
					self.config["%s" % widget_group]["%s" % widget_setting] = opt
					if type == "text":
						widget.set_text("%s" % self.config["%s" % widget_group]["%s" % widget_setting])
					elif type == "int":
						widget.set_value(self.config["%s" % widget_group].as_int("%s" % widget_setting))

			def set_option(widget, type, dict, widget_group, widget_setting):
				if type == "text":
					self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_text()
				elif type == "int":
					self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_value_as_int()
				elif type == "bool":
					self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_active()
				elif type == "combo":
					self.config["%s" % widget_group]["%s" % widget_setting] =  dict[widget.get_active()]

			def emit_text(widget, text, *args):
				if text in blacklist:
					widget.emit_stop_by_name('insert-text')

			object = LoadWidget()
			LoadValue()
			ConnectSignals()

		def InitKeyWidget(self, setting):
			group = "Keybindings"
			modifier = self.config["%s" % group]["%s" % setting].split(":")[0]
			boundkey = self.config["%s" % group]["%s" % setting].split(":")[1]

			def LoadWidgets():
				object_alt = gtkbuilder.get_object("%s.alt" % setting)
				object_ctrl = gtkbuilder.get_object("%s.ctrl" % setting)
				object_entry = gtkbuilder.get_object("%s.entry" % setting)
				object_button = gtkbuilder.get_object("%s.delete" % setting)
				return object_alt, object_ctrl, object_entry, object_button

			def LoadValues():
				if modifier == "e":
					object_alt.set_active(True)
				else:
					object_ctrl.set_active(True)
				object_entry.set_text(boundkey)

			def ConnectSignals():
				object_entry.connect("insert-text", emit_text)
				object_entry.connect("changed", set_option)
				object_alt.connect("toggled", set_option)
				object_ctrl.connect("toggled", set_option)
				object_button.connect("clicked", revert_option)

			def revert_option(widget):
				old_opt = self.factorydefault["%s" % group]["%s" % setting]
				old_mod = old_opt.split(":")[0]
				old_key = old_opt.split(":")[1]
				if old_mod == "e":
					object_alt.set_active(True)
				else:
					object_ctrl.set_active(True)
				object_entry.set_text(old_key)

			def set_option(widget):
				if object_entry.get_text() != "":
					if object_alt.get_active() == True:
						new_mod = "e"
					else:
						new_mod = "C"
					self.config["%s" % group]["%s" % setting] = new_mod + ":" + object_entry.get_text()
				else:
					self.config["%s" % group]["%s" % setting] = ""

			def emit_text(widget, text, *args):
				if text in blacklist:
					widget.emit_stop_by_name('insert-text')

			object_alt, object_ctrl, object_entry, object_button = LoadWidgets()
			LoadValues()
			ConnectSignals()

