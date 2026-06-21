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

import gettext
import os
import args

lang = gettext.translation('bashstyle', fallback=True)
lang.install(names=['_'])
args.CmdArgs()

print(_(f"\nBashStyle-NG Version {os.getenv('BSNG_VERSION')} starting"))

MODULES = ['os.path', 'sys', 'string', 'shutil', 'optparse', 'subprocess',
           'lockfile', 'config', 'widgethandler', 'configui', 'adwaita',
           'dicts', 'prompts', 'promptbuilder', 'iconbook', 'keybindings']
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
    from gi.repository import Gtk, Gdk, Gio
except ImportError:
    FAILED.append("Gtk (from gi.repository)")

if FAILED:
    print(_(f"The following modules failed to import: {' '.join(FAILED)}"))
    sys.exit(1)

if adwaita.USE_ADWAITA:
    try:
        if adwaita.USE_KDE:
            os.environ["ADW_DISABLE_PORTAL"] = "1"
        gi.require_version('Adw', '1')
        from gi.repository import Adw
        Adw.init()
    except (ValueError, ImportError):
        Adw = None
        adwaita.USE_ADWAITA = False
else:
    Adw = None

lock = lockfile.LockFile()
config = config.Config()

class BashStyleNG(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="org.nanolx.bashstyle-ng",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        self.is_restarting = False

    def do_activate(self):
        lock.Write()

        config.InitConfig()
        config.LoadConfig()
        config.CheckConfig()

        gtkbuilder = widgethandler.gtkbuilder
        WidgetHandler = widgethandler.WidgetHandler(config.cfo, config.udc, config.fdc)

        if adwaita.USE_ADWAITA:
            self.style_manager = Adw.StyleManager.get_default()
            if adwaita.USE_KDE and adwaita.KDE_DARK:
                self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            elif adwaita.USE_KDE:
                self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            self.gtk_settings = Gtk.Settings.get_default()
            if adwaita.USE_KDE and adwaita.KDE_DARK:
                self.gtk_settings.set_property("gtk-application-prefer-dark-theme", True)
            elif adwaita.USE_KDE:
                self.gtk_settings.set_property("gtk-application-prefer-dark-theme", False)

        WidgetHandler.InitEntry("user_char", "Style", "user_char", 1)
        WidgetHandler.InitEntry("root_char", "Style", "root_char", 1)
        WidgetHandler.InitEntry("return_good", "Style", "return_good", 1)
        WidgetHandler.InitEntry("return_bad", "Style", "return_bad", 1)
        WidgetHandler.InitEntry("return_other", "Style", "return_other", 1)
        WidgetHandler.InitEntry("alias1", "Alias", "alias_one")
        WidgetHandler.InitEntry("alias2", "Alias", "alias_two")
        WidgetHandler.InitEntry("alias3", "Alias", "alias_three")
        WidgetHandler.InitEntry("alias4", "Alias", "alias_four")
        WidgetHandler.InitEntry("alias5", "Alias", "alias_five")
        WidgetHandler.InitEntry("alias6", "Alias", "alias_six")
        WidgetHandler.InitEntry("alias7", "Alias", "alias_seven")
        WidgetHandler.InitEntry("alias8", "Alias", "alias_eight")
        WidgetHandler.InitEntry("alias9", "Alias", "alias_nine")
        WidgetHandler.InitEntry("history_blacklist", "Advanced", "history_ignore")
        WidgetHandler.InitEntry("separator", "Advanced", "separator", 1)
        WidgetHandler.InitEntry("ps0", "Advanced", "ps0")
        WidgetHandler.InitEntry("ps2", "Advanced", "ps2")
        WidgetHandler.InitEntry("ps3", "Advanced", "ps3")
        WidgetHandler.InitEntry("ps4", "Advanced", "ps4")
        WidgetHandler.InitEntry("pwd_cutter", "Advanced", "pwdcut", 1)
        WidgetHandler.InitEntry("cdpath", "Advanced", "cdpath")
        WidgetHandler.InitEntry("completion_blacklist", "Advanced", "completion_ignore")
        WidgetHandler.InitEntry("fcedit", "Advanced", "fcedit")
        WidgetHandler.InitEntry("welcome", "Advanced", "welcome_message")
        WidgetHandler.InitEntry("path", "Advanced", "path")
        WidgetHandler.InitEntry("history_timeformat", "Advanced", "history_timeformat")
        WidgetHandler.InitEntry("dirchar", "Advanced", "directory_indicator", 1)
        WidgetHandler.InitEntry("lscd_options", "Advanced", "lscd_opts")
        WidgetHandler.InitEntry("treecd_options", "Advanced", "treecd_opts")
        WidgetHandler.InitEntry("birthday", "Advanced", "user_birthday", 5)
        WidgetHandler.InitEntry("execignore", "Advanced", "exec_ignore")
        WidgetHandler.InitEntry("globignore", "Advanced", "glob_ignore")
        WidgetHandler.InitEntry("curl_useragent_string", "Advanced", "curl_useragent_string")
        WidgetHandler.InitEntry("less_options_string", "Advanced", "less_options_string")
        WidgetHandler.InitEntry("wget_useragent_string", "Advanced", "wget_useragent_string")
        WidgetHandler.InitEntry("grep_options_string", "Advanced", "grep_options_string")
        WidgetHandler.InitEntry("vi_cmd_string", "Readline", "vi_cmd_mode_string", 1)
        WidgetHandler.InitEntry("vi_ins_string", "Readline", "vi_ins_mode_string", 1)
        WidgetHandler.InitEntry("emacs_string", "Readline", "emacs_mode_string", 1)
        WidgetHandler.InitEntry("git_user", "Git", "git_user_name")
        WidgetHandler.InitEntry("git_mail", "Git", "git_user_mail")
        WidgetHandler.InitEntry("git_editor", "Git", "git_editor")
        WidgetHandler.InitEntry("git_signkey", "Git", "git_signkey")
        WidgetHandler.InitEntry("git_ssh_keyfile", "Git", "git_ssh_keyfile")
        WidgetHandler.InitEntry("vim_rulerformat", "Vim", "rulerformat")
        WidgetHandler.InitEntry("ls_custom", "LSColors", "custom")

        WidgetHandler.InitSwitch("use_bashstyle", "Style", "use_bashstyle", "style.grid")
        WidgetHandler.InitSwitch("termcap_colors", "Termcap", "less_termcap_color", "termcap.grid")
        WidgetHandler.InitSwitch("use_readline", "Readline", "use_readlinecfg", "readline.grid")
        WidgetHandler.InitSwitch("use_git", "Git", "use_gitcfg", "git.grid")
        WidgetHandler.InitSwitch("use_vim", "Vim", "use_vimcfg", "vim.grid")
        WidgetHandler.InitSwitch("use_nano", "Nano", "use_nanocfg", "nano.grid")
        WidgetHandler.InitSwitch("use_lscolors", "LSColors", "use_lscolors", "ls_colors.grid")
        WidgetHandler.InitSwitch("gcc_colors_enable", "GCC", "use_gcc_colors", "gcc.grid")
        WidgetHandler.InitSwitch("grep_colors_enable", "GREP", "use_grep_colors", "grep.grid")
        WidgetHandler.InitSwitch("use_customprompt", "Custom", "use_custom_prompt", "cpb.grid")

        WidgetHandler.InitIconSpinButton("history_size_label", "history_size", "Advanced", "history_size", 100, 1000000)
        WidgetHandler.InitIconSpinButton("pwdlen_label", "pwd_len", "Advanced", "pwdlength", 10, 100)
        WidgetHandler.InitIconSpinButton("timeout_label", "timeout", "Advanced", "timeout", 0, 10000)
        WidgetHandler.InitIconSpinButton("bat_tabwidth_label", "bat_tabwidth", "Advanced", "bat_tabwidth", 2, 16)
        WidgetHandler.InitIconSpinButton("query_items_label", "query_items", "Readline", "query_items", 10, 10000)
        WidgetHandler.InitIconSpinButton("git_ssh_timeout_label", "git_ssh_timeout", "Git", "git_ssh_timeout", 60, 3600)
        WidgetHandler.InitIconSpinButton("vim_tabstop_label", "vim_tabstop", "Vim", "tab_length", 2, 16)
        WidgetHandler.InitIconSpinButton("vim_autowrap_label", "vim_autowrap", "Vim", "wrap_length", 40, 500)
        WidgetHandler.InitIconSpinButton("vim_foldlevelstart_label", "vim_foldlevelstart", "Vim", "foldlevelstart", 4, 32)
        WidgetHandler.InitIconSpinButton("vim_foldnestmax_label", "vim_foldnestmax", "Vim", "foldnestmax", 4, 32)
        WidgetHandler.InitIconSpinButton("nano_guide_stripe_label", "nano_guide_stripe", "Nano", "guide_stripe", 40, 500)
        WidgetHandler.InitIconSpinButton("nano_tabwidth_label", "nano_tabwidth", "Nano", "tab_size", 4, 16)

        WidgetHandler.InitWidget("colored_prompts", "Style", "enable_colors", "bool", None)
        WidgetHandler.InitWidget("dark_terminal", "Style", "dark_terminal", "bool", None)
        WidgetHandler.InitWidget("ls_color", "Style", "colored_ls", "bool", None)
        WidgetHandler.InitWidget("random_style", "Style", "random_style", "bool", None)
        WidgetHandler.InitWidget("prompt_style", "Style", "prompt_style", "combo", dicts.prompt_styles)
        WidgetHandler.InitWidget("color_style", "Style", "color_style", "combo", dicts.color_styles)
        WidgetHandler.InitWidget("colorshell", "Style", "colorshell", "bool", None)
        WidgetHandler.InitWidget("colorshell_reset", "Style", "colorshell_reset", "bool", None)
        WidgetHandler.InitWidget("color_date", "Style", "color_date", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_font", "Style", "color_font", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_host", "Style", "color_host", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_ps", "Style", "color_ps", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_ps0", "Style", "color_ps0", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_ps2", "Style", "color_ps2", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_ps3", "Style", "color_ps3", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_ps4", "Style", "color_ps4", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_separator", "Style", "color_separator", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_time", "Style", "color_time", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_uptime", "Style", "color_uptime", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_user", "Style", "color_user", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_wdir", "Style", "color_wdir", "combo", dicts.colors)

        WidgetHandler.InitWidget("show_files_amount", "Style", "files_amount", "bool", None)
        WidgetHandler.InitWidget("show_uptime", "Style", "uptime", "bool", None)
        WidgetHandler.InitWidget("show_file_size", "Style", "files_size", "bool", None)
        WidgetHandler.InitWidget("show_tty", "Style", "tty", "bool", None)
        WidgetHandler.InitWidget("show_processes", "Style", "processes", "bool", None)
        WidgetHandler.InitWidget("show_load", "Style", "load", "bool", None)
        WidgetHandler.InitWidget("show_battery", "Style", "battery_load", "bool", None)
        WidgetHandler.InitWidget("show_mem", "Style", "mem", "combo", dicts.memory_types)

        WidgetHandler.InitWidget("equinox_systemload", "Style", "equinox_systemload", "bool", None)
        WidgetHandler.InitWidget("equinox_cpuload", "Style", "equinox_cpuload", "bool", None)
        WidgetHandler.InitWidget("equinox_ram", "Style", "equinox_ram", "bool", None)
        WidgetHandler.InitWidget("equinox_proc", "Style", "equinox_proc", "bool", None)
        WidgetHandler.InitWidget("equinox_lastcmd", "Style", "equinox_lastcmd", "bool", None)
        WidgetHandler.InitWidget("equinox_uptime", "Style", "equinox_uptime", "bool", None)
        WidgetHandler.InitWidget("equinox_git", "Style", "equinox_git", "bool", None)

        WidgetHandler.InitWidget("termcap_mb", "Termcap", "less_blink", "combo", dicts.less_foreground_colors)
        WidgetHandler.InitWidget("termcap_md", "Termcap", "less_bold", "combo", dicts.less_foreground_colors)
        WidgetHandler.InitWidget("termcap_us", "Termcap", "less_underline", "combo", dicts.less_foreground_colors)
        WidgetHandler.InitWidget("termcap_rs", "Termcap", "less_reverse", "combo", dicts.less_foreground_colors)
        WidgetHandler.InitWidget("termcap_mh", "Termcap", "less_dim", "combo", dicts.less_foreground_colors)
        WidgetHandler.InitWidget("termcap_sof", "Termcap", "less_standout_foreground", "combo", dicts.less_foreground_colors)
        WidgetHandler.InitWidget("termcap_sob", "Termcap", "less_standout_background", "combo", dicts.less_background_colors)

        WidgetHandler.InitWidget("path_pwd", "Advanced", "path_wd", "bool", None)
        WidgetHandler.InitWidget("history_control", "Advanced", "history_control", "combo", dicts.history_types)

        WidgetHandler.InitWidget("enable_lscd", "Advanced", "use_lscd", "bool", None)
        WidgetHandler.InitWidget("enable_treecd", "Advanced", "use_treecd", "bool", None)
        WidgetHandler.InitWidget("customcd_mkdir", "Advanced", "customcd_mkdir", "bool", None)

        WidgetHandler.InitWidget("color_cd_banner", "Style", "color_cd_banner", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_cd_empty", "Style", "color_cd_empty", "combo", dicts.colors)
        WidgetHandler.InitWidget("color_cd_mkdir", "Style", "color_cd_mkdir", "combo", dicts.colors)

        WidgetHandler.InitWidget("dd_noerror", "Advanced", "dd_noerror", "bool", None)
        WidgetHandler.InitWidget("dd_progress", "Advanced", "dd_progress", "bool", None)
        WidgetHandler.InitWidget("restore_pwd", "Advanced", "restore_directory", "bool", None)
        WidgetHandler.InitWidget("debug_verbose", "Advanced", "debug_verbose", "bool", None)
        WidgetHandler.InitWidget("history_sync", "Advanced", "history_sync", "bool", None)
        WidgetHandler.InitWidget("globsort", "Advanced", "glob_sort", "combo", dicts.globsort_modes)
        WidgetHandler.InitWidget("history_isolate", "Advanced", "history_isolate", "bool", None)
        WidgetHandler.InitWidget("enable_bat", "Advanced", "use_bat", "bool", None)
        WidgetHandler.InitWidget("bat_theme", "Advanced", "bat_theme", "combo", dicts.bat_themes)
        WidgetHandler.InitWidget("curl_useragent", "Advanced", "curl_useragent", "bool", None)
        WidgetHandler.InitWidget("wget_useragent", "Advanced", "wget_useragent", "bool", None)
        WidgetHandler.InitWidget("less_options", "Advanced", "less_options", "bool", None)
        WidgetHandler.InitWidget("grep_options", "Advanced", "grep_options", "bool", None)

        WidgetHandler.InitWidget("completion", "Readline", "completion", "bool", None)
        WidgetHandler.InitWidget("ambiguous", "Readline", "ambiguous_show", "bool", None)
        WidgetHandler.InitWidget("match_hidden", "Readline", "complete_hidden", "bool", None)
        WidgetHandler.InitWidget("ignore_case", "Readline", "ignore_case", "bool", None)
        WidgetHandler.InitWidget("completion_hz", "Readline", "complete_horizontal", "bool", None)
        WidgetHandler.InitWidget("mark_dirs", "Readline", "mark_directories", "bool", None)
        WidgetHandler.InitWidget("mark_symdirs", "Readline", "mark_symbolic_directories", "bool", None)
        WidgetHandler.InitWidget("vstats", "Readline", "visible_stats", "bool", None)
        WidgetHandler.InitWidget("scroll_hz", "Readline", "scroll_horizontal", "bool", None)
        WidgetHandler.InitWidget("modlines", "Readline", "mark_modified", "bool", None)
        WidgetHandler.InitWidget("bellstyle", "Readline", "bellstyle", "combo", dicts.bell_styles)
        WidgetHandler.InitWidget("editmode", "Readline", "editing_mode", "combo", dicts.edit_modes)
        WidgetHandler.InitWidget("show_editmode", "Readline", "show_editmode", "bool", None)
        WidgetHandler.InitWidget("cstats", "Readline", "colored_stats", "bool", None)
        WidgetHandler.InitWidget("skipcomptext", "Readline", "skip_completed_text", "bool", None)
        WidgetHandler.InitWidget("colored_completion_prefix", "Readline", "colored_completion_prefix", "bool", None)
        WidgetHandler.InitWidget("enable_bracketed_paste", "Readline", "enable_bracketed_paste", "bool", None)
        WidgetHandler.InitWidget("search_ignore_case", "Readline", "search_ignore_case", "bool", None)

        WidgetHandler.InitWidget("histappend", "Shopt", "histappend", "bool", None)
        WidgetHandler.InitWidget("cdspell", "Shopt", "cdspell", "bool", None)
        WidgetHandler.InitWidget("cdable_vars", "Shopt", "cdable_vars", "bool", None)
        WidgetHandler.InitWidget("checkhash", "Shopt", "checkhash", "bool", None)
        WidgetHandler.InitWidget("cmdhist", "Shopt", "cmdhist", "bool", None)
        WidgetHandler.InitWidget("force_fignore", "Shopt", "force_fignore", "bool", None)
        WidgetHandler.InitWidget("histreedit", "Shopt", "histreedit", "bool", None)
        WidgetHandler.InitWidget("no_empty_cmd", "Shopt", "no_empty_cmd_completion", "bool", None)
        WidgetHandler.InitWidget("autocd", "Shopt", "autocd", "bool", None)
        WidgetHandler.InitWidget("checkjobs", "Shopt", "checkjobs", "bool", None)
        WidgetHandler.InitWidget("globstar", "Shopt", "globstar", "bool", None)
        WidgetHandler.InitWidget("dirspell", "Shopt", "dirspell", "bool", None)
        WidgetHandler.InitWidget("direxpand", "Shopt", "direxpand", "bool", None)
        WidgetHandler.InitWidget("globasciiranges", "Shopt", "globasciiranges", "bool", None)
        WidgetHandler.InitWidget("dotglob", "Shopt", "dotglob", "bool", None)
        WidgetHandler.InitWidget("extglob", "Shopt", "extglob", "bool", None)
        WidgetHandler.InitWidget("nocaseglob", "Shopt", "nocaseglob", "bool", None)
        WidgetHandler.InitWidget("nocasematch", "Shopt", "nocasematch", "bool", None)
        WidgetHandler.InitWidget("localvar_inherit", "Shopt", "localvar_inherit", "bool", None)

        WidgetHandler.InitWidget("git_color", "Git", "git_color", "bool", None)
        WidgetHandler.InitWidget("git_aliases", "Git", "git_aliases", "bool", None)
        WidgetHandler.InitWidget("git_ssh_remember", "Git", "git_ssh_remember", "bool", None)

        WidgetHandler.InitWidget("vim_backup", "Vim", "vim_backup", "bool", None)
        WidgetHandler.InitWidget("vim_jump", "Vim", "jump_back", "bool", None)
        WidgetHandler.InitWidget("vim_sline", "Vim", "start_line", "bool", None)
        WidgetHandler.InitWidget("vim_expandtab", "Vim", "expandtab", "bool", None)
        WidgetHandler.InitWidget("vim_wrap", "Vim", "wrap_line", "bool", None)
        WidgetHandler.InitWidget("vim_cd", "Vim", "chdir", "bool", None)
        WidgetHandler.InitWidget("vim_indent", "Vim", "filetype_indent", "bool", None)
        WidgetHandler.InitWidget("vim_cmd", "Vim", "show_command", "bool", None)
        WidgetHandler.InitWidget("vim_match", "Vim", "highlight_matches", "bool", None)
        WidgetHandler.InitWidget("vim_syntax", "Vim", "syntax_hilight", "bool", None)
        WidgetHandler.InitWidget("vim_bg", "Vim", "dark_background", "bool", None)
        WidgetHandler.InitWidget("vim_icase", "Vim", "ignore_case", "bool", None)
        WidgetHandler.InitWidget("vim_scase", "Vim", "smart_case", "bool", None)
        WidgetHandler.InitWidget("vim_isearch", "Vim", "incremental_search", "bool", None)
        WidgetHandler.InitWidget("vim_hilight", "Vim", "highlight_brackets", "bool", None)
        WidgetHandler.InitWidget("vim_number", "Vim", "show_lineno", "bool", None)
        WidgetHandler.InitWidget("vim_save", "Vim", "autosave", "bool", None)
        WidgetHandler.InitWidget("vim_hiline", "Vim", "highlight_line", "bool", None)
        WidgetHandler.InitWidget("vim_hicol", "Vim", "highlight_column", "bool", None)
        WidgetHandler.InitWidget("vim_ruler", "Vim", "ruler", "bool", None)
        WidgetHandler.InitWidget("vim_wildmenu", "Vim", "wildmenu", "bool", None)
        WidgetHandler.InitWidget("vim_foldenable", "Vim", "foldenable", "bool", None)
        WidgetHandler.InitWidget("vim_foldmethod", "Vim", "foldmethod", "combo", dicts.vim_foldmethods)

        WidgetHandler.InitWidget("nano_backup", "Nano", "nano_backup", "bool", None)
        WidgetHandler.InitWidget("nano_const", "Nano", "show_position", "bool", None)
        WidgetHandler.InitWidget("nano_line_numbers", "Nano", "line_numbers", "bool", None)
        WidgetHandler.InitWidget("nano_indent", "Nano", "auto_indent", "bool", None)
        WidgetHandler.InitWidget("nano_colors", "Nano", "syntax_highlight", "bool", None)
        WidgetHandler.InitWidget("nano_nohelp", "Nano", "hide_help", "bool", None)
        WidgetHandler.InitWidget("nano_case", "Nano", "case_sensitive", "bool", None)
        WidgetHandler.InitWidget("nano_boldtext", "Nano", "bold_text", "bool", None)
        WidgetHandler.InitWidget("nano_emptyspace", "Nano", "empty_space", "bool", None)
        WidgetHandler.InitWidget("nano_history", "Nano", "history", "bool", None)
        WidgetHandler.InitWidget("nano_rbdel", "Nano", "rebind_delete", "bool", None)
        WidgetHandler.InitWidget("nano_mouse", "Nano", "enable_mouse",  "bool", None)
        WidgetHandler.InitWidget("nano_logpos",  "Nano", "log_position", "bool", None)
        WidgetHandler.InitWidget("nano_nowrap", "Nano", "no_wrap", "bool", None)
        WidgetHandler.InitWidget("nano_tabspace", "Nano", "tab_to_spaces", "bool", None)
        WidgetHandler.InitWidget("nano_colorui", "Nano", "set_uicolors", "bool", None)
        WidgetHandler.InitWidget("nano_functions_fg", "Nano", "function_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_functions_bg", "Nano", "function_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_keys_fg", "Nano", "key_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_keys_bg", "Nano", "key_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_status_fg", "Nano", "status_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_status_bg", "Nano", "status_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_title_fg", "Nano", "title_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_title_bg", "Nano", "title_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_number_fg", "Nano", "number_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_number_bg", "Nano", "number_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_error_fg", "Nano", "error_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_error_bg", "Nano", "error_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_stripe_fg", "Nano", "stripe_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_stripe_bg", "Nano", "stripe_color_bg", "combo", dicts.nano_bg_colors)
        WidgetHandler.InitWidget("nano_selected_fg", "Nano", "selected_color_fg", "combo", dicts.nano_fg_colors)
        WidgetHandler.InitWidget("nano_selected_bg", "Nano", "selected_color_bg", "combo", dicts.nano_bg_colors)

        WidgetHandler.InitWidget("ls_exec", "LSColors", "exec", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_gen", "LSColors", "generic", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_log", "LSColors", "logs", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_deb", "LSColors", "deb", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_rpm", "LSColors", "rpm", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_dirs", "LSColors", "dirs", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_jpeg", "LSColors", "jpeg", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_png", "LSColors", "png", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_gif", "LSColors", "gif", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_mp3", "LSColors", "mp3", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_ogg", "LSColors", "ogg", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_flac", "LSColors", "flac", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_tar", "LSColors", "tar", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_targz", "LSColors", "targz", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_tarbz2", "LSColors", "tarbz2", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_tarxz", "LSColors", "tarxz", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_zip", "LSColors", "zip", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_rar", "LSColors", "rar", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_link", "LSColors", "link", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_socket", "LSColors", "socket", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_pipe", "LSColors", "pipe", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_blockdev", "LSColors", "blockdev", "combo", dicts.ls_colors)
        WidgetHandler.InitWidget("ls_chardev", "LSColors", "chardev", "combo", dicts.ls_colors)

        self.use_vivid = WidgetHandler.InitWidget("use_vivid", "LSColors", "use_vivid", "bool", None)
        # This gets out of sync when use_vivid is toggled, but then use_lscolors gets toggled aswell
        # This could be fixed by custom DisableChilds for both, but is difficult to implement in a generic funtion
        # So for now we live with that rare corner case, also it's only for sensitivity of widgets, there's no
        # downside for the user interaction for issue with the configuration
        self.use_vivid.connect("toggled", WidgetHandler.DisableChilds, None, "ls_colors.grid", ("use_lscolors", "ls_custom", "use_vivid", "vivid_", ), True)
        WidgetHandler.DisableChilds(self.use_vivid, None, "ls_colors.grid", ("use_lscolors", "ls_custom", "use_vivid", "vivid_"), True)
        WidgetHandler.InitWidget("vivid_colorscheme", "LSColors", "vivid_colorscheme", "combo", dicts.vivid_colorschemes)

        WidgetHandler.InitWidget("gcc_color_error", "GCC", "gcc_color_error", "combo", dicts.gcc_colors)
        WidgetHandler.InitWidget("gcc_color_warn", "GCC", "gcc_color_warn", "combo", dicts.gcc_colors)
        WidgetHandler.InitWidget("gcc_color_notes", "GCC", "gcc_color_notes", "combo", dicts.gcc_colors)
        WidgetHandler.InitWidget("gcc_color_caret", "GCC", "gcc_color_caret", "combo", dicts.gcc_colors)
        WidgetHandler.InitWidget("gcc_color_locus", "GCC", "gcc_color_locus", "combo", dicts.gcc_colors)
        WidgetHandler.InitWidget("gcc_color_quote", "GCC", "gcc_color_quote", "combo", dicts.gcc_colors)

        WidgetHandler.InitWidget("grep_color_ms", "GREP", "grep_color_ms", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_mc", "GREP", "grep_color_mc", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_sl", "GREP", "grep_color_sl", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_cx", "GREP", "grep_color_cx", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_fn", "GREP", "grep_color_fn", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_ln", "GREP", "grep_color_ln", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_bn", "GREP", "grep_color_bn", "combo", dicts.grep_colors)
        WidgetHandler.InitWidget("grep_color_se", "GREP", "grep_color_se", "combo", dicts.grep_colors)

        keytree = keybindings.KeyTree(config.cfo, config.udc, config.fdc)
        keytree.InitTree()

        pbuilder = promptbuilder.PromptBuilder(config.cfo, config.udc, config.fdc)
        pbuilder.InitPromptBuilder()

        def on_theme_changed(self, manager, pspec):
            update_source_scheme(self)

        def update_source_scheme(self):
            if adwaita.USE_ADWAITA:
                is_dark = self.style_manager.get_dark()
            else:
                is_dark = self.gtk_settings.get_property("gtk-application-prefer-dark-theme")
            if is_dark:
                scheme = pbuilder.scheme_manager.get_scheme("oblivion")
            else:
                scheme = pbuilder.scheme_manager.get_scheme("tango")
            if scheme:
                pbuilder.prompt_command_buffer.set_style_scheme(scheme)
                pbuilder.custom_prompt_buffer.set_style_scheme(scheme)

        if adwaita.USE_ADWAITA:
            self.style_manager.connect("notify::dark", on_theme_changed)
        else:
            self.gtk_settings.connect("notify::gtk-application-prefer-dark-theme", on_theme_changed)

        update_source_scheme(self)

        view = iconbook.IconBook()
        view.InitIconBook()

        cfgui = configui.ConfigUI(config.cfo, config.udc, config.fdc)
        cfgui.InitConfigUI()

        WidgetHandler.InitWidget("about.prefix", None, os.getenv('BSNG_PREFIX'), "label", None)
        WidgetHandler.InitWidget("about.version", None, f"{os.getenv('BSNG_VERSION')} ({os.getenv('BSNG_CODENAME')})", "label", None)
        WidgetHandler.InitWidget("about.log", None, f"file://{os.getenv('HOME')}/.bashstyle-ng.log", "link", None)

        suui = configui.StartupUI(config.cfo, config.udc, config.fdc)
        suui.InitStartupUI()

        self.bashstyle = gtkbuilder.get_object("bashstyle")

        self.revert_user = gtkbuilder.get_object("revert_user")
        self.revert_user.connect("clicked", self.restart, False)

        self.restart_btn = gtkbuilder.get_object("restart")
        self.restart_btn.connect("clicked", self.restart, False)

        self.revert_factory = gtkbuilder.get_object("revert_factory")
        self.revert_factory.connect("clicked", self.restart, True)

        self.bashstyle.connect("close-request", self.destroy, None)
        self.bashstyle_gtk_css()
        self.bashstyle.set_application(self)
        self.bashstyle.present()

    def destroy(self, widget, data):
        if self.is_restarting:
            return False
        config.WriteConfig()
        lock.Remove()

    def restart(self, widget, reset):
        self.is_restarting = True
        executable = sys.executable
        args = sys.argv
        if reset:
            config.ResetConfig(False)
        subprocess.Popen([executable] + args, close_fds=True)
        self.quit()

    def bashstyle_gtk_css(self):
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

if __name__ == "__main__":
    lock.Check()
    app = BashStyleNG()
    app.run()
