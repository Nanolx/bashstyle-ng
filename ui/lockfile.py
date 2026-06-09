# coding=utf-8
# ##################################################### #
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright Christopher Roy Bratušek                    #
#                                                       #
# ##################################################### #

MODULES = ['os', 'os.path', 'sys', 'subprocess']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

lockfile = os.path.expanduser("~/.bashstyle.lock")

class LockFile(object):
    def Check(self):
        if os.access(lockfile, os.F_OK):
            with open(lockfile, "r") as rlockfile:
                rlockfile.seek(0)
                oldpid = rlockfile.readline().strip()

            if os.path.exists(f"/proc/{oldpid}"):
                xpid = subprocess.getoutput("pgrep -l bashstyle")
                gpid = xpid.split()

                if len(gpid) > 1 and gpid[1] == "bashstyle":
                    print(
                        _(f"Lockfile does exist and bashstyle-ng is already running.\n\nbashstyle-ng is running as process {oldpid}")
                    )
                    sys.exit(1)
                else:
                    print(
                        _(f"Lockfile does exist but the process with that pid is not\n\nbashstyle, removing lockfile of old process: {oldpid}")
                    )
                    os.remove(lockfile)
            else:
                print(
                    _(f"Lockfile does exist but the process with that pid is no\n\nlonger running, removing lockfile of old process: {oldpid}")
                )
                os.remove(lockfile)
        else:
            print(_("Lockfile does not exist"))

    def Write(self):
        if not os.access(lockfile, os.F_OK):
            # Nutzt 'with', damit die Datei auch bei Fehlern sicher geschlossen wird
            with open(lockfile, "w") as wlockfile:
                wlockfile.write(f"{os.getpid()}")

    def Remove(self):
        if os.access(lockfile, os.F_OK):
            os.remove(lockfile)
