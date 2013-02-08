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

MODULES = [ 'os', 'os.path', 'configobj', 'string', 'shutil' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

if FAILED:
    print "The following modules failed to import: %s" % (" ".join(FAILED))
    sys.exit(1)

PREFIX = os.getenv('BSNG_UI_PREFIX') or "/usr"
USER_DEFAULTS = (os.getenv('HOME') + '/.bs-ng.ini')
USER_DEFAULTS_NEW = (os.getenv('HOME') + '/.bs-ng.ini.new')
USER_DEFAULTS_SAVE = (os.getenv('HOME') + '/.bs-ng.ini.save')
FACTORY_DEFAULTS = (PREFIX + '/share/bashstyle-ng/bs-ng.ini')

app_ini_version = 2

class Config(object):
	def InitConfig(self):
		if not os.access(USER_DEFAULTS, os.F_OK):
			shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS)

	def LoadConfig(self):
		self.cfo = configobj.ConfigObj(USER_DEFAULTS)
		self.fdc = configobj.ConfigObj(FACTORY_DEFAULTS)
		self.udc = configobj.ConfigObj(USER_DEFAULTS)

	def ReloadConfig(self):
		self.cfo.reload()
		self.udc.reload()
		self.fdc.reload()

	def UpdateConfig(self):
		if self.cfo.as_int("ini_version") < app_ini_version:
			shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS_NEW)
			new = configobj.ConfigObj(USER_DEFAULTS_NEW)
			old = configobj.ConfigObj(USER_DEFAULTS)
			new.merge(old)
			new["ini_version"] = app_ini_version
			new.write()
			shutil.move(USER_DEFAULTS_NEW, USER_DEFAULTS)

	def ResetConfig(self):
		shutil.copy(FACTORY_DEFAULTS, USER_DEFAULTS)

	def BackupConfig(self):
		shutil.copy(USER_DEFAULTS, USER_DEFAULTS_SAVE)

	def RestoreConfig(self):
		shutil.copy(USER_DEFAULTS_SAVE, USER_DEFAULTS)

	def WriteConfig(self):
		self.cfo.write()

	def GetUserConfig(self, group, setting):
		print self.cfo["%s" % group]["%s" % setting]

	def SetUserConfig(self, group, setting, value):
		self.cfo["%s" % group]["%s" % setting] = value

	def SetUserConfigFromOld(self, group, setting):
		self.cfo["%s" % group]["%s" % setting] = self.udc["%s" % group]["%s" % setting]

	def SetUserConfigFromFactory(self, group, setting):
		self.cfo["%s" % group]["%s" % setting] = self.fdc["%s" % group]["%s" % setting]

	def GetUserOldConfig(self, group, setting):
		print self.udc["%s" % group]["%s" % setting]

	def GetFactoryConfig(self, group, setting):
		print self.fdc["%s" % group]["%s" % setting]