# coding=utf-8
# #######################################################
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright Christopher Roy Bratušek                    #
#                                                       #
# #######################################################

MODULES = ['sys', 'widgethandler', 'dicts', 'prompts']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

try:
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version('GtkSource', '5')
    from gi.repository import Gtk, GtkSource
except ImportError:
    FAILED.append(_("Gtk (from gi.repository)"))

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

gtkbuilder = widgethandler.gtkbuilder


class PromptBuilder(object):

    def __init__(self, cfo, udc, fdc):
        self.config = cfo
        self.userdefault = udc
        self.factorydefault = fdc

    def InitPromptBuilder(self):

        WidgetHandler = widgethandler.WidgetHandler(self.config, self.userdefault, self.factorydefault)

        lang_manager = GtkSource.LanguageManager.get_default()
        bash_lang = lang_manager.get_language("sh")
        scheme_manager = GtkSource.StyleSchemeManager.get_default()

        def on_theme_changed(self, manager, pspec):
            self.update_source_scheme()

        def update_source_scheme(self):
            scheme_manager = GtkSource.StyleSchemeManager.get_default()
            if self.gtk_settings.get_property("gtk-application-prefer-dark-theme"):
                scheme = scheme_manager.get_scheme("oblivion")
            else:
                scheme = scheme_manager.get_scheme("tango")
            if scheme:
                self.prompt_command_buffer.set_style_scheme(scheme)
                self.custom_prompt_buffer.set_style_scheme(scheme)

        # GtkTextView
        self.prompt_command_buffer = GtkSource.Buffer()
        self.prompt_command_buffer.set_enable_undo(True)
        self.prompt_command_buffer.set_language(bash_lang)
        self.prompt_command_buffer.set_highlight_syntax(True)
        self.prompt_command_buffer.set_text(f"{self.config['Custom']['command']}")

        self.prompt_command = GtkSource.View.new_with_buffer(self.prompt_command_buffer)
        self.prompt_command.set_wrap_mode(Gtk.WrapMode.NONE)
        self.prompt_command.set_show_line_numbers(True)
        self.prompt_command.set_highlight_current_line(True)
        self.prompt_command.set_auto_indent(True)
        WidgetHandler.ReplaceWidget("prompt_command", self.prompt_command)

        self.custom_prompt_buffer = GtkSource.Buffer()
        self.custom_prompt_buffer.set_enable_undo(True)
        self.custom_prompt_buffer.set_language(bash_lang)
        self.custom_prompt_buffer.set_highlight_syntax(True)
        self.custom_prompt_buffer.set_text(f"{self.config['Custom']['prompt']}")

        self.custom_prompt = GtkSource.View.new_with_buffer(self.custom_prompt_buffer)
        self.custom_prompt.set_wrap_mode(Gtk.WrapMode.NONE)
        self.custom_prompt.set_show_line_numbers(True)
        self.custom_prompt.set_highlight_current_line(True)
        self.custom_prompt.set_auto_indent(True)
        WidgetHandler.ReplaceWidget("custom_prompt", self.custom_prompt)

        self.gtk_settings = Gtk.Settings.get_default()
        self.gtk_settings.connect("notify::gtk-application-prefer-dark-theme", on_theme_changed)
        update_source_scheme(self)

        def set_custom_prompt(widget, setting):
            start = widget.get_start_iter()
            end = widget.get_end_iter()
            self.config["Custom"][f"{setting}"] = widget.get_text(start, end, False)

        self.prompt_command_buffer.connect("changed", set_custom_prompt, "command")
        self.custom_prompt_buffer.connect("changed", set_custom_prompt, "prompt")

        self.active_buffer = "P_C"

        def set_active_buffer(widget, buffer):
            self.active_buffer = buffer

        self.eventControllerPC = Gtk.EventControllerFocus.new()
        self.eventControllerPC.connect("enter", set_active_buffer, "P_C")
        self.prompt_command.add_controller(self.eventControllerPC)

        self.eventControllerPS1 = Gtk.EventControllerFocus.new()
        self.eventControllerPS1.connect("enter", set_active_buffer, "PS1")
        self.custom_prompt.add_controller(self.eventControllerPS1)

        # Helper Functions

        def prompt_add(widget, text_p_c, text_ps1):
            if self.active_buffer == "P_C":
                self.prompt_command_buffer.insert_at_cursor(text_p_c)
            elif self.active_buffer == "PS1":
                self.custom_prompt_buffer.insert_at_cursor(text_ps1)

        def prompt_add_combo(widget, data, dict_p_c, dict_ps1):
            if widget.get_selected() != 0:
                prompt_add(widget, dict_p_c[widget.get_selected()], dict_ps1[widget.get_selected()])
                widget.set_selected(0)

        # GtkButtons

        def do_empty(widget, data):
            if self.active_buffer == "P_C":
                self.prompt_command_buffer.set_text("")
            elif self.active_buffer == "PS1":
                self.custom_prompt_buffer.set_text("")

        def do_undo(widget, data):
            if self.active_buffer == "P_C" and self.prompt_command_buffer.get_can_undo():
                self.prompt_command_buffer.undo()
            elif self.active_buffer == "PS1" and self.custom_prompt_buffer.get_can_undo():
                self.custom_prompt_buffer.undo()

        def do_redo(widget, data):
            if self.active_buffer == "P_C" and self.prompt_command_buffer.get_can_redo():
                self.prompt_command_buffer.redo()
            elif self.active_buffer == "PS1" and self.custom_prompt_buffer.get_can_redo():
                self.custom_prompt_buffer.redo()

        def do_reset(widget, data):
            self.prompt_command_buffer.set_text("%s" % self.userdefault["Custom"]["command"])
            self.custom_prompt_buffer.set_text("%s" % self.userdefault["Custom"]["prompt"])

        def do_revert(widget, data):
            self.prompt_command_buffer.set_text("%s" % self.factorydefault["Custom"]["command"])
            self.custom_prompt_buffer.set_text("%s" % self.factorydefault["Custom"]["prompt"])

        WidgetHandler.InitWidget("cpb_empty", do_empty, None, "button", None)
        WidgetHandler.InitWidget("cpb_undo", do_undo, None, "button", None)
        WidgetHandler.InitWidget("cpb_redo", do_redo, None, "button", None)
        WidgetHandler.InitWidget("cpb_reset", do_reset, None, "button", None)
        WidgetHandler.InitWidget("cpb_factory", do_revert, None, "button", None)

        # Toolbox

        def do_show_toolbox(widget, data):
            toolbox = gtkbuilder.get_object("Toolbox")
            toolbox_close = gtkbuilder.get_object("toolbox.close")
            if not hasattr(toolbox, "_signals_connected"):
                toolbox.connect("close-request", on_toolbox_close_request)
                toolbox_close.connect("clicked", lambda w: toolbox.hide())
                toolbox._signals_connected = True
            toolbox.present()

        def on_toolbox_close_request(window):
            window.hide()
            return True

        WidgetHandler.InitWidget("show_toolbox", do_show_toolbox, None, "button", None)

        # Toolbox Buttons

        WidgetHandler.InitWidget("username", "${USER}", "\\u", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("hostname", "${HOSTNAME/.*}", "\\h", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("fhostname", "${HOSTNAME}", "\\H", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("time", "$(date +%H:%M:%S)", "\\t", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("date", "$(date date +%d.%m.%Y)", "\\d", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("sign", "", "\\$", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("fworkdir", "${PWD}", "\\w", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("workdir", "${PWD/*\\/}", "\\W", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("euid", "${EUID}", "${EUID}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("jobs", "$(jobs -pr)", "\\j", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("bang", "", "\\!", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("number", "", "\\#", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("pid", "${BAHSPID}", "${BASHPID}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("shlvl", "${SHLVL}", "${SHLVL}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("truncpwd", "$(truncpwd)", "\\$(truncpwd)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showsize", "$(systemkit dirsize)", "\\$(systemkit dirsize)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("countprocesses", "$(systemkit processes)", "\\$(systemkit processes)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showuptime", "$(systemkit uptime)", "\\$(systemkit uptime)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showtty", "$(systemkit tty)", "\\$(systemkit tty)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showcpuload", "$(systemkit cpuload)", "\\$(systemkit cpuload)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showseconds", "${SECONDS}", "${SECONDS}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showbatteryload", "$(systemkit battery)", "\\$(systemkit battery)", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showexit", "${lastexit}", "${lastexit}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showlastcmd", "${lastcommand}", "${lastcommand}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showlastcmd_cut", "${lastcommandprintable}", "${lastcommandprintable}", "cpb_button", prompt_add)
        WidgetHandler.InitWidget("showuser", "${showuser}", "\\$(showuser)", "cpb_button", prompt_add)

        # Toolbox Comboboxes

        WidgetHandler.InitWidget("showmem", dicts.memory_getters_p_c, dicts.memory_getters_ps1, "cpb_combo", prompt_add_combo)
        WidgetHandler.InitWidget("showspace", dicts.space_getters_p_c, dicts.space_getters_ps1, "cpb_combo", prompt_add_combo)
        WidgetHandler.InitWidget("countfiles", dicts.counters_p_c, dicts.counters_ps1, "cpb_combo", prompt_add_combo)
        WidgetHandler.InitWidget("showload", dicts.load_getters_p_c, dicts.load_getters_ps1, "cpb_combo", prompt_add_combo)
        WidgetHandler.InitWidget("insert_color", dicts.symbolic_colors_p_c, dicts.symbolic_colors_ps1, "cpb_combo", prompt_add_combo)

        # Default Styles

        self.insert_prompt = gtkbuilder.get_object("insert_prompt")
        self.insert_prompt.set_selected(0)

        def do_insert_prompt(widget, data=None):
            selection = widget.get_selected()
            if selection != 0:
                self.prompt_command_buffer.set_text(prompts.styles_pc[selection])
                self.custom_prompt_buffer.set_text(prompts.styles_ps1[selection])

        self.insert_prompt.connect("notify::selected", do_insert_prompt)
