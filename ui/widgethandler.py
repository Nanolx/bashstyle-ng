#!/usr/bin/env bashstyle --python
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

MODULES = [ 'os', 'misc' ]

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

PREFIX = os.getenv('BSNG_UI_PREFIX') or "/usr"
blacklist = ['\'', '\"']
gtkbuilder = Gtk.Builder()
gtkbuilder.set_translation_domain("bs-ng")
gtkbuilder.add_from_file(PREFIX + "/share/bashstyle-ng/ui/bashstyle8.ui")

class WidgetHandler(object):
		####################### metafuncs for handling widgets ###########################
		def __init__(self, cfo, udc, fdc):
			self.config = cfo
			self.userdefault = udc
			self.factorydefault = fdc

		def InitWidget(self, widget, group, setting, type, dict):

			def LoadWidget(widget):
				object = gtkbuilder.get_object("%s" % widget)
				return object

			def LoadValue(object, group, setting, type):
				if type == "text":
					object.set_text("%s" % self.config["%s" % group]["%s" % setting])
				elif type == "int":
					object.set_value(self.config["%s" % group].as_int("%s" % setting))
				elif type == "bool":
					object.set_active(self.config["%s" % group].as_bool("%s" % setting))
				elif type == "combo":
					object.set_active(misc.SwapDictionary(dict)[self.config["%s" % group]["%s" % setting]])

			def ConnectSignals(object, type, widget_group, widget_setting):
				if type == "text":
					object.connect("insert-text", emit_text)
					object.connect("icon-press", revert_option, type, widget_group, widget_setting)
					object.connect("changed", set_option, type, None, widget_group, widget_setting)
				elif type == "int":
					object.connect("value-changed", set_option, type, None, widget_group, widget_setting)
					object.connect("icon-press", revert_option, type, widget_group, widget_setting)
				elif type == "bool":
					object.connect("toggled", set_option, type, None, widget_group, widget_setting)
				elif type == "combo":
					object.connect("changed", set_option, type, dict, widget_group, widget_setting)

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
					if widget_setting == "use_bashstyle":
						misc.EnableBashstyleNG(widget.get_active())
				elif type == "combo":
					self.config["%s" % widget_group]["%s" % widget_setting] =  dict[widget.get_active()]

			def emit_text(widget, text, *args):
				if text in blacklist:
					widget.emit_stop_by_name('insert-text')
			
			object = LoadWidget(widget)
			LoadValue(object, group, setting, type)
			ConnectSignals(object, type, group, setting)
