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

import os
import gi
import configparser
from gi.repository import Gio
from pathlib import Path

def is_adwaita_default():
    try:
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        current_theme = settings.get_string("gtk-theme").lower()
        return "adwaita" in current_theme
    except Exception:
        return True

def is_kde_environment():
    current_desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    desktop_session = os.environ.get("DESKTOP_SESSION", "").lower()
    return "kde" in current_desktop or "kde" in desktop_session or "plasma" in current_desktop

def is_kde_dark_mode():
    try:
        kde_config_path = Path.home() / ".config" / "kdeglobals"
        if not kde_config_path.exists():
            return False
        config = configparser.ConfigParser()
        config.read(kde_config_path)
        if config.has_section("General"):
            color_scheme = config.get("General", "ColorScheme", fallback="").lower()
            if "dark" in color_scheme or "black" in color_scheme:
                return True
        if config.has_section("Colors:Window"):
            bg_color_str = config.get("Colors:Window", "BackgroundNormal", fallback="")
            if bg_color_str:
                rgb = [int(x) for x in bg_color_str.split(",")]
                if len(rgb) >= 3:
                    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2])
                    return luminance < 128
    except Exception as e:
        print(f"Erorr reading KDE color scheme: {e}")
    return False

USE_ADWAITA = is_adwaita_default()
USE_KDE = is_kde_environment()
KDE_DARK = is_kde_dark_mode()