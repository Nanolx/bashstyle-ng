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

MODULES = [ 'os', 'os.path', 'sys', 'configobj', 'shutil' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

DATADIR = os.getenv('BSNG_DATADIR')
USER_DEFAULTS = (os.getenv('HOME') + '/.bs-ng.ini')
USER_DEFAULTS_NEW = (os.getenv('HOME') + '/.bs-ng.ini.new')
USER_DEFAULTS_SAVE = (os.getenv('HOME') + '/.bs-ng.ini.save')
FACTORY_DEFAULTS = (DATADIR + '/bashstyle-ng/bs-ng.ini')
VENDOR_DEFAULTS = ('/etc/bs-ng_vendor.ini')

app_ini_version = 18

class Config(object):
	def InitConfig(self):
		if not os.access(USER_DEFAULTS, os.F_OK):
			RestoreConfig()

	def LoadConfig(self):
		self.cfo = configobj.ConfigObj(infile=USER_DEFAULTS,default_encoding="utf8")
		if os.access('/etc/bs-ng_vendor.ini', os.F_OK):
			vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS,default_encoding="utf8")
			if vendor_ini.as_int("ini_version") == app_ini_version:
				print(_("LoadConfig: vendor configuration up-to-date, using it's values."))
				self.fdc = configobj.ConfigObj(infile=VENDOR_DEFAULTS,default_encoding="utf8")
			else:
				print(_("LoadConfig: vendor configuration oudated, using factory defaults!"))
				self.fdc = configobj.ConfigObj(infile=FACTORY_DEFAULTS,default_encoding="utf8")
		else:
			print(_("LoadConfig: no vendor configuration found, using factory defaults."))
			self.fdc = configobj.ConfigObj(infile=FACTORY_DEFAULTS,default_encoding="utf8")
		self.udc = configobj.ConfigObj(infile=USER_DEFAULTS,default_encoding="utf8")

	def ReloadConfig(self):
		self.cfo.reload()
		self.udc.reload()
		self.fdc.reload()

	def CheckConfig(self):
		try:
			if self.cfo.as_int("ini_version") < app_ini_version:
				print(_("CheckConfig: User ini is at version {}, but {} is available, updating.").format(self.cfo.as_int("ini_version"), app_ini_version))
				self.UpdateConfig()
			elif self.cfo.as_int("ini_version") > app_ini_version:
				print(_("CheckConfig: User ini version is at {}, but {} is the highest known. Resetting due to error.").format(self.cfo.as_int("ini_version"), app_ini_version))
				self.ResetConfig()
			else:
				print(_("CheckConfig: User configuration up-to-date."))
			self.FixUpConfig()
		except KeyError:
			print(_("CheckConfig: something is wrong with User configuration, restoring defaults."))
			ResetConfig()

	def ResetConfig(self):
		if os.access('/etc/bs-ng_vendor.ini', os.F_OK):
			vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS,default_encoding="utf8")
			if vendor_ini.as_int("ini_version") == app_ini_version:
				print(_("ResetConfig: vendor configuration up-to-date, using it's values."))
				shutil.copy(VENDOR_DEFAULTS, USER_DEFAULTS)
			else:
				print(_("ResetConfig: vendor configuration oudated, using factory defaults!"))
				shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS)
		else:
			print(_("ResetConfig: no vendor configuration found, using factory defaults."))
			shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS)

	def BackupConfig(self):
		print(_("BackupConfig: backing up configuration to %s." % USER_DEFAULTS_SAVE))
		shutil.copy(USER_DEFAULTS, USER_DEFAULTS_SAVE)

	def RestoreConfig(self):
		print(_("RestoreConfig: restoring configuration from %s" % USER_DEFAULTS_SAVE))
		shutil.copy(USER_DEFAULTS_SAVE, USER_DEFAULTS)

	def UpdateConfig(self):
		if os.access('/etc/bs-ng_vendor.ini', os.F_OK):
			vendor_ini = configobj.ConfigObj(infile=VENDOR_DEFAULTS,default_encoding="utf8")
			if vendor_ini.as_int("ini_version") == app_ini_version:
				print(_("UpdateConfig: vendor configuration up-to-date, copying as user-default."))
				shutil.copy(VENDOR_DEFAULTS, USER_DEFAULTS_NEW)
			else:
				print(_("UpdateConfig: vendor configuration outdated, using factory defaults instead!"))
				shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS_NEW)
		else:
			print(_("UpdateConfig: no vendor configuration found, using factory defaults instead."))
			shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS_NEW)
		new = configobj.ConfigObj(infile=USER_DEFAULTS_NEW,default_encoding="utf8")
		old = configobj.ConfigObj(infile=USER_DEFAULTS,default_encoding="utf8")
		print(_("UpdateConfig: merging values."))
		new.merge(old)
		new["ini_version"] = app_ini_version
		new.write()
		shutil.move(USER_DEFAULTS_NEW, USER_DEFAULTS)
		self.cfo.reload()

	def WriteConfig(self):
		print(_("WriteConfig: saving configuration."))
		self.cfo.write()

	def FixUpConfig(self):
		print(_("FixUpConfig: checking for outdated values."))
		if self.cfo["Style"]["prompt_style"] == "clock-ad":
			print(_("FixUpConfig: updating prompt_style for name change clock-ad >> equinox."))
			self.SetUserConfig("Style", "prompt_style", "equinox")

	def GetUserConfig(self, group, setting):
		print(self.cfo["%s" % group]["%s" % setting])

	def SetUserConfig(self, group, setting, value):
		self.cfo["%s" % group]["%s" % setting] = value

	def SetUserConfigFromOld(self, group, setting):
		self.cfo["%s" % group]["%s" % setting] = self.udc["%s" % group]["%s" % setting]

	def SetUserConfigFromFactory(self, group, setting):
		self.cfo["%s" % group]["%s" % setting] = self.fdc["%s" % group]["%s" % setting]

	def GetUserOldConfig(self, group, setting):
		print(self.udc["%s" % group]["%s" % setting])

	def GetFactoryConfig(self, group, setting):
		print(self.fdc["%s" % group]["%s" % setting])
