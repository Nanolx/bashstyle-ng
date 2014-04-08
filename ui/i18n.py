#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2014 Christopher Bratusek		#
#							#
#########################################################

MODULES = [ 'locale', 'gettext' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

if FAILED:
    print("The following modules failed to import: %s" % (" ".join(FAILED)))
    sys.exit(1)

class Gettext(object):
	def SetLang(self):
		self.langs = ["C", "de", "it", "ru", "es"]
		lc, encoding = locale.getdefaultlocale()
		gettext.bindtextdomain("bs-ng")
		gettext.textdomain("bs-ng")
		self.lang = gettext.translation("bs-ng", languages=self.langs, fallback=True)
		global _
		_ = self.lang.gettext

	def GetLang(self):
		print(lc)

	def Geti18n(self):
		if lc[:2] in self.langs:
			print(lc)
		else:
			print("C")
