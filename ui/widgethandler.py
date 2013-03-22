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
		def InitWidget(self, widget, group, setting, type, cfo, udc, fdc):

			def LoadWidget(widget):
				object = gtkbuilder.get_object("%s" % widget)
				return object

			def LoadValue(object, group, setting, type):
				if type == "text":
					object.set_text("%s" % cfo["%s" % group]["%s" % setting])
				elif type == "int":
					object.set_value(cfo["%s" % group].as_int("%s" % setting))
				elif type == "bool":
					object.set_active(cfo["%s" % group]["%s" % setting])

			def ConnectSignals(object, type, widget_group, widget_setting):
				if type == "text":
					object.connect("insert-text", emit_text)
					object.connect("icon-press", revert_option, type, widget_group, widget_setting)
					object.connect("changed", set_option, type, widget_group, widget_setting)
				elif type == "int":
					object.connect("value-changed", set_option, type, widget_group, widget_setting)
					object.connect("icon-press", revert_option, type, widget_group, widget_setting)
				elif type == "bool":
					object.connect("toggled", set_option, type, widget_group, widget_setting)

			def revert_option(widget, pos, event, type, widget_group, widget_setting):
				if type == "text" or type == "int":
					if pos == Gtk.EntryIconPosition.SECONDARY:
						opt = fdc["%s" % widget_group]["%s" % widget_setting]
					else:
						opt = udc["%s" % widget_group]["%s" % widget_setting]
					cfo["%s" % widget_group]["%s" % widget_setting] = opt
					if type == "text":
						widget.set_text("%s" % cfo["%s" % widget_group]["%s" % widget_setting])
					elif type == "int":
						widget.set_value(cfo["%s" % widget_group].as_int("%s" % widget_setting))

			def set_option(widget, type, widget_group, widget_setting):
				if type == "text":
					cfo["%s" % widget_group]["%s" % widget_setting] = widget.get_text()
				elif type == "int":
					cfo["%s" % widget_group]["%s" % widget_setting] = widget.get_value_as_int()
				elif type == "bool":
					cfo["%s" % widget_group]["%s" % widget_setting] = widget.get_active()
					if widget_setting == "use_bashstyle":
						misc.EnableBashstyleNG(widget.get_active())

			def emit_text(widget, text, *args):
				if text in blacklist:
					widget.emit_stop_by_name('insert-text')
			
			object = LoadWidget(widget)
			LoadValue(object, group, setting, type)
			ConnectSignals(object, type, group, setting)
