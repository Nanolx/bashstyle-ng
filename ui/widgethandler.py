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

try:
	from gi.repository import Granite
except ImportError:
	FAILED.append("Granite (from gi.repository)")

if FAILED:
    print("The following modules failed to import: %s" % (" ".join(FAILED)))
    sys.exit(1)

PREFIX = os.getenv('BSNG_UI_PREFIX')
DATADIR = os.getenv('BSNG_DATADIR')
blacklist = ['\'', '\"']
blacklist_key = ['\'' '\"', ':' ]
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
				if type == "key":
					object = Granite.WidgetsModeButton()
				else:
					object = gtkbuilder.get_object("%s" % widget)
				return object

			def PrepareKeyWidget():
				label = gtkbuilder.get_object("%s.label" % setting)
				object.append_text("Alt")
				object.append_text("Ctrl")
				grid = gtkbuilder.get_object("keybindings.table")
				grid.attach_next_to(object, label, Gtk.PositionType.RIGHT, 1, 1)
				object.set_visible(True)

			def LoadValue():
				if type == "text":
					object.set_text("%s" % self.config["%s" % group]["%s" % setting])
				elif type == "int":
					object.set_value(self.config["%s" % group].as_int("%s" % setting))
				elif type == "bool":
					object.set_active(self.config["%s" % group].as_bool("%s" % setting))
				elif type == "combo":
					object.set_active(misc.SwapDictionary(dict)[self.config["%s" % group]["%s" % setting]])
				elif type == "key":
					if self.config["%s" % group]["%s" % setting] != "":
						modifier = self.config["%s" % group]["%s" % setting].split(":")[0]
						boundkey = self.config["%s" % group]["%s" % setting].split(":")[1]
					else:
						modifier = ""
						boundkey = ""
					if modifier == "e":
						object.set_selected(0)
					elif modifier == "C":
						object.set_selected(1)
					else:
						object.set_selected(-1)
					gtkbuilder.get_object("%s.entry" % setting).set_text(boundkey)

			def ConnectSignals():
				if type == "text":
					object.connect("insert-text", emit_text)
					object.connect("icon-press", revert_option, type, group, setting)
					object.connect("changed", set_option, None, type, None, group, setting)
				elif type == "int":
					object.connect("value-changed", set_option, None, type, None, group, setting)
					object.connect("icon-press", revert_option, type, group, setting)
				elif type == "bool":
					object.connect("toggled", set_option, None, type, None, group, setting)
				elif type == "combo":
					object.connect("changed", set_option, None, type, dict, group, setting)
				elif type == "key":
					object.connect("mode-changed", set_option, type, None, group, setting)
					gtkbuilder.get_object("%s.entry" % setting).connect("insert-text", emit_keytext)
					gtkbuilder.get_object("%s.entry" % setting).connect("changed", set_option, None, type, None, group, setting)
					gtkbuilder.get_object("%s.entry" % setting).connect("icon-press", revert_option, type, group, setting)

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
				elif type == "key":
					if pos == Gtk.EntryIconPosition.SECONDARY:
						opt = self.factorydefault["%s" % widget_group]["%s" % widget_setting]
					if opt != "":
						modifier = opt.split(":")[0]
						boundkey = opt.split(":")[1]
					else:
						modifier = ""
						boundkey = ""
					if modifier == "e":
						object.set_selected(0)
					elif modifier == "C":
						object.set_selected(1)
					else:
						object.set_selected(-1)
					gtkbuilder.get_object("%s.entry" % setting).set_text(boundkey)

			def set_option(widget, data, type, dict, widget_group, widget_setting):
				if type == "text":
					self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_text()
				elif type == "int":
					self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_value_as_int()
				elif type == "bool":
					self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_active()
				elif type == "combo":
					self.config["%s" % widget_group]["%s" % widget_setting] =  dict[widget.get_active()]
				elif type == "key":
					if gtkbuilder.get_object("%s.entry" % setting).get_text() != "":
						if object.get_selected() == 0:
							new_mod = "e"
						elif object.get_selected() == 1:
							new_mod = "C"
						else:
							new_mod = "C"
							print("no modifier selected, fallback to C")
						self.config["%s" % widget_group]["%s" % widget_setting] = new_mod + ":" + gtkbuilder.get_object("%s.entry" % setting).get_text()
					else:
						self.config["%s" % widget_group]["%s" % widget_setting] = ""

			def emit_text(widget, text, *args):
				if text in blacklist:
					widget.emit_stop_by_name('insert-text')

			def emit_keytext(widget, text, *args):
				if text in blacklist_key:
					widget.emit_stop_by_name('insert-text')

			object = LoadWidget()
			if type == "key":
				PrepareKeyWidget()
			LoadValue()
			ConnectSignals()
