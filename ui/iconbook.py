# coding=utf-8
# ##################################################### #
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright Christopher Bratusek                        #
#                                                       #
# ##################################################### #

MODULES = ['sys', 'os', 'widgethandler', 'subprocess', 'dicts']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    from gi.repository import Gtk
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

try:
    from gi.repository.GdkPixbuf import Pixbuf
except ImportError:
    FAILED.append(_("GdkPixbuf (from gi.repository)"))

if FAILED:
    print(
        _("The following modules failed to import: %s")
        % (" ".join(FAILED))
    )
    sys.exit(1)

gtkbuilder = widgethandler.gtkbuilder


class IconBook(object):

    def InitIconBook(self):

        liststore = gtkbuilder.get_object("iconviewstore")
        iconview = gtkbuilder.get_object("iconview")
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)
        iconview.set_activate_on_single_click(True)

        notebook = gtkbuilder.get_object("notebook")
        notebook.set_current_page(0)

        main_label = gtkbuilder.get_object("main.label")
        main_label.set_visible(0)

        def back_clicked(data):
            notebook.set_current_page(0)
            back.set_visible(0)
            main_label.set_visible(0)

        back = gtkbuilder.get_object("back")
        back.connect("clicked", back_clicked)
        back.set_visible(0)

        for icon in dicts.iconview_icons:
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 32, 0)
            liststore.append([pixbuf, dicts.iconview_labels[icon]])

        def iconview_activated(widget, item):
            model = widget.get_model()
            if model[item][1] == _("Documentation"):
                back.set_visible(0)
                subprocess.Popen(
                    ["xdg-open", "%s" % os.getenv('BSNG_DATADIR') +
                     "/doc/bashstyle-ng/index.html"]
                )
            elif model[item][1] == _("Start Terminal"):
                back.set_visible(0)
                subprocess.Popen(["x-terminal-emulator"])
            else:
                notebook.set_current_page(dicts.notebook_pages[model[item][1]])
                back.set_visible(1)
                main_label.set_visible(1)
                main_label.set_text(_("Category: ") + _(model[item][1]))

        iconview.connect("item-activated", iconview_activated)
