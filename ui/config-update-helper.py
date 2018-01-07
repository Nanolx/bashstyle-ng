# coding=utf-8
# ##################################################### #
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright 2007 - 2018 Christopher Bratusek            #
#                                                       #
# ##################################################### #

MODULES = ['os', 'gettext', 'optparse', 'config']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

if FAILED:
    print(
        _("The following modules failed to import: %s")
        % (" ".join(FAILED))
    )
    sys.exit(1)

lang = gettext.translation('bashstyle', fallback=True)
lang.install(names=['_'])

cfg = config.Config()
USER_DEFAULTS_SAVE = config.USER_DEFAULTS_SAVE


class ConfigUpdateHelper(object):

    def __init__(self):

        parser = optparse.OptionParser(
            _("\n  bashstyle-config-helper <option>\
                \n\n\
        BashStyle-NG © 2007 - 2018 Christopher Bratusek\n\
        Licensed under the GNU GENERAL PUBLIC LICENSE v3")
        )

        parser.add_option(
            "-v", "--version", dest="version", action="store_true",
            default=False, help=_("print version and exit")
        )

        parser.add_option(
            "-p", "--prefix", dest="prefix", action="store_true",
            default=False, help=_("print installation prefix and exit")
        )

        parser.add_option(
            "-P", "--python", dest="python", action="store_true",
            default=False, help=_("print used Python interpreter; \
if additional args are given they will be passed to the used Python \
interpreter.")
        )

        parser.add_option(
            "-d", "--doc", dest="doc", action="store_true",
            default=False, help=_("open HTML documentation and exit")
        )

        parser.add_option(
            "-u", "--update", dest="update", action="store_true",
            default=False, help=_("update user configuration and exit")
        )

        parser.add_option(
            "-b", "--backup", dest="backup", action="store_true",
            default=False, help=_("backup user configuration and exit")
        )

        parser.add_option(
            "-r", "--restore", dest="restore", action="store_true",
            default=False, help=_("restore user configuration backup and exit")
        )

        parser.add_option(
            "-R", "--reset", dest="reset", action="store_true",
            default=False, help=_("reset user configuration and exit")
        )

        (options, args) = parser.parse_args()

        if options.version:
            print("%s" % os.getenv('BSNG_VERSION'))
            sys.exit(0)

        if options.prefix:
            print("%s" % os.getenv('BSNG_PREFIX'))
            sys.exit(0)

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
