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

MODULES = [ 'sys', 'widgethandler' ]

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

try:
	from gi.repository import GObject
except ImportError:
	FAILED.append(_("GObject (from gi.repository)"))

try:
	from gi.repository.GdkPixbuf import Pixbuf
except ImportError:
	FAILED.append(_("GdkPixbuf (from gi.repository)"))

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

gtkbuilder = widgethandler.gtkbuilder

keybindings = {
	"undo",
	"upcase_word",
	"capitalize_word",
	"downcase_word",
	"transpose_words",
	"transpose_chars",
	"unix_word_rubout",
	"kill_word",
	"possible_filename_completions",
	"possible_hostname_completions",
	"possible_username_completions",
	"possible_variable_completions",
	"kill_line",
	"unix_line_discard",
	"beginning_of_line",
	"end_of_line",
	"clear_screen",
	"history_search_forward",
	"history_search_backward",
	"complete_path",
	"alias_expand_line",
	"backward_char",
	"backward_delete_char",
	"delete_char",
	"forward_char",
	"backward_word",
	"forward_word",
	"overwrite_mode",
	"menu_complete"
}

class CellRendererClickablePixbuf(Gtk.CellRendererPixbuf):
	__gsignals__ = {
		'clicked': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
		(GObject.TYPE_STRING,))
	}

	def __init__(self):
		Gtk.CellRendererPixbuf.__init__(self)
		self.set_property('mode', Gtk.CellRendererMode(1))

	def do_activate(self, event, widget, path, background_area, cell_area, flags):
		if (event
			and cell_area.x <= event.x <= cell_area.x + cell_area.width
			and cell_area.y <= event.y <= cell_area.y + cell_area.height):
			self.emit('clicked', path)

GObject.type_register(CellRendererClickablePixbuf)

class KeyTree(object):

	def __init__(self, cfo, udc, fdc):
			self.config = cfo
			self.userdefault = udc
			self.factorydefault = fdc

	def InitTree(self):
		use_keys = gtkbuilder.get_object("use_keybindingscfg")
		store = gtkbuilder.get_object("treeviewstore")
		tree = gtkbuilder.get_object("keybindings.treeview")

		render_binding = Gtk.CellRendererText()
		column_binding = Gtk.TreeViewColumn(_("Binding"), render_binding, text=0)
		tree.append_column(column_binding)

		render_revert_user = CellRendererClickablePixbuf()
		render_revert_user.set_property("icon-name", "gtk-revert-to-saved")
		column_revert_user = Gtk.TreeViewColumn(_("Revert"), render_revert_user, icon_name=1)
		tree.append_column(column_revert_user)

		render_revert_factory = CellRendererClickablePixbuf()
		render_revert_factory.set_property("icon-name", "gtk-delete")
		column_revert_factory = Gtk.TreeViewColumn(_("Default"), render_revert_factory, icon_name=2)
		tree.append_column(column_revert_factory)

		render_alt = Gtk.CellRendererToggle()
		render_alt.set_property("radio", True)
		column_alt = Gtk.TreeViewColumn(_("Alt"), render_alt, active=3)
		tree.append_column(column_alt)

		render_ctrl = Gtk.CellRendererToggle()
		render_ctrl.set_property("radio", True)
		column_ctrl = Gtk.TreeViewColumn(_("Ctrl"), render_ctrl, active=4)
		tree.append_column(column_ctrl)

		render_nmod = Gtk.CellRendererToggle()
		render_nmod.set_property("radio", True)
		column_nmod = Gtk.TreeViewColumn(_("None"), render_nmod, active=5)
		tree.append_column(column_nmod)

		def on_cell_toggled(widget, path, alt, ctrl, nmod):
			store[path][3] = alt
			store[path][4] = ctrl
			store[path][5] = nmod

		render_alt.connect("toggled", on_cell_toggled, True, False, False)
		render_ctrl.connect("toggled", on_cell_toggled, False, True, False)
		render_nmod.connect("toggled", on_cell_toggled, False, False, True)

		render_key = Gtk.CellRendererText()
		render_key.set_property("editable", True)
		column_key = Gtk.TreeViewColumn(_("Key"), render_key, text=6)
		tree.append_column(column_key)

		def text_edited(widget, path, text):
			store[path][6] = text
			if text == "":
				on_cell_toggled(widget, path, False, False, False)
			else:
				self.change_setting(store[path][0].replace("-", "_"), store[path][3],
					store[path][4], store[path][5], store[path][6])

		render_key.connect("edited", text_edited)

		def on_changed(selection):
			(model, iter) = selection.get_selected()
			self.change_setting(model[iter][0].replace("-", "_"), model[iter][3],
					model[iter][4], model[iter][5], model[iter][6])

		tree.get_selection().connect("changed", on_changed)

		use_keys.set_active(self.config["Keybindings"].as_bool("use_keybindingscfg"))
		tree.set_sensitive(use_keys.get_active())

		def on_use_keys(widget):
			self.config["Keybindings"]["use_keybindingscfg"] = widget.get_active()
			tree.set_sensitive(widget.get_active())

		use_keys.connect("toggled", on_use_keys)

		def on_reset(widget, path, config):
			sel = tree.get_selection()
			(model, iter) = sel.get_selected()
			setting = model[iter][0].replace("-", "_")
			if config == "user":
				self.config["Keybindings"][setting] = self.userdefault["Keybindings"][setting]
			else:
				self.config["Keybindings"][setting] = self.factorydefault["Keybindings"][setting]
			if self.config["Keybindings"][setting] == "":
				alt = False
				ctrl = False
				nmod = False
				boundkey = ""
			else:
				modifier = self.config["Keybindings"][setting].split(":")[0]
				if modifier == "e":
					alt = True
					ctrl = False
					nmod = False
				elif modifier == "C":
					alt = False
					ctrl = True
					nmod = False
				elif modifier == "X":
					alt = False
					ctrl = False
					nmod = True
				boundkey = self.config["Keybindings"][setting].split(":")[1]
			model[iter][3] = alt
			model[iter][4] = ctrl
			model[iter][5] = nmod
			model[iter][6] = boundkey

		render_revert_user.connect("clicked", on_reset, "user")
		render_revert_factory.connect("clicked", on_reset, "factory")

		self.populate(keybindings, store)

	def prepare(self, setting):
		value = self.config["Keybindings"][setting]
		if value == "":
			modifier = ""
			boundkey = ""
		else:
			modifier = value.split(":")[0]
			boundkey = value.split(":")[1]
		label = setting.replace("_", "-")
		return modifier, boundkey, label

	def populate(self, settings, store):
		for key in sorted(settings):
			modifier, boundkey, label = self.prepare(key)
			if modifier == "e":
				alt = True
				ctrl = False
				nmod = False
			elif modifier == "C":
				alt = False
				ctrl = True
				nmod = False
			elif modifier == "X":
				alt = False
				ctrl = False
				nmod = True
			else:
				alt = False
				ctrl = False
				nmod = False
			store.append([label, "gtk-revert-to-saved", "gtk-delete", alt, ctrl, nmod, boundkey])

	def change_setting(self, setting, alt, ctrl, nmod, key):
		if key == "":
			self.config["Keybindings"][setting] = ""
		else:
			if alt == True:
				self.config["Keybindings"][setting] = "e:" + key
			elif ctrl == True:
				self.config["Keybindings"][setting] = "C:" + key
			elif nmod == True:
				self.config["Keybindings"][setting] = "X:" + key
			else:
				self.config["Keybindings"][setting] = ""
