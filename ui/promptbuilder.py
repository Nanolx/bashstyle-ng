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
        self.scheme_manager = GtkSource.StyleSchemeManager.get_default()

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

        def set_custom_prompt(widget, setting):
            start = widget.get_start_iter()
            end = widget.get_end_iter()
            self.config["Custom"][f"{setting}"] = widget.get_text(start, end, False)
            self.config.write()

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

        def prompt_add(widget, text):
            if self.active_buffer == "P_C":
                self.prompt_command_buffer.insert_at_cursor(text[0])
            elif self.active_buffer == "PS1":
                self.custom_prompt_buffer.insert_at_cursor(text[1])

        def prompt_add_combo(widget, data, dict_p_c, dict_ps1):
            if widget.get_selected() != 0:
                if self.active_buffer == "P_C":
                    self.prompt_command_buffer.insert_at_cursor(dict_p_c[widget.get_selected()])
                elif self.active_buffer == "PS1":
                    self.custom_prompt_buffer.insert_at_cursor(dict_ps1[widget.get_selected()])
                widget.set_selected(0)

        def do_insert_prompt(widget, data, dict1, dict2):
            if widget.get_selected() != 0:
                self.prompt_command_buffer.set_text(dict1[widget.get_selected()])
                self.custom_prompt_buffer.set_text(dict2[widget.get_selected()])
                widget.set_selected(0)

        # GtkButtons
        def do_empty(widget):
            if self.active_buffer == "P_C":
                self.prompt_command_buffer.set_text("")
            elif self.active_buffer == "PS1":
                self.custom_prompt_buffer.set_text("")

        def do_undo(widget):
            if self.active_buffer == "P_C" and self.prompt_command_buffer.get_can_undo():
                self.prompt_command_buffer.undo()
            elif self.active_buffer == "PS1" and self.custom_prompt_buffer.get_can_undo():
                self.custom_prompt_buffer.undo()

        def do_redo(widget):
            if self.active_buffer == "P_C" and self.prompt_command_buffer.get_can_redo():
                self.prompt_command_buffer.redo()
            elif self.active_buffer == "PS1" and self.custom_prompt_buffer.get_can_redo():
                self.custom_prompt_buffer.redo()

        def do_reset(widget):
            self.prompt_command_buffer.set_text("%s" % self.userdefault["Custom"]["command"])
            self.custom_prompt_buffer.set_text("%s" % self.userdefault["Custom"]["prompt"])

        def do_revert(widget):
            self.prompt_command_buffer.set_text("%s" % self.factorydefault["Custom"]["command"])
            self.custom_prompt_buffer.set_text("%s" % self.factorydefault["Custom"]["prompt"])

        WidgetHandler.InitButton("cpb_empty", do_empty)
        WidgetHandler.InitButton("cpb_undo", do_undo)
        WidgetHandler.InitButton("cpb_redo", do_redo)
        WidgetHandler.InitButton("cpb_reset", do_reset)
        WidgetHandler.InitButton("cpb_factory", do_revert)

        # Toolbox
        def do_show_toolbox(widget):
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

        WidgetHandler.InitButton("show_toolbox", do_show_toolbox)

        # Toolbox Buttons
        WidgetHandler.InitButton("username", prompt_add, ("${USER}", "\\u"))
        WidgetHandler.InitButton("hostname", prompt_add, ("${HOSTNAME/.*}", "\\h"))
        WidgetHandler.InitButton("fhostname", prompt_add, ("${HOSTNAME}", "\\H"))
        WidgetHandler.InitButton("time", prompt_add, ("$(date +%H:%M:%S))", "\\t"))
        WidgetHandler.InitButton("date", prompt_add, ("$(date date +%d.%m.%Y))", "\\d"))
        WidgetHandler.InitButton("sign", prompt_add, ("", "\\$"))
        WidgetHandler.InitButton("fworkdir", prompt_add, ("${PWD}", "\\w"))
        WidgetHandler.InitButton("workdir", prompt_add, ("${PWD/*\\/}", "\\W"))
        WidgetHandler.InitButton("euid", prompt_add, ("${EUID}", "${EUID}"))
        WidgetHandler.InitButton("jobs", prompt_add, ("$(jobs -pr))", "\\j"))
        WidgetHandler.InitButton("bang", prompt_add, ("", "\\!"))
        WidgetHandler.InitButton("number", prompt_add, ("", "\\#"))
        WidgetHandler.InitButton("pid", prompt_add, ("${BAHSPID}", "${BASHPID}"))
        WidgetHandler.InitButton("shlvl", prompt_add, ("${SHLVL}", "${SHLVL}"))
        WidgetHandler.InitButton("truncpwd", prompt_add, ("$(truncpwd))", "\\$(truncpwd))"))
        WidgetHandler.InitButton("showsize", prompt_add, ("$(systemkit dirsize))", "\\$(systemkit dirsize))"))
        WidgetHandler.InitButton("countprocesses", prompt_add, ("$(systemkit processes))", "\\$(systemkit processes))"))
        WidgetHandler.InitButton("showuptime", prompt_add, ("$(systemkit uptime))", "\\$(systemkit uptime))"))
        WidgetHandler.InitButton("showtty", prompt_add, ("$(systemkit tty))", "\\$(systemkit tty))"))
        WidgetHandler.InitButton("showcpuload", prompt_add, ("$(systemkit cpuload))", "\\$(systemkit cpuload))"))
        WidgetHandler.InitButton("showseconds", prompt_add, ("${SECONDS}", "${SECONDS}"))
        WidgetHandler.InitButton("showbatteryload", prompt_add, ("$(systemkit battery))", "\\$(systemkit battery))"))
        WidgetHandler.InitButton("showexit", prompt_add, ("${lastexit}", "${lastexit}"))
        WidgetHandler.InitButton("showlastcmd", prompt_add, ("${lastcommand}", "${lastcommand}"))
        WidgetHandler.InitButton("showlastcmd_cut", prompt_add, ("${lastcommandprintable}", "${lastcommandprintable}"))
        WidgetHandler.InitButton("showuser", prompt_add, ("${showuser}", "\\$(showuser))"))

        # Toolbox Comboboxes
        WidgetHandler.InitDropDownButton("showmem", prompt_add_combo, dicts.memory_getters_p_c, dicts.memory_getters_ps1)
        WidgetHandler.InitDropDownButton("showspace", prompt_add_combo, dicts.space_getters_p_c, dicts.space_getters_ps1)
        WidgetHandler.InitDropDownButton("countfiles", prompt_add_combo, dicts.counters_p_c, dicts.counters_ps1)
        WidgetHandler.InitDropDownButton("showload", prompt_add_combo, dicts.load_getters_p_c, dicts.load_getters_ps1)
        WidgetHandler.InitDropDownButton("insert_color", prompt_add_combo, dicts.symbolic_colors_p_c, dicts.symbolic_colors_ps1)
        WidgetHandler.InitDropDownButton("gitkit", prompt_add_combo, dicts.gitkit_getters_p_c, dicts.gitkit_getters_ps1)

        # Default Styles
        WidgetHandler.InitDropDownButton("insert_prompt", do_insert_prompt, prompts.styles_pc, prompts.styles_ps1)
