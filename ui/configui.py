# coding=utf-8
# #######################################################
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright Christopher Roy Bratušek                    #
#                                                       #
# #######################################################

MODULES = ['sys', 'os', 'widgethandler', 'subprocess',
           'config', 'lockfile', 'dicts']

FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
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

        def backup_configAction(data):
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
            versionlabel_userbackup.set_text(f"{config.UserSaveConfigVersion()}")

        def restore_configAction(data):
            config.RestoreConfig()
            lock.Remove()
            print(_("RestoreConfig: relaunching BashStyle-NG"))
            python = sys.executable
            os.execl(python, python, * sys.argv)

        def reset_configAction(data):
            config.ResetConfig(False)
            lock.Remove()
            print(_("ResetConfig: relaunching BashStyle-NG"))
            python = sys.executable
            os.execl(python, python, * sys.argv)

        def delete_configPossible():
            delete_config.set_sensitive(config.UserSaveConfigExists())

        def delete_configAction(data):
            if os.access(USER_DEFAULTS_SAVE, os.F_OK):
                print(_(f"BackupConfig: deleting user backup {USER_DEFAULTS_SAVE}"))
                os.remove(USER_DEFAULTS_SAVE)
            restore_configPossible()
            delete_configPossible()

        def openFile(data, file):
            if not os.access(file, os.F_OK):
                with open(file, 'w') as fp: pass
            subprocess.Popen(["xdg-open", f"{file}"])

        WidgetHandler = widgethandler.WidgetHandler(self.config, self.userdefault, self.factorydefault)

        WidgetHandler.InitButton("config.backup", backup_configAction)
        WidgetHandler.InitButton("config.reset", reset_configAction)
        WidgetHandler.InitButton("config.edit_bashrc", openFile, f"{os.getenv('HOME')}/.bashrc")
        WidgetHandler.InitButton("config.edit_bashstylecustom", openFile, f"{os.getenv('HOME')}/.bashstyle.custom")
        WidgetHandler.InitButton("config.edit_vimrccustom", openFile, f"{os.getenv('HOME')}/.vimrc.custom")
        WidgetHandler.InitButton("config.edit_inputrccustom", openFile, f"{os.getenv('HOME')}/.inputrc.custom")
        restore_config = WidgetHandler.InitButton("config.restore", restore_configAction)
        delete_config = WidgetHandler.InitButton("config.delete", delete_configAction)

        WidgetHandler.InitLabel("config.label_user.desc", config.UserConfigVersion())
        WidgetHandler.InitLabel("config.label_vendor.desc", config.VendorConfigVersion())
        WidgetHandler.InitLabel("config.label_factory.desc", config.FactoryConfigVersion())
        versionlabel_userbackup = WidgetHandler.InitLabel("config.label_userbackup.desc", config.UserSaveConfigVersion())

        restore_configPossible()
        delete_configPossible()

class StartupUI(object):

    def __init__(self, cfo, udc, fdc):
        self.config = cfo
        self.userdefault = udc
        self.factorydefault = fdc

    def InitStartupUI(self):

        if not config.CheckBashStyle():
            def setBashStyle(data, atad):
                config.EnableBashStyle(True)
                notebook.set_current_page(0)

            def abortBashStyle(data, atad):
                notebook.set_current_page(0)

            WidgetHandler = widgethandler.WidgetHandler(self.config, self.userdefault, self.factorydefault)
            WidgetHandler.InitWidget("startup.enable", setBashStyle, None, "button", None)
            WidgetHandler.InitWidget("startup.cancel", abortBashStyle, None, "button", None)

            notebook = gtkbuilder.get_object("notebook")
            notebook.set_current_page(13)
