# coding=utf-8
# ##################################################### #
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright Christopher Roy Bratušek                        #
#                                                       #
# ##################################################### #

MODULES = ['os', 'sys', 'optparse']
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


class CmdArgs(object):
    parser = optparse.OptionParser(
        _("\n  bashstyle <option>\n\n\
        BashStyle-NG © 2007 - 2024 Christopher Roy Bratušek\n\
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
        "-l", "--log", dest="log", action="store_true",
        default=False, help=_("view BashStyle-NG log file")
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

    parser.add_option(
        "-i", "--ini-get", dest="ini-get", action="store_true",
        default=False, help=_("get the value of the specified setting")
    )

    parser.add_option(
        "-I", "--ini-set", dest="ini-set", action="store_true",
        default=False, help=_("set the value of the specified setting")
    )

    parser.add_option(
        "-E", "--enable", dest="enable", action="store_true",
        default=False, help=_("enable BashStyle-NG")
    )

    parser.add_option(
        "-D", "--disable", dest="disable", action="store_true",
        default=False, help=_("disable BashStyle-NG")
    )

    (options, args) = parser.parse_args()

    if options.version:
        print("%s (%s)" % (os.getenv('BSNG_VERSION'),
                           os.getenv('BSNG_CODENAME')))
        sys.exit(0)

    if options.prefix:
        print("%s" % os.getenv('BSNG_PREFIX'))
        sys.exit(0)
