#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2017 Christopher Bratusek		#
#							#
#########################################################

import gettext, os, optparse
lang = gettext.translation('bashstyle', fallback=True)
lang.install(names=['_'])

import config

cfg = config.Config()
USER_DEFAULTS_SAVE = config.USER_DEFAULTS_SAVE

class ConfigUpdateHelper(object):

	def __init__(self):

		parser = optparse.OptionParser(_("config-update-helper <option>\
				\n\nBashStyle-NG © 2007 - 2017 Christopher Bratusek\
				\nBashStyle-NG configuration update helper.\
				\nLicensed under the GNU GENERAL PUBLIC LICENSE v3"))

		parser.add_option("-u", "--update", dest="update",
				action="store_true", default=False, help=_("update user configuration and exit"))

		parser.add_option("-b", "--backup", dest="backup",
				  action="store_true", default=False, help=_("backup user configuration and exit"))

		parser.add_option("-r", "--restore", dest="restore",
				  action="store_true", default=False, help=_("restore user configuration backup and exit"))

		parser.add_option("-R", "--reset", dest="reset",
				  action="store_true", default=False, help=_("reset user configuration and exit"))

		(options, args) = parser.parse_args()

		if options.update:
			cfg.InitConfig()
			cfg.LoadConfig()
			cfg.CheckConfig()

		if options.backup:
			cfg.BackupConfig()

		if options.restore:
			cfg.ResetConfig(True)
		
		if options.reset:
			cfg.ResetConfig(False)

if __name__ == "__main__":
	ConfigUpdateHelper()
