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

MODULES = [ 'os', 'sys', 'optparse' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

class CmdArgs(object):
	parser = optparse.OptionParser("bashstyle <option>\
					\n\nBashStyle-NG © 2007 - 2015 Christopher Bratusek\
					\nLicensed under the GNU GENERAL PUBLIC LICENSE v3")

	parser.add_option("-v", "--version", dest="version",
			  action="store_true", default=False, help="print version and exit")

	parser.add_option("-p", "--prefix", dest="prefix",
			  action="store_true", default=False, help="print prefix and exit")

	(options, args) = parser.parse_args()

	if options.version:
		print("%s" % os.getenv('BSNG_UI_VERSION'))
		sys.exit(0)

	if options.prefix:
		print("%s" % os.getenv('BSNG_UI_PREFIX'))
		sys.exit(0)
