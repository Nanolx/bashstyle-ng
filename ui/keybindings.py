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

MODULES = ['sys', 'widgethandler', 'dicts']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Gdk", "4.0")
    gi.require_version("Gio", "2.0")
    from gi.repository import Gtk, Gdk, Gio, GObject
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))


if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

gtkbuilder = widgethandler.gtkbuilder

class KeyItem(GObject.Object):
    label = GObject.Property(type=str)
    alt = GObject.Property(type=bool, default=False)
    ctrl = GObject.Property(type=bool, default=False)
    nmod = GObject.Property(type=bool, default=False)
    key = GObject.Property(type=str)

    def __init__(self, label, alt, ctrl, nmod, key):
        super().__init__()
        self.label = label
        self.alt = alt
        self.ctrl = ctrl
        self.nmod = nmod
        self.key = key

class KeyTree(object):
    def __init__(self, cfo, udc, fdc):
        self.config = cfo
        self.userdefault = udc
        self.factorydefault = fdc
        self.model = Gio.ListStore(item_type=KeyItem)

    def InitTree(self):
        self.use_keys = gtkbuilder.get_object("use_keybindings")
        self.tree = gtkbuilder.get_object("keybindings_columview")

        selection = Gtk.SingleSelection(model=self.model)
        self.tree.set_model(selection)
        self.tree.set_hexpand(True)

        css_provider = Gtk.CssProvider()
        css_data = """
            columnview, columnview listview {
                background-color: transparent;
            }
            columnview listview row:nth-child(even) {
                background-color: alpha(@theme_fg_color, 0.02);
            }
            columnview listview row:hover {
                background-color: alpha(@theme_fg_color, 0.05);
            }
            columnview header button {
                background: transparent;
                border: none;
            }
            columnview listview row cell {
                padding-left: 4px;
                padding-right: 4px;
            }
            columnview row entry,
            columnview row entry > text,
            columnview row entry > stack > text {
                background-color: transparent;
                background-image: none;
                box-shadow: none;
                border: none;
                color: inherit;
            }
        """
        css_provider.load_from_string(css_data)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self._add_column("Binding", self._create_text_factory("label"))
        self._add_column("Alt", self._create_radio_factory("alt"))
        self._add_column("Ctrl", self._create_radio_factory("ctrl"))
        self._add_column("None", self._create_radio_factory("nmod"))
        self._add_column("Key", self._create_edit_factory())
        self._add_column("Revert", self._create_button_factory("edit-undo", self.on_revert_user))
        self._add_column("Default", self._create_button_factory("edit-clear", self.on_revert_factory))

        self.populate(dicts.keybindings)

        header_row = self.tree.get_first_child()
        if header_row:
            header_cell = header_row.get_first_child()
            current_index = 0
            while header_cell:
                if current_index != 0 and current_index != 4:
                    header_cell.set_halign(Gtk.Align.CENTER)
                header_cell = header_cell.get_next_sibling()
                current_index += 1

        self.use_keys.set_active(self.config["Keybindings"].as_bool("use_keybindingscfg"))
        self.tree.set_sensitive(self.use_keys.get_active())

        def on_use_keys(widget, data):
            self.config["Keybindings"]["use_keybindingscfg"] = widget.get_active()
            self.tree.set_sensitive(widget.get_active())

        self.use_keys.connect("notify::active", on_use_keys)

    def _add_column(self, title, factory):
        col = Gtk.ColumnViewColumn(title=title, factory=factory)
        col.set_expand(True)
        self.tree.append_column(col)

    def _create_text_factory(self, attr):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", lambda f, item: item.set_child(Gtk.Label(xalign=0)))
        factory.connect("bind", lambda f, item: item.get_child().set_label(getattr(item.get_item(), attr)))
        return factory

    def _create_radio_factory(self, attr):
        factory = Gtk.SignalListItemFactory()

        def on_setup(f, list_item):
            rb = Gtk.CheckButton()
            rb.set_halign(Gtk.Align.CENTER)
            rb.set_valign(Gtk.Align.CENTER)
            rb.add_css_class("selection-mode")
            list_item.set_child(rb)

        def on_bind(f, list_item):
            row_item = list_item.get_item()
            rb = list_item.get_child()

            if not hasattr(row_item, "_radio_group"):
                row_item._radio_group = {}

            row_item._radio_group[attr] = rb
            if "alt" in row_item._radio_group and "ctrl" in row_item._radio_group and "nmod" in row_item._radio_group:
                row_item._radio_group["ctrl"].set_group(row_item._radio_group["alt"])
                row_item._radio_group["nmod"].set_group(row_item._radio_group["alt"])

            rb.connect("toggled", self.on_radio_toggled, row_item, attr)
            row_item.bind_property(attr, rb, "active", GObject.BindingFlags.SYNC_CREATE)

        factory.connect("setup", on_setup)
        factory.connect("bind", on_bind)
        return factory

    def on_radio_toggled(self, rb, row_item, attr):
        if rb.get_active():
            if getattr(row_item, attr) != True:
                row_item.alt = (attr == "alt")
                row_item.ctrl = (attr == "ctrl")
                row_item.nmod = (attr == "nmod")
                self.update_config(row_item)

    def _create_button_factory(self, icon, callback):
        factory = Gtk.SignalListItemFactory()

        def on_setup(f, list_item):
            btn = Gtk.Button(icon_name=icon)
            btn.add_css_class("flat")
            btn.set_valign(Gtk.Align.CENTER)
            btn.set_halign(Gtk.Align.CENTER)
            list_item.set_child(btn)

        def on_bind(f, list_item):
            btn = list_item.get_child()
            row_item = list_item.get_item()
            btn.connect("clicked", callback, row_item)

        factory.connect("setup", on_setup)
        factory.connect("bind", on_bind)
        return factory

    def _create_edit_factory(self):
        factory = Gtk.SignalListItemFactory()

        def on_setup(f, list_item):
            entry = Gtk.Entry()
            list_item.set_child(entry)

        def on_bind(f, list_item):
            row_item = list_item.get_item()
            entry = list_item.get_child()
            row_item.bind_property("key", entry, "text",
                                 GObject.BindingFlags.SYNC_CREATE |
                                 GObject.BindingFlags.BIDIRECTIONAL)

            def on_notify(obj, pspec):
                self.update_config(obj)

            row_item.connect("notify::key", on_notify)

        factory.connect("setup", on_setup)
        factory.connect("bind", on_bind)
        return factory

    def prepare(self, setting):
        value = self.config["Keybindings"].get(setting, "")
        if value == "":
            modifier = ""
            boundkey = ""
        else:
            parts = value.split(":")
            modifier = parts[0]
            boundkey = parts[1] if len(parts) > 1 else ""
        label = setting.replace("_", "-")
        return modifier, boundkey, label

    def on_revert_user(self, btn, row_item):
        setting = row_item.label.replace("-", "_")
        default_val = self.userdefault["Keybindings"].get(setting, "")
        self.apply_revert(row_item, default_val)

    def on_revert_factory(self, btn, row_item):
        setting = row_item.label.replace("-", "_")
        default_val = self.factorydefault["Keybindings"].get(setting, "")
        self.apply_revert(row_item, default_val)

    def apply_revert(self, row_item, config_value):
        if config_value == "":
            row_item.alt = False
            row_item.ctrl = False
            row_item.nmod = False
            row_item.key = ""
        else:
            parts = config_value.split(":")
            modifier = parts[0]
            row_item.key = parts[1] if len(parts) > 1 else ""
            row_item.alt = (modifier == "e")
            row_item.ctrl = (modifier == "C")
            row_item.nmod = (modifier == "X")
        self.update_config(row_item)

    def populate(self, settings):
        self.model.remove_all()
        for key in sorted(settings):
            modifier, boundkey, label = self.prepare(key)
            item = KeyItem(
                label=label,
                alt=(modifier == "e"),
                ctrl=(modifier == "C"),
                nmod=(modifier == "X"),
                key=boundkey
            )
            self.model.append(item)

    def update_config(self, row_item):
        setting = row_item.label.replace("-", "_")
        if row_item.key == "":
            new_value = ""
        else:
            if row_item.alt:
                prefix = "e:"
            elif row_item.ctrl:
                prefix = "C:"
            elif row_item.nmod:
                prefix = "X:"
            else:
                prefix = ""
            new_value = f"{prefix}{row_item.key}"
        self.config["Keybindings"][setting] = new_value