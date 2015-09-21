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

MODULES = [ 'sys', 'widgethandler', 'subprocess' ]

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
	from gi.repository.GdkPixbuf import Pixbuf
except ImportError:
	FAILED.append(_("GdkPixbuf (from gi.repository)"))

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

iconview_icons = ["bs-ng-style", "bs-ng-alias", "bs-ng-advanced",
		  "bs-ng-shopts", "bs-ng-git", "bs-ng-readline",
		  "bs-ng-vim", "bs-ng-nano", "bs-ng-ls", "bs-ng-keys",
		  "bs-ng-custom", "bs-ng-info" ]

iconview_labels = {
	"bs-ng-style" : _("General Style"),
	"bs-ng-alias" : _("Aliases"),
	"bs-ng-advanced" : _("Advanced"),
	"bs-ng-readline" : _("Readline"),
	"bs-ng-vim" : _("Vi IMproved"),
	"bs-ng-nano" : _("GNU Nano"),
	"bs-ng-ls" : _("LS colors"),
	"bs-ng-custom" : _("Custom Prompt Builder"),
	"bs-ng-shopts" : _("Shell Options"),
	"bs-ng-git" : _("GIT"),
	"bs-ng-info" : _("About BashStyle-NG"),
	"bs-ng-keys" : _("Keybindings")
}

notebook_pages = {

	_("General Style") : 1,
	_("Aliases") : 2,
	_("Advanced") : 3,
	_("Readline") : 4,
	_("Vi IMproved") : 5,
	_("GNU Nano") : 6,
	_("LS colors") : 7,
	_("Custom Prompt Builder") : 8,
	_("Shell Options") : 10,
	_("GIT") : 9,
	_("About BashStyle-NG") : 12,
	_("Keybindings") : 11
}

gtkbuilder = widgethandler.gtkbuilder

class IconBook(object):

	def InitIconBook(self):

		liststore = gtkbuilder.get_object("iconviewstore")
		iconview = gtkbuilder.get_object("iconview")
		iconview.set_model(liststore)
		iconview.set_pixbuf_column(0)
		iconview.set_text_column(1)
		iconview.set_activate_on_single_click(True)

		notebook = gtkbuilder.get_object("notebook")
		notebook.set_current_page(0)
		notebook.set_show_tabs(False)

		main_label = gtkbuilder.get_object("main.label")

		use_keys_button = gtkbuilder.get_object("use_keybindingscfg")
		use_keys_button.set_visible(0)

		def back_clicked(data):
			notebook.set_current_page(0)
			use_keys_button.set_visible(0)
			back.set_visible(0)
			main_label.set_text(_("Choose a Category:"))

		back = gtkbuilder.get_object("back")
		back.connect("clicked", back_clicked)
		back.set_visible(0)

		for icon in iconview_icons:
			pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
			liststore.append([pixbuf, iconview_labels[icon]])

		def iconview_activated(widget, item):
			model = widget.get_model()
			notebook.set_current_page(notebook_pages[model[item][1]])
			back.set_visible(1)
			main_label.set_text(_("Category: ") + _(model[item][1]))
			if model[item][1] == _("Keybindings"):
				use_keys_button.set_visible(1)

		iconview.connect("item-activated", iconview_activated)
