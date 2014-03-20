#!/usr/bin/env bashstyle --python
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

MODULES = [ 'os', 'os.path', 'string', 'shutil', 'subprocess', 'sys' ]

FAILED = []

for module in MODULES:
	try:
		globals()[module] = __import__(module)
	except ImportError:
		FAILED.append(module)

if FAILED:
    print("The following modules failed to import: %s" % (" ".join(FAILED)))
    sys.exit(1)

lockfile = os.path.expanduser("~/.bashstyle.lock")

class LockFile(object):
	def Check(self):
		if os.access(lockfile, os.F_OK):
			rlockfile = open(lockfile, "r")
			rlockfile.seek(0)
			oldpid = rlockfile.readline()
			if os.path.exists("/proc/%s" % oldpid):
				xpid = subprocess.getoutput("pgrep -l bashstyle")
				gpid = string.split(xpid)
				if not xpid == "" and gpid[1] == "bashstyle":
					print("Lockfile does exist and bashstyle-ng is already running.")
					print("bashstyle-ng is running as process %s" % oldpid)
					sys.exit(1)
				else:
					print("Lockfile does exist but the process with that pid is not")
					print("bashstyle-ng, removing lockfile of old process: %s" % oldpid)
					os.remove(lockfile)
			else:
				print("Lockfile does exist but the process with that pid is no")
				print("longer running, removing lockfile of old process: %s" % oldpid)
				os.remove(lockfile)
		else:
			print("Lockfile does not exist")

	def Write(self):
		if not os.access(lockfile, os.F_OK):
			wlockfile = open(lockfile, "w")
			wlockfile.write("%s" % os.getpid())
			wlockfile.close

	def Remove(self):
		if os.access(lockfile, os.F_OK):
			os.remove(lockfile)
