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

MODULES = ['os', 'sys', 'iconspinbutton', 'adwaita', 'dicts']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, GObject, GLib
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

DATADIR = os.getenv('BSNG_DATADIR')
blacklist = ['\'', '\"']
gtkbuilder = Gtk.Builder()
gtkbuilder.set_translation_domain("bashstyle")
gtkbuilder.add_from_file(DATADIR + "/bashstyle-ng/ui/bashstyle.ui")

class WidgetHandler(object):
    def __init__(self, cfo, udc, fdc):
        self.config = cfo
        self.userdefault = udc
        self.factorydefault = fdc

    def SwapDictionary(self, original_dict):
        try:
            iteritems = original_dict.iteritems
        except AttributeError:
            iteritems = original_dict.items
        return dict([(v, k) for (k, v) in iteritems()])

    def InitEntry(self, widget, group, setting, max_len=-1):
        object = gtkbuilder.get_object(f"{widget}")

        object.set_text(f"{self.config[group][setting]}")
        if max_len > 0: object.set_max_length(max_len)

        def revert_option(widget, pos, widget_group, widget_setting):
            if pos == Gtk.EntryIconPosition.SECONDARY:
                opt = self.factorydefault[widget_group][widget_setting]
            else:
                opt = self.userdefault[widget_group][widget_setting]
            self.config[widget_group][widget_setting] = opt
            widget.set_text(f"{opt}")
            self.config.write()

        def set_option(widget, widget_group, widget_setting):
            self.config[widget_group][widget_setting] = widget.get_text()
            self.config.write()

        def emit_text(widget, text, *args):
            if text in blacklist:
                widget.emit_stop_by_name('insert-text')

        object.connect("insert-text", emit_text)
        object.connect("icon-press", revert_option, group, setting)
        object.connect("changed", set_option, group, setting)

        return object

    def InitSwitch(self, widget, group, setting, grid):
        object = gtkbuilder.get_object(f"{widget}")

        object.set_active(self.config[group].as_bool(setting))

        def set_option(widget, data, widget_group, widget_setting):
            self.config[widget_group][widget_setting] = widget.get_active()
            self.config.write()

        object.connect("notify::active", set_option, group, setting)
        object.connect("notify::active", self.DisableChilds, grid)
        self.DisableChilds(object, None, grid)

        return object

    def InitCheckButton(self, widget, group, setting):
        object = gtkbuilder.get_object(f"{widget}")

        object.set_active(self.config[group].as_bool(setting))

        def set_option(widget, widget_group, widget_setting):
            self.config[widget_group][widget_setting] = widget.get_active()
            self.config.write()

        object.connect("toggled", set_option, group, setting)

        return object

    def InitDropDown(self, widget, group, setting, dict):
        object = gtkbuilder.get_object(f"{widget}")

        object.set_selected(self.SwapDictionary(dict)[self.config[group][setting]])

        def set_option(widget, widget_group, widget_setting, dict):
            self.config[widget_group][widget_setting] = dict[widget.get_selected()]
            self.config.write()

        object.connect("notify::selected", set_option, type, dict, group, setting)

        return object

    def InitWidget(self, widget, group, setting, type, dict):
        # known widget types:
        #   text        GtkTextEntry
        #   int         GtkSpinButton
        #   bool        GtkToggleButton / GtkRadioButton
        #   switch      GtkSwitch
        #   combo       GtkDropDown
        #   button      GtkButton
        #   label       GtkLabel
        #   cpb_button  Custom Prompt Builder GtkButton
        #   cpb_combo   Custom Prompt Builder GtkDropDown
        #   link        GtkLinkButton

        def LoadWidget():
            object = gtkbuilder.get_object(f"{widget}")
            return object

        def LoadValue():
            if type == "int":
                object.set_value(self.config[group].as_int(setting))
            elif type == "label":
                object.set_label(f"{setting}")
            elif type == "link":
                object.set_uri(f"{setting}")
            elif type == "cpb_combo":
                object.set_selected(0)

        def ConnectSignals():
            if type == "int":
                object.connect("value-changed", set_option, None, type, None, group, setting)
            elif type == "button":
                object.connect("clicked", group, setting)
            elif type == "cpb_button":
                object.connect("clicked", dict, group, setting)
            elif type == "cpb_combo":
                object.connect("notify::selected", dict, group, setting)

        def set_option(widget, data, type, dict, widget_group, widget_setting):
            if type == "int":
                self.config[widget_group][widget_setting] = widget.get_value_as_int()
            self.config.write()

        object = LoadWidget()
        LoadValue()
        ConnectSignals()
        return object

    def DisableChilds(self, widget, pspec, grid_widget, filter=None, inverted=False):
        is_active = widget.get_active()
        target_sensitive_state = not is_active if inverted else is_active
        grid = gtkbuilder.get_object(grid_widget)
        grid_layout = grid.get_layout_manager()
        current_child = grid.get_first_child()
        parent = widget.get_parent()

        if filter:
            filter_tuple = (filter,) if isinstance(filter, str) else tuple(filter)
        else:
            filter_tuple = ()

        while current_child is not None:
            if current_child == parent or current_child == widget:
                current_child = current_child.get_next_sibling()
                continue
            if filter_tuple:
                child_name = current_child.get_buildable_id()
                if child_name and child_name.startswith(filter_tuple):
                    current_child = current_child.get_next_sibling()
                    continue
            current_child.set_sensitive(target_sensitive_state)
            current_child = current_child.get_next_sibling()

    def ReplaceWidget(self, placeholder_id, new_widget):
        placeholder = gtkbuilder.get_object(placeholder_id)
        if not placeholder:
            print(_(f"Error: placeholder wasn't found in XML UI definition: {placeholder_id}"))
            return False

        parent = placeholder.get_parent()
        if not parent:
            print(_(f"Error: placeholder has no parent container: {placeholder_id}"))
            return False

        new_widget.set_hexpand(placeholder.get_hexpand())
        new_widget.set_vexpand(placeholder.get_vexpand())
        new_widget.set_halign(placeholder.get_halign())
        new_widget.set_valign(placeholder.get_valign())
        new_widget.set_margin_start(placeholder.get_margin_start())
        new_widget.set_margin_end(placeholder.get_margin_end())
        new_widget.set_margin_top(placeholder.get_margin_top())
        new_widget.set_margin_bottom(placeholder.get_margin_bottom())

        if isinstance(parent, Gtk.Grid):
            grid_layout = parent.get_layout_manager()
            grid_child = grid_layout.get_layout_child(placeholder)
            if grid_child:
                col = grid_child.get_column()
                row = grid_child.get_row()
                col_span = grid_child.get_column_span()
                row_span = grid_child.get_row_span()

                parent.remove(placeholder)
                parent.attach(new_widget, col, row, col_span, row_span)
            else:
                parent.remove(placeholder)
                parent.attach(new_widget, 0, 0, 1, 1)
        elif isinstance(parent, Gtk.Box):
            sibling = None
            current = parent.get_first_child()
            while current is not None:
                if current == placeholder:
                    break
                sibling = current
                current = current.get_next_sibling()

            parent.remove(placeholder)
            if sibling:
                parent.insert_child_after(new_widget, sibling)
            else:
                parent.prepend(new_widget)
        else:
            if hasattr(parent, "remove"):
                parent.remove(placeholder)
            if hasattr(parent, "set_child"):
                parent.set_child(new_widget)
            elif hasattr(parent, "append"):
                parent.append(new_widget)
        return True

    def InitIconSpinButton(self, placeholder, name, group, setting, minvalue, maxvalue):
        object = iconspinbutton.CustomIconSpinButton(
            primary_icon_name="edit-undo", secondary_icon_name="edit-clear",
            min_val=minvalue, max_val=maxvalue, step=1, pixel_size=16)

        object.set_value(self.config[group].as_int(setting))

        def revert_option(widget, pos, widget_group, widget_setting):
            if pos == 1:
                opt = self.factorydefault[widget_group][widget_setting]
            else:
                opt = self.userdefault[widget_group][widget_setting]
            self.config[widget_group][widget_setting] = opt
            widget.set_value(self.config[widget_group].as_int(widget_setting))
            self.config.write()

        def set_option(widget, widget_group, widget_setting):
            self.config[widget_group][widget_setting] = widget.get_value_as_int()
            self.config.write()

        object.connect("value-changed", set_option, group, setting)
        object.connect("primary-icon-clicked", revert_option, 0, group, setting)
        object.connect("secondary-icon-clicked", revert_option, 1, group, setting)

        self.ReplaceWidget(placeholder, object)
        return object