#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2016 Christopher Bratusek		#
#							#
#########################################################

MODULES = [ 'sys', 'os', 'widgethandler', 'subprocess', 'config', 'lockfile' ]

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
		  "bs-ng-custom",  "bs-ng-config", "bs-ng-doc",
		  "bs-ng-info" ]

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
	"bs-ng-keys" : _("Keybindings"),
	"bs-ng-config" : _("Configuration"),
        "bs-ng-doc" : _("Documentation"),
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
	_("Keybindings") : 11,
	_("BashStyle-NG StartUp") : 13,
	_("Configuration") : 14,
	_("Documentation") : 0,
}

gtkbuilder = widgethandler.gtkbuilder
USER_DEFAULTS_SAVE = config.USER_DEFAULTS_SAVE
config = config.Config()
lock = lockfile.LockFile()

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
			if model[item][1] == _("Documentation"):
				back.set_visible(0)
				openFile(False, os.getenv('BSNG_DATADIR') + "/doc/bashstyle-ng/index.html")
			else:
				notebook.set_current_page(notebook_pages[model[item][1]])
				back.set_visible(1)
				main_label.set_text(_("Category: ") + _(model[item][1]))
				if model[item][1] == _("Keybindings"):
					use_keys_button.set_visible(1)

		iconview.connect("item-activated", iconview_activated)

		def backup_configAction(data, atad):
			config.BackupConfig()
			restore_configPossible()
			delete_configPossible()

		def restore_configPossible():
			if config.UserSaveConfigExists():
				if config.UserSaveConfigVersion() == config.FactoryConfigVersion():
					restore_config.set_sensitive(True)
				else:
					restore_config.set_sensitive(False)
			else:
				restore_config.set_sensitive(False)
			versionlabel_userbackup.set_text("%s" % config.UserSaveConfigVersion())

		def restore_configAction(data, atad):
			config.RestoreConfig()
			lock.Remove()
			print(_("RestoreConfig: relaunching BashStyle-NG"))
			python = sys.executable
			os.execl(python, python, * sys.argv)

		def reset_configAction(data, atad):
			config.ResetConfig(False)
			lock.Remove()
			print(_("ResetConfig: relaunching BashStyle-NG"))
			python = sys.executable
			os.execl(python, python, * sys.argv)

		def delete_configPossible():
			delete_config.set_sensitive(config.UserSaveConfigExists())

		def delete_configAction(data, atad):
			if os.access(USER_DEFAULTS_SAVE, os.F_OK):
				print(_("BackupConfig: deleting user backup %s" % USER_DEFAULTS_SAVE))
				os.remove(USER_DEFAULTS_SAVE)
			restore_configPossible()
			delete_configPossible()

		def openFile(data, file):
			subprocess.Popen(["xdg-open", "%s" %file])

		def load_button(widget, action, extraarg=None):
			widget = gtkbuilder.get_object("%s" % widget)
			widget.connect("clicked", action, extraarg)
			return widget

		load_button("config.backup", backup_configAction)
		load_button("config.reset", reset_configAction)
		load_button("config.edit_bashrc", openFile, os.getenv('HOME') + "/.bashrc")
		load_button("config.edit_bashstylecustom", openFile, os.getenv('HOME') + "/.bashstyle.custom")
		load_button("config.edit_vimrccustom", openFile, os.getenv('HOME') + "/.vimrc.custom")
		load_button("config.edit_inputrccustom", openFile, os.getenv('HOME') + "/.inputrc.custom")
		restore_config = load_button("config.restore", restore_configAction)
		delete_config = load_button("config.delete", delete_configAction)

		def load_label(widget, action):
			widget = gtkbuilder.get_object("%s" % widget)
			widget.set_text("%s" % action)
			return widget

		load_label("config.label_user.desc", config.UserConfigVersion())
		load_label("config.label_vendor.desc", config.VendorConfigVersion())
		load_label("config.label_factory.desc", config.FactoryConfigVersion())
		versionlabel_userbackup = load_label("config.label_userbackup.desc", config.UserSaveConfigVersion())

		restore_configPossible()
		delete_configPossible()

		if config.CheckBashStyle() == False:
			def setBashStyle(data, atad):
				config.EnableBashStyle(True)
				notebook.set_current_page(0)
				main_label.set_text(_("Choose a Category:"))

			def abortBashStyle(data, atad):
				notebook.set_current_page(0)
				main_label.set_text(_("Choose a Category:"))

			load_button("startup.enable", setBashStyle)
			load_button("startup.cancel", abortBashStyle)

			notebook.set_current_page(13)
			main_label.set_text(_("Category: ") + _("BashStyle-NG StartUp"))
