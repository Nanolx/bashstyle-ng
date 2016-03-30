#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2016 Christopher Bratusek		#
#							#
#########################################################

import gettext, os
lang = gettext.translation('bashstyle', fallback=True)
lang.install(names=['_'])

import config

print (_("BashStyle-NG configuration update helper."))

cfg = config.Config()

cfg.InitConfig()
cfg.LoadConfig()
cfg.CheckConfig()
cfg.WriteConfig()
