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

MODULES = ['os', 'sys']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, GObject
    gi.require_version("Gdk", "4.0")
    from gi.repository import Gdk
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_("The following modules failed to import: %s") % (" ".join(FAILED)))
    sys.exit(1)

# CustomIconSpinButton was written by Google AI
class CustomIconSpinButton(Gtk.Box):
    __gsignals__ = {
        'primary-icon-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'secondary-icon-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'value-changed': (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, primary_icon_name=None, secondary_icon_name=None,
                 min_val=0, max_val=100, step=1, pixel_size=24):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # 1. Eigene CSS-Klassen für das Styling zuweisen
        self.add_css_class("custom-spin-container")

        self.set_hexpand(True)
        self.set_halign(Gtk.Align.FILL)
        self.set_valign(Gtk.Align.CENTER)

        # 2. Primary Icon Setup
        if primary_icon_name:
            self.primary_icon = Gtk.Image.new_from_icon_name(primary_icon_name)
            self.primary_icon.set_pixel_size(pixel_size)
            self.primary_icon.set_valign(Gtk.Align.CENTER)
            self.primary_icon.add_css_class("inner-icon") # Für CSS-Padding links

            primary_gesture = Gtk.GestureClick.new()
            primary_gesture.connect("released", self._on_primary_clicked)
            self.primary_icon.add_controller(primary_gesture)

            self.append(self.primary_icon)

        # 3. Core SpinButton Component
        adjustment = Gtk.Adjustment.new(min_val, min_val, max_val, step, step * 10, 0)
        self.spin_button = Gtk.SpinButton(adjustment=adjustment, climb_rate=1.0, digits=0)

        self.spin_button.set_hexpand(True)
        self.spin_button.set_halign(Gtk.Align.FILL)
        self.spin_button.set_width_chars(-1)
        self.spin_button.set_max_width_chars(-1)

        # Margins für den inneren Abstand zu den Icons nutzen
        if primary_icon_name:
            self.spin_button.set_margin_start(6)
        if secondary_icon_name:
            self.spin_button.set_margin_end(6)

        self.spin_button.connect("changed", self._on_spin_value_changed)
        self.append(self.spin_button)

        # 4. Secondary Icon Setup
        if secondary_icon_name:
            self.secondary_icon = Gtk.Image.new_from_icon_name(secondary_icon_name)
            self.secondary_icon.set_pixel_size(pixel_size)
            self.secondary_icon.set_valign(Gtk.Align.CENTER)
            self.secondary_icon.add_css_class("inner-icon") # Für CSS-Padding rechts

            secondary_gesture = Gtk.GestureClick.new()
            secondary_gesture.connect("released", self._on_secondary_clicked)
            self.secondary_icon.add_controller(secondary_gesture)

            self.append(self.secondary_icon)

        # 5. CSS direkt für diese Komponente initialisieren
        self._setup_css()

    def _setup_css(self):
        """Erzeugt das CSS-Styling, das die Komponenten visuell verschmilzt."""
        css_provider = Gtk.CssProvider()
        css_data = """
        /* Der äußere Container bekommt das Aussehen einer GtkEntry */
        .custom-spin-container {
            background-color: @theme_bg_color;
            border: 1px solid @text_view_bg; /* Standard-Rahmenfarbe */
            border-radius: 6px;
            padding: 2px 6px;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.07);
        }

        /* Visuelles Feedback: Äußerer Rahmen leuchtet, wenn das innere Textfeld aktiv ist */
        .custom-spin-container:focus-within {
            border-color: @theme_selected_bg_color;
            outline: 2px solid rgba(53, 132, 228, 0.5); /* Adwaita Fokus-Blau */
        }

        /* Den nativen Rahmen des inneren SpinButtons und dessen Hintergrund entfernen */
        .custom-spin-container spinbutton {
            background: none;
            border: none;
            box-shadow: none;
        }
        .custom-spin-container spinbutton text {
            background: none;
            box-shadow: none;
        }

        /* Icons optisch leicht einrücken */
        .inner-icon {
            opacity: 0.7;
        }
        .inner-icon:hover {
            opacity: 1.0; /* Hover-Effekt für Interaktivität */
        }
        """
        css_provider.load_from_data(css_data, -1)

        # Den Style auf die App-Ebene (oder Display-Ebene) anwenden
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _on_primary_clicked(self, gesture, n_press, x, y):
        self.emit("primary-icon-clicked")

    def _on_secondary_clicked(self, gesture, n_press, x, y):
        self.emit("secondary-icon-clicked")

    def _on_spin_value_changed(self, spin_btn):
        self.emit("value-changed")

    def get_value_as_int(self):
        return self.spin_button.get_value_as_int()

    def set_value(self, value):
        self.spin_button.set_value(value)
