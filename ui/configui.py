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

MODULES = [ 'sys', 'os', 'widgethandler', 'subprocess',
            'config', 'lockfile', 'dicts' ]

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

gtkbuilder = widgethandler.gtkbuilder
USER_DEFAULTS_SAVE = config.USER_DEFAULTS_SAVE
config = config.Config()
lock = lockfile.LockFile()

class ConfigUI(object):

	def __init__(self, cfo, udc, fdc):
			self.config = cfo
			self.userdefault = udc
			self.factorydefault = fdc

	def InitConfigUI(self):

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

		WidgetHandler = widgethandler.WidgetHandler(self.config, self.userdefault, self.factorydefault)
		WidgetHandler.InitWidget("config.backup", backup_configAction, None, "button", None)
		WidgetHandler.InitWidget("config.reset", reset_configAction, None, "button", None)
		WidgetHandler.InitWidget("config.edit_bashrc", openFile, os.getenv('HOME') + "/.bashrc", "button", None)
		WidgetHandler.InitWidget("config.edit_bashstylecustom", openFile, os.getenv('HOME') + "/.bashstyle.custom", "button", None)
		WidgetHandler.InitWidget("config.edit_vimrccustom", openFile, os.getenv('HOME') + "/.vimrc.custom", "button", None)
		WidgetHandler.InitWidget("config.edit_inputrccustom", openFile, os.getenv('HOME') + "/.inputrc.custom", "button", None)
		WidgetHandler.InitWidget("config.label_user.desc", None, config.UserConfigVersion(), "label", None)
		WidgetHandler.InitWidget("config.label_vendor.desc", None, config.VendorConfigVersion(), "label", None)
		WidgetHandler.InitWidget("config.label_factory.desc", None, config.FactoryConfigVersion(), "label", None)
		WidgetHandler.InitWidget("about.prefix", None, os.getenv('BSNG_UI_PREFIX'), "label", None)
		WidgetHandler.InitWidget("about.version", None, os.getenv('BSNG_UI_VERSION'), "label", None)

		# widgets stored for later re-usage
		restore_config = WidgetHandler.InitWidget("config.restore", restore_configAction, None, "button", None)
		delete_config = WidgetHandler.InitWidget("config.delete", delete_configAction, None, "button", None)
		versionlabel_userbackup = WidgetHandler.InitWidget("config.label_userbackup.desc", None, config.UserSaveConfigVersion(), "label", None)

		restore_configPossible()
		delete_configPossible()

class StartupUI(object):

	def __init__(self, cfo, udc, fdc):
			self.config = cfo
			self.userdefault = udc
			self.factorydefault = fdc

	def InitStartupUI(self):

		if config.CheckBashStyle() == False:
			def setBashStyle(data, atad):
				config.EnableBashStyle(True)
				notebook.set_current_page(0)
				main_label.set_text(_("Choose a Category:"))

			def abortBashStyle(data, atad):
				notebook.set_current_page(0)
				main_label.set_text(_("Choose a Category:"))

			WidgetHandler = widgethandler.WidgetHandler(self.config, self.userdefault, self.factorydefault)
			WidgetHandler.InitWidget("startup.enable", setBashStyle, None, "button", None)
			WidgetHandler.InitWidget("startup.cancel", abortBashStyle, None, "button", None)

			notebook = gtkbuilder.get_object("notebook")
			notebook.set_current_page(13)

			main_label = gtkbuilder.get_object("main.label")
			main_label.set_text(_("Category: ") + _("BashStyle-NG StartUp"))
