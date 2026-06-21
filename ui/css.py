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

MODULES = ['os', 'sys', 'adwaita']
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
    from gi.repository import Gtk, Gdk
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

def bashstyle_gtk_css():
    css_provider = Gtk.CssProvider()
    css_data = """
    label.rotated_label {
        transform: rotate(90deg);
        font-weight: bold;
    }
    .monospace-label {
        font-family: monospace;
    }
    columnview,
    columnview listview {
        background-color: transparent;
    }
    columnview listview row:nth-child(even) {
        background-color: alpha(@theme_fg_color, 0.02);
    }
    columnview listview row:hover {
        background-color: alpha(@theme_fg_color, 0.05);
    }
    columnview listview row:selected {
        background-color: @theme_selected_bg_color;
        color: @theme_selected_fg_color;
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
    columnview row entry.error {
        background-color: alpha(@error_color, 0.15);
        border: 1px solid @error_color;
        border-radius: 4px;
        color: @error_color;
    }
    columnview listview row:selected radio {
        color: @theme_selected_fg_color;
        border-color: alpha(@theme_selected_fg_color, 0.6);
    }
    columnview listview row:selected radio:checked {
        background-color: @theme_selected_fg_color;
        color: @theme_selected_bg_color;
    }
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
    checkbutton:hover check,
    checkbutton:hover radio,
    button:hover {
        border-color: @theme_selected_bg_color;
        box-shadow: 0 0 4px 2px rgba(53, 132, 228, 0.4);
        background-color: rgba(53, 132, 228, 0.1);
    }
    .custom-spin-container {
        background-color: @view_bg_color;
        border: 1px solid transparent;
        border-radius: 6px;
        padding: 2px 6px;
        box-shadow: inset 0 0 0 1px alpha(currentColor, 0.15);
        transition: all 150ms ease-in-out;
    }
    .custom-spin-container:focus-within,
    .custom-spin-container:hover {
        outline: 2px solid @theme_selected_bg_color;
        outline-offset: -1px;
        border-color: transparent;
    }
    .custom-spin-container spinbutton {
        background: none;
        border: none;
        box-shadow: none;
    }
    .custom-spin-container spinbutton text {
        background: none;
        box-shadow: none;
        transition: all 150ms ease-in-out;
    }
    .inner-icon {
        opacity: 0.7;
    }
    .inner-icon:hover {
        opacity: 1.0;
    }
    entry:focus-within,
    entry:hover {
        outline: 2px solid @theme_selected_bg_color;
        outline-offset: -1px;
        border-color: transparent;
    }
     entry, columnview, gridview, check, radio, button, dropdown {
        transition: all 150ms ease-in-out;
    }
    """

    if adwaita.USE_ADWAITA:
        css_data += """
        dropdown popover listview row:selected {
            background-color: @accent_bg_color;
            color: @accent_fg_color;
        }
        dropdown popover listview row:selected label {
            color: @accent_fg_color;
        }
        dropdown:hover button.toggle {
            border-color: @accent_bg_color;
            box-shadow: inset 0 0 0 1px @accent_bg_color;
            background-color: rgba(53, 132, 228, 0.1);
        }
        dropdown:hover button.toggle label,
        dropdown:hover button.toggle image {
            color: @accent_bg_color;
        }
        columnview row cell {
            min-height: 0px;
            padding-top: 2px;
            padding-bottom: 2px;
            padding-left: 2px;
            padding-right: 2px;
        }
        columnview row cell checkbutton {
            min-width: 0px;
            min-height: 0px;
            padding: 0px;
            margin: 0px;
        }
        columnview row cell checkbutton check,
        columnview row cell checkbutton radio {
            min-width: 6px;
            min-height: 6px;
            padding: 0px;
            margin: 0px;
        }
        entry.custom-hover:hover,
        entry.custom-hover:focus-within {
            outline: 2px solid @theme_selected_bg_color;
            outline-offset: -1px;
            border-color: transparent;
        }
        .custom-spin-container {
            padding: 0px;
            margin: 0px;
        }
        .custom-spin-container spinbutton {
            min-height: 20px;
            padding-top: 1px;
            padding-bottom: 1px;
        }
        .custom-spin-container spinbutton text {
            padding-top: 2px;
            padding-bottom: 2px;
        }
        .custom-spin-container spinbutton button {
            padding: 2px 2px;
        }
        .custom-spin-container .inner-icon {
            margin-top: 1px;
            margin-bottom: 1px;
            margin-right: 6px;
            margin-left: 6px;
            padding: 2px;
        }
        """

    css_provider.load_from_string(css_data)

    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

