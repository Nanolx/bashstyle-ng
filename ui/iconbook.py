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

MODULES = ['sys', 'os', 'widgethandler', 'subprocess', 'dicts']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk
    gi.require_version("Gdk", "4.0")
    from gi.repository import Gdk, Gio, GObject
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_("The following modules failed to import: %s")
          % (" ".join(FAILED)))
    sys.exit(1)

gtkbuilder = widgethandler.gtkbuilder

class IconItem(GObject.Object):
    def __init__(self, name, label):
        super().__init__()
        self.name = name
        self.label = label

class IconBook(object):
    def InitIconBook(self):
        self.gridview = gtkbuilder.get_object("iconview")
        self.model = Gio.ListStore(item_type=IconItem)
        no_selection = Gtk.NoSelection(model=self.model)
        self.gridview.set_model(no_selection)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.on_setup_grid_item)
        factory.connect("bind", self.on_bind_grid_item)
        self.gridview.set_factory(factory)

        self.notebook = gtkbuilder.get_object("notebook")
        self.back = gtkbuilder.get_object("back")
        self.back.set_visible(False)
        self.back.connect("clicked", self.back_clicked)
        self.main_label = gtkbuilder.get_object("main.label")

        for icon_name in dicts.iconview_icons:
            label_text = dicts.iconview_labels.get(icon_name, icon_name)
            self.model.append(IconItem(icon_name, label_text))

        self.setup_css()

    def setup_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data("""
            gridview child {
                padding: 0;
                background: transparent;
            }
            .icon-card {
                padding: 15px;
                border-radius: 12px;
                transition: all 200ms ease-out;
            }
            gridview child:hover .icon-card {
                background-color: alpha(@theme_fg_color, 0.1);
                transform: translateY(-2px);
            }
            gridview child:hover .icon-card image {
                transform: scale(1.15);
                transition: transform 200ms ease-out;
            }
            gridview child:hover .icon-card label {
                font-weight: bold;
                color: @theme_selected_bg_color;
            }
        """.encode())

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_setup_grid_item(self, factory, list_item):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.add_css_class("icon-card")

        img = Gtk.Image(pixel_size=32)
        lbl = Gtk.Label()

        box.append(img)
        box.append(lbl)
        list_item.set_child(box)

        gesture = Gtk.GestureClick()
        gesture.connect("released", self.on_item_clicked, list_item)
        box.add_controller(gesture)

    def on_bind_grid_item(self, factory, list_item):
        item = list_item.get_item()
        box = list_item.get_child()

        if box and item:
            img = box.get_first_child()
            lbl = box.get_last_child()

            img.set_from_icon_name(item.name)
            lbl.set_label(item.label)

    def on_item_clicked(self, gesture, n_press, x, y, list_item):
        item = list_item.get_item()
        if not item:
            return

        label = item.label

        if label == _("Documentation"):
            self.back.set_visible(False)
            path = os.getenv('BSNG_DATADIR') + "/doc/bashstyle-ng/index.html"
            subprocess.Popen(["xdg-open", path])
        elif label == _("Start Terminal"):
            self.back.set_visible(False)
            subprocess.Popen(["x-terminal-emulator"])
        else:
            page_num = dicts.notebook_pages.get(label, 0)
            self.notebook.set_current_page(page_num)
            self.back.set_visible(True)
            self.main_label.set_visible(True)
            self.main_label.set_text(_("Category: ") + _(label))

    def back_clicked(self, btn):
        self.notebook.set_current_page(0)
        self.back.set_visible(False)
        self.main_label.set_visible(False)