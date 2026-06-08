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

MODULES = ['os', 'sys', 'iconspinbutton']
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
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
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

    def InitWidget(self, widget, group, setting, type, dict):
        # known widget types:
        #   text        GtkTextEntry
        #   int         GtkSpinButton
        #   bool        GtkToggleButton / GtkRadioButton
        #   switch      GtkSwitch
        #   combo       GtkComboBox
        #   button      GtkButton
        #   label       GtkLabel
        #   cpb_button  Custom Prompt Builder GtkButton
        #   cpb_combo   Custom Prompt Builder GtkComboBox
        #   link        GtkLinkButton

        # required parameters:
        #    for text, int, bool, switch:
        #    widget, group, setting, type, None
        #    for combo:
        #    widget, group, setting, type, dict
        #    for button:
        #    widget, action, actionarg, type, None
        #    for labels:
        #    widget, None, label, type, None
        #    for cpb_button:
        #    widget, pc_text, ps1_text, type, action
        #    for cpb_combo:
        #    widget, pc_dict, ps1_dict, type action
        #    for link:
        #    widget, None, link, type, None

        def LoadWidget():
            object = gtkbuilder.get_object("%s" % widget)
            return object

        def LoadValue():
            if type == "text":
                object.set_text("%s" % self.config["%s" % group]["%s" % setting])
            elif type == "int":
                object.set_value(self.config["%s" % group].as_int("%s" % setting))
            elif type == "bool":
                object.set_active(self.config["%s" % group].as_bool("%s" % setting))
            elif type == "switch":
                object.set_active(self.config["%s" % group].as_bool("%s" % setting))
            elif type == "combo":
                object.set_active(self.SwapDictionary(dict)[self.config["%s" % group]["%s" % setting]])
            elif type == "label":
                object.set_label("%s" % setting)
            elif type == "link":
                object.set_uri("%s" % setting)
            elif type == "cpb_combo":
                object.set_active(0)

        def ConnectSignals():
            if type == "text":
                object.connect("insert-text", emit_text)
                object.connect("icon-press", revert_option, type, group, setting)
                object.connect("changed", set_option, None, type, None, group, setting)
            elif type == "int":
                object.connect("value-changed", set_option, None, type, None, group, setting)
            elif type == "bool":
                object.connect("toggled", set_option, None, type, None, group, setting)
            elif type == "switch":
                object.connect("notify::active", set_option, type, None, group, setting)
            elif type == "combo":
                object.connect("changed", set_option, None, type, dict, group, setting)
            elif type == "button":
                object.connect("clicked", group, setting)
            elif type == "cpb_button":
                object.connect("clicked", dict, group, setting)
            elif type == "cpb_combo":
                object.connect("changed", dict, group, setting)

        def revert_option(widget, pos, type, widget_group, widget_setting):
            if type == "text":
                if pos == Gtk.EntryIconPosition.SECONDARY:
                    opt = self.factorydefault["%s" % widget_group]["%s" % widget_setting]
                else:
                    opt = self.userdefault["%s" % widget_group]["%s" % widget_setting]
                self.config["%s" % widget_group]["%s" % widget_setting] = opt
                widget.set_text("%s" % self.config["%s" % widget_group]["%s" % widget_setting])

        def set_option(widget, data, type, dict, widget_group, widget_setting):
            if type == "text":
                self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_text()
            elif type == "int":
                self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_value_as_int()
            elif type == "bool":
                self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_active()
            elif type == "switch":
                self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_active()
            elif type == "combo":
                self.config["%s" % widget_group]["%s" % widget_setting] = dict[widget.get_active()]

        def emit_text(widget, text, *args):
            if text in blacklist:
                widget.emit_stop_by_name('insert-text')

        object = LoadWidget()
        LoadValue()
        ConnectSignals()
        return object

    # ReplaceWidget was written by Google AI
    def ReplaceWidget(self, placeholder_id, new_widget):
        placeholder = gtkbuilder.get_object(placeholder_id)
        if not placeholder:
            print(f"Fehler: Platzhalter '{placeholder_id}' wurde im Builder-XML nicht gefunden.")
            return False

        parent = placeholder.get_parent()
        if not parent:
            print(f"Fehler: Platzhalter '{placeholder_id}' hat keinen Parent-Container.")
            return False

        if isinstance(parent, Gtk.Box):
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
        elif isinstance(parent, Gtk.Grid):
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
        else:
            parent.remove(placeholder)
            if hasattr(parent, "set_child"):
                parent.set_child(new_widget)
            elif hasattr(parent, "append"):
                parent.append(new_widget)

    def InitIconSpinButton(self, placeholder, name, group, setting, primaryicon, secondaryicon, minvalue, maxvalue, iconsize):
        def LoadWidget():
            widget = iconspinbutton.CustomIconSpinButton(primary_icon_name=primaryicon,
                secondary_icon_name=secondaryicon, min_val=minvalue,
                max_val=maxvalue, step=1, pixel_size=iconsize)
            return widget

        def LoadValue():
            object.set_value(self.config["%s" % group].as_int("%s" % setting))

        def ConnectSignals():
            object.connect("value-changed", set_option, group, setting)
            object.connect("primary-icon-clicked", revert_option, 0, group, setting)
            object.connect("secondary-icon-clicked", revert_option, 1, group, setting)

        def revert_option(widget, pos, widget_group, widget_setting):
            if pos == 1:
                opt = self.factorydefault["%s" % widget_group]["%s" % widget_setting]
            else:
                opt = self.userdefault["%s" % widget_group]["%s" % widget_setting]
            self.config["%s" % widget_group]["%s" % widget_setting] = opt
            widget.set_value(self.config["%s" % widget_group].as_int("%s" % widget_setting))

        def set_option(widget, widget_group, widget_setting):
            self.config["%s" % widget_group]["%s" % widget_setting] = widget.get_value_as_int()

        object = LoadWidget()
        LoadValue()
        ConnectSignals()
        self.ReplaceWidget(placeholder, object)
        return object
