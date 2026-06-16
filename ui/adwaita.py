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

import gi
from gi.repository import Gio

def is_adwaita_default():
    try:
        settings = Gio.Settings.new("org.gnome.desktop.interface")
        current_theme = settings.get_string("gtk-theme").lower()
        return "adwaita" in current_theme or current_theme == "default"
    except Exception:
        return True

USE_ADWAITA = is_adwaita_default()