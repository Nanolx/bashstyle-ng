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

        selection = Gtk.SingleSelection(model=self.model)
        selection.connect("selection-changed", self.on_selection_changed)
        self.gridview.set_model(selection)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.on_setup_grid_item)
        factory.connect("bind", self.on_bind_grid_item)
        self.gridview.set_factory(factory)

        self.notebook = gtkbuilder.get_object("notebook")
        self.notebook.set_current_page(0)
        self.main_label = gtkbuilder.get_object("main.label")
        self.main_label.set_visible(False)
        self.back = gtkbuilder.get_object("back")
        self.back.set_visible(False)
        self.back.connect("clicked", self.back_clicked)

        for icon in dicts.iconview_icons:
            label = dicts.iconview_labels[icon]
            self.model.append(IconItem(icon, label))

        provider = Gtk.CssProvider()
        provider.load_from_data("""
            gridview child {
                padding: 10px;
                border-radius: 8px;
                transition: all 200ms ease-out;
            }
            gridview child:hover {
                background-color: alpha(@theme_fg_color, 0.1);
                transform: translateY(-2px);
            }
            gridview child:focus {
                background-color: alpha(@theme_selected_bg_color, 0.2);
                outline: 2px solid alpha(@theme_selected_bg_color, 0.5);
            }
            gridview child:hover image {
                transform: scale(1.15);
                transition: transform 200ms ease-out;
            }
            gridview child:hover label {
                font-weight: bold;
                color: @theme_selected_bg_color;
            }
            gridview child image {
                margin-bottom: 5px;
                filter: drop-shadow(0 2px 2px rgba(0,0,0,0.1));
            }
        """.encode())

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_setup_grid_item(self, factory, list_item):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        box.set_margin_top(10)
        box.set_margin_bottom(10)

        icon = Gtk.Image(pixel_size=32)
        label = Gtk.Label()

        box.append(icon)
        box.append(label)
        list_item.set_child(box)

    def on_bind_grid_item(self, factory, list_item):
        row_item = list_item.get_item()
        box = list_item.get_child()
        icon_widget = box.get_first_child()
        label_widget = box.get_last_child()

        icon_widget.set_from_icon_name(row_item.name)
        label_widget.set_label(row_item.label)

    def on_selection_changed(self, selection, position, n_items):
        item = selection.get_selected_item()
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
            self.notebook.set_current_page(dicts.notebook_pages[label])
            self.back.set_visible(True)
            self.main_label.set_visible(True)
            self.main_label.set_text(_("Category: ") + _(label))

        selection.set_selected(Gtk.INVALID_LIST_POSITION)

    def back_clicked(self, btn):
        self.notebook.set_current_page(0)
        self.back.set_visible(False)
        self.main_label.set_visible(False)
        self.gridview.get_model().set_selected(Gtk.INVALID_LIST_POSITION)