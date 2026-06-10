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

MODULES = ['os', 'os.path', 'sys', 'configobj', 'shutil']

FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

DATADIR = os.getenv('BSNG_DATADIR')

USER_DEFAULTS_TMP = f"{os.getenv('HOME')}/.bashstyle-ng.ini.new"
FACTORY_DEFAULTS = f"{DATADIR}/bashstyle-ng/bashstyle-ng.ini"
VENDOR_DEFAULTS = "/etc/bashstyle-ng_vendor.ini"

BASHSTYLERC = f"{DATADIR}/bashstyle-ng/rc/bashstyle-rc"

USER_DEFAULTS = f"{os.getenv('HOME')}/.bashstyle-ng.ini"
USER_DEFAULTS_SAVE = f"{os.getenv('HOME')}/.bashstyle-ng.ini.save"

app_ini_version = 45

class Config(object):
    def InitConfig(self):
        if not os.access(USER_DEFAULTS, os.F_OK):
            self.ResetConfig(True)

    def LoadConfig(self):
        try:
            self.cfo = configobj.ConfigObj(infile=USER_DEFAULTS, default_encoding="utf8")
        except configobj.ConfigObjError:
            print(_("LoadConfig: something is wrong with User configuration, restoring defaults."))
            self.ResetConfig(True)
            self.cfo = configobj.ConfigObj(infile=USER_DEFAULTS, default_encoding="utf8")

        self.udc = configobj.ConfigObj(infile=USER_DEFAULTS, default_encoding="utf8")
        if self.VendorConfigExists():
            vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS, default_encoding="utf8")
            if vendor_ini.as_int("ini_version") == app_ini_version:
                print(_("LoadConfig: vendor configuration up-to-date, using it's values."))
                self.fdc = configobj.ConfigObj(infile=VENDOR_DEFAULTS, default_encoding="utf8")
            else:
                print(_("LoadConfig: vendor configuration oudated, using factory defaults!"))
                self.fdc = configobj.ConfigObj(infile=FACTORY_DEFAULTS, default_encoding="utf8")
        else:
            print(_("LoadConfig: no vendor configuration found, using factory defaults."))
            self.fdc = configobj.ConfigObj(infile=FACTORY_DEFAULTS, default_encoding="utf8")

    def ReloadConfig(self):
        self.cfo.reload()
        self.udc.reload()
        self.fdc.reload()

    def CheckConfig(self):
        if self.cfo.as_int("ini_version") < app_ini_version:
            print(_("CheckConfig: User ini is at version {}, but {} is available, updating.").format(self.cfo.as_int("ini_version"), app_ini_version))
            self.UpdateConfig()
            self.cfo.reload()
        elif self.cfo.as_int("ini_version") > app_ini_version:
            print(_("CheckConfig: User ini version is at {}, but {} is the highest known. Resetting due to error.").format(self.cfo.as_int("ini_version"), app_ini_version))
            self.ResetConfig(True)
            self.cfo.reload()
        else:
            print(_("CheckConfig: User configuration up-to-date."))
        self.FixUpConfig()

    def ResetConfig(self, userbackup):
        restore_from = FACTORY_DEFAULTS
        restore_string = _("ResetConfig: reset to factory configuration.")

        if self.VendorConfigExists():
            vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS, default_encoding="utf8")
            if vendor_ini.as_int("ini_version") == app_ini_version:
                restore_from = VENDOR_DEFAULTS
                restore_string = _("ResetConfig: reset to vendor configuration.")

        if userbackup:
            if self.UserSaveConfigExists():
                backup_ini = configobj.ConfigObj(infile=USER_DEFAULTS_SAVE, default_encoding="utf8")
                if backup_ini.as_int("ini_version") == app_ini_version:
                    restore_from = USER_DEFAULTS_SAVE
                    restore_string = _("ResetConfig: reset to user backup configuration.")

        print(restore_string)
        shutil.copy(restore_from, USER_DEFAULTS)

    def BackupConfig(self):
        print(_(f"BackupConfig: backing up configuration to {USER_DEFAULTS_SAVE}."))
        shutil.copy(USER_DEFAULTS, USER_DEFAULTS_SAVE)

    def RestoreConfig(self):
        if self.UserSaveConfigExists():
            backup_ini = configobj.ConfigObj(infile=USER_DEFAULTS_SAVE, default_encoding="utf8")
            if backup_ini.as_int("ini_version") == app_ini_version:
                print(_(f"RestoreConfig: restoring configuration from {USER_DEFAULTS_SAVE}."))
                shutil.copy(USER_DEFAULTS_SAVE, USER_DEFAULTS)
            else:
                print(_("RestoreConfig: not restoring configuration as it's outdated."))
        else:
            print(_("RestoreConfig: no backup configuration exists."))

    def UpdateConfig(self):
        if os.access(VENDOR_DEFAULTS, os.F_OK):
            vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS, default_encoding="utf8")
            if vendor_ini.as_int("ini_version") == app_ini_version:
                print(_("UpdateConfig: vendor configuration up-to-date, copying as user-default."))
                shutil.copy(VENDOR_DEFAULTS, USER_DEFAULTS_TMP)
            else:
                print(_("UpdateConfig: vendor configuration outdated, using factory defaults instead!"))
                shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS_TMP)
        else:
            print(_("UpdateConfig: no vendor configuration found, using factory defaults instead."))
            shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS_TMP)
        new = configobj.ConfigObj(infile=USER_DEFAULTS_TMP, default_encoding="utf8")
        old = configobj.ConfigObj(infile=USER_DEFAULTS, default_encoding="utf8")
        print(_("UpdateConfig: merging values."))
        new.merge(old)
        new["ini_version"] = app_ini_version
        new.write()
        shutil.move(USER_DEFAULTS_TMP, USER_DEFAULTS)

    def WriteConfig(self):
        print(_("WriteConfig: saving configuration."))
        self.cfo.write()

    def FixUpConfig(self):
        print(_("FixUpConfig: checking for outdated values."))
        if self.cfo["Style"]["prompt_style"] == "clock-ad":
            print(_("FixUpConfig: updating prompt_style for name change clock-ad >> equinox."))
            self.SetUserConfig("Style", "prompt_style", "equinox")

    def GetUserConfig(self, group, setting):
        print(self.cfo[group][setting])

    def SetUserConfig(self, group, setting, value):
        self.cfo[group][setting] = value

    def SetUserConfigFromOld(self, group, setting):
        self.cfo[group][setting] = self.udc[group][setting]

    def SetUserConfigFromFactory(self, group, setting):
        self.cfo[group][setting] = self.fdc[group][setting]

    def GetUserOldConfig(self, group, setting):
        print(self.udc[group][setting])

    def GetFactoryConfig(self, group, setting):
        print(self.fdc[group][setting])

    def UserSaveConfigExists(self):
        if os.access(USER_DEFAULTS_SAVE, os.F_OK):
            try:
                backup_ini = configobj.ConfigObj(infile=USER_DEFAULTS_SAVE, default_encoding="utf8")
                return True
            except configobj.ConfigObjError:
                print(_("UserSaveConfigExists: backup configuration can't be loaded due errors."))
                return False
        else:
            return False

    def VendorConfigExists(self):
        if os.access(VENDOR_DEFAULTS, os.F_OK):
            try:
                vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS, default_encoding="utf8")
                return True
            except configobj.ConfigObjError:
                print(_("VendorConfigExists: vendor configuration can't be loaded due errors."))
                return False
        else:
            return False

    def UserConfigVersion(self):
        user_ini = configobj.ConfigObj(infile=USER_DEFAULTS, default_encoding="utf8")
        return user_ini.as_int("ini_version")

    def UserSaveConfigVersion(self):
        if self.UserSaveConfigExists():
            backup_ini = configobj.ConfigObj(infile=USER_DEFAULTS_SAVE, default_encoding="utf8")
            return backup_ini.as_int("ini_version")
        else:
            return _("None")

    def VendorConfigVersion(self):
        if self.VendorConfigExists():
            vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS, default_encoding="utf8")
            return vendor_ini.as_int("ini_version")
        else:
            return _("None")

    def FactoryConfigVersion(self):
        return app_ini_version

    def CheckBashStyle(self):
        found = False
        bashrc_path = os.path.expanduser("~/.bashrc")

        with open(bashrc_path, "r") as rc:
            content = rc.readlines()
            for line in content:
                if line.startswith(f"[[ -f {BASHSTYLERC} ]]", 0):
                    found = True
                    break
        return found

    def EnableBashStyle(self, OnOff):
        bashrc_path = os.path.expanduser("~/.bashrc")
        bashrc_new_path = os.path.expanduser("~/.bashrc.new")

        with open(bashrc_path, "r") as rc, open(bashrc_new_path, "w") as rc_new:
            content = rc.readlines()
            for line in content:
                if line.find("bashstyle-ng/rc/") == -1:
                    rc_new.write(line)

            if OnOff:
                rc_new.write(f"\n[[ -f {BASHSTYLERC} ]] && source {BASHSTYLERC}\n")

        shutil.move(bashrc_new_path, bashrc_path)
