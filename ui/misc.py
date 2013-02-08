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

MODULES = [ 'os', 'os.path', 'shutil', 'string', 'sys' ]

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

def SwapDictionary(original_dict):
	return dict([(v, k) for (k, v) in original_dict.iteritems()])

def EnableBashstyleNG(activate):
	rc = open(os.path.expanduser("~/.bashrc"), "r")
	rc_new = open(os.path.expanduser("~/.bashrc.new"), "w")
	content = rc.readlines()
	for line in content:
		if line.find("bashstyle-ng/rc/nx-rc") == -1:
			rc_new.write(line)
	rc.close
	if activate == True:
		rc_new.write("source %s/share/bashstyle-ng/rc/nx-rc" % PREFIX)
	rc_new.close
	shutil.move(os.path.expanduser("~/.bashrc.new"), os.path.expanduser("~/.bashrc"))