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

MODULES = [ 'os', 'os.path', 'sys', 'widgethandler', 'subprocess' ]

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
	from gi.repository.GdkPixbuf import Pixbuf
except ImportError:
	FAILED.append("GdkPixbuf (from gi.repository)")

if FAILED:
    print("The following modules failed to import: %s" % (" ".join(FAILED)))
    sys.exit(1)

keybindings = ["bs-ng-style", "bs-ng-separator", "bs-ng-alias",
		  "bs-ng-advanced", "bs-ng-shopts", "bs-ng-git",
		  "bs-ng-readline", "bs-ng-vim", "bs-ng-nano",
		  "bs-ng-ls", "bs-ng-keys", "bs-ng-custom",
		  "bs-ng-help", "bs-ng-info" ]

keybindings_labels = {
	"bs-ng-style" : "General Style",
	"bs-ng-alias" : "Aliases",
	"bs-ng-advanced" : "Advanced",
	"bs-ng-readline" : "Readline",
	"bs-ng-vim" : "Vi IMproved",
	"bs-ng-nano" : "GNU Nano",
	"bs-ng-ls" : "LS colors",
	"bs-ng-custom" : "Custom Prompt Builder",
	"bs-ng-separator" : "Separator Style",
	"bs-ng-shopts" : "Shell Options",
	"bs-ng-git" : "GIT",
	"bs-ng-help" : "Documentation",
	"bs-ng-info" : "About BashStyle-NG",
	"bs-ng-keys" : "Keybindings"
}

gtkbuilder = widgethandler.gtkbuilder

class Tree(object):

	def __init__(self, cfo, udc, fdc):
			self.config = cfo
			self.userdefault = udc
			self.factorydefault = fdc

	def InitTree(self):
		store = gtkbuilder.get_object("treeviewstore")
		tree = gtkbuilder.get_object("treeview")

		render_binding = Gtk.CellRendererText()
		column_binding = Gtk.TreeViewColumn("Binding", render_binding, text=0)
		tree.append_column(column_binding)

		render_alt = Gtk.CellRendererToggle()
		render_alt.set_property("radio", True)
		column_alt = Gtk.TreeViewColumn("Alt", render_alt, active=1)
		tree.append_column(column_alt)

		render_ctrl = Gtk.CellRendererToggle()
		render_ctrl.set_property("radio", True)
		column_ctrl = Gtk.TreeViewColumn("Ctrl", render_ctrl, active=2)
		tree.append_column(column_ctrl)

		def on_cell_toggled(self, widget, path, column, concurrent_column):
			store[path][column] = not store[path][column]
			store[path][concurrent_column] = not store[path][concurrent_column]

		render_ctrl.connect("toggled", on_cell_toggled, 2, 1)
		render_alt.connect("toggled", on_cell_toggled, 1, 2)

		render_key = Gtk.CellRendererText()
		render_key.set_property("editable", True)
		column_key = Gtk.TreeViewColumn("Key", render_key, text=3)
		tree.append_column(column_key)

		def text_edited(widget, path, text):
			store[path][3] = text
			print(store[path][0], store[path][1], store[path][2], store[path][3])

		render_key.connect("edited", text_edited)

		def on_changed(selection):
			(model, iter) = selection.get_selected()
			print("%s %s %s %s" %(model[iter][0],  model[iter][1], model[iter][2], model[iter][3]))
			return True

		tree.get_selection().connect("changed", on_changed)

		store.append(["unix-discard-line", False, True, "u"])
		store.append(["kill-line", True, False, "k"])
