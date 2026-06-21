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
           'lockfile', 'config', 'widgethandler', 'configui', 'adwaita', 'css',
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

        # GtkEntry
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

        # GtkSwitch
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

        # CustomIconSpinButton
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

        # GtkCheckButton
        WidgetHandler.InitCheckButton("colored_prompts", "Style", "enable_colors")
        WidgetHandler.InitCheckButton("dark_terminal", "Style", "dark_terminal")
        WidgetHandler.InitCheckButton("ls_color", "Style", "colored_ls")
        WidgetHandler.InitCheckButton("random_style", "Style", "random_style")
        WidgetHandler.InitCheckButton("colorshell", "Style", "colorshell")
        WidgetHandler.InitCheckButton("colorshell_reset", "Style", "colorshell_reset")
        WidgetHandler.InitCheckButton("show_files_amount", "Style", "files_amount")
        WidgetHandler.InitCheckButton("show_uptime", "Style", "uptime")
        WidgetHandler.InitCheckButton("show_file_size", "Style", "files_size")
        WidgetHandler.InitCheckButton("show_tty", "Style", "tty")
        WidgetHandler.InitCheckButton("show_processes", "Style", "processes")
        WidgetHandler.InitCheckButton("show_load", "Style", "load")
        WidgetHandler.InitCheckButton("show_battery", "Style", "battery_load")
        WidgetHandler.InitCheckButton("equinox_systemload", "Style", "equinox_systemload")
        WidgetHandler.InitCheckButton("equinox_cpuload", "Style", "equinox_cpuload")
        WidgetHandler.InitCheckButton("equinox_ram", "Style", "equinox_ram")
        WidgetHandler.InitCheckButton("equinox_proc", "Style", "equinox_proc")
        WidgetHandler.InitCheckButton("equinox_lastcmd", "Style", "equinox_lastcmd")
        WidgetHandler.InitCheckButton("equinox_uptime", "Style", "equinox_uptime")
        WidgetHandler.InitCheckButton("equinox_git", "Style", "equinox_git")
        WidgetHandler.InitCheckButton("path_pwd", "Advanced", "path_wd")
        WidgetHandler.InitCheckButton("enable_lscd", "Advanced", "use_lscd")
        WidgetHandler.InitCheckButton("enable_treecd", "Advanced", "use_treecd")
        WidgetHandler.InitCheckButton("customcd_mkdir", "Advanced", "customcd_mkdir")
        WidgetHandler.InitCheckButton("dd_noerror", "Advanced", "dd_noerror")
        WidgetHandler.InitCheckButton("dd_progress", "Advanced", "dd_progress")
        WidgetHandler.InitCheckButton("restore_pwd", "Advanced", "restore_directory")
        WidgetHandler.InitCheckButton("debug_verbose", "Advanced", "debug_verbose")
        WidgetHandler.InitCheckButton("history_sync", "Advanced", "history_sync")
        WidgetHandler.InitCheckButton("history_isolate", "Advanced", "history_isolate")
        WidgetHandler.InitCheckButton("enable_bat", "Advanced", "use_bat")
        WidgetHandler.InitCheckButton("curl_useragent", "Advanced", "curl_useragent")
        WidgetHandler.InitCheckButton("wget_useragent", "Advanced", "wget_useragent")
        WidgetHandler.InitCheckButton("less_options", "Advanced", "less_options")
        WidgetHandler.InitCheckButton("grep_options", "Advanced", "grep_options")
        WidgetHandler.InitCheckButton("completion", "Readline", "completion")
        WidgetHandler.InitCheckButton("ambiguous", "Readline", "ambiguous_show")
        WidgetHandler.InitCheckButton("match_hidden", "Readline", "complete_hidden")
        WidgetHandler.InitCheckButton("ignore_case", "Readline", "ignore_case")
        WidgetHandler.InitCheckButton("completion_hz", "Readline", "complete_horizontal")
        WidgetHandler.InitCheckButton("mark_dirs", "Readline", "mark_directories")
        WidgetHandler.InitCheckButton("mark_symdirs", "Readline", "mark_symbolic_directories")
        WidgetHandler.InitCheckButton("vstats", "Readline", "visible_stats")
        WidgetHandler.InitCheckButton("scroll_hz", "Readline", "scroll_horizontal")
        WidgetHandler.InitCheckButton("modlines", "Readline", "mark_modified")
        WidgetHandler.InitCheckButton("cstats", "Readline", "colored_stats")
        WidgetHandler.InitCheckButton("skipcomptext", "Readline", "skip_completed_text")
        WidgetHandler.InitCheckButton("colored_completion_prefix", "Readline", "colored_completion_prefix")
        WidgetHandler.InitCheckButton("enable_bracketed_paste", "Readline", "enable_bracketed_paste")
        WidgetHandler.InitCheckButton("search_ignore_case", "Readline", "search_ignore_case")
        WidgetHandler.InitCheckButton("histappend", "Shopt", "histappend")
        WidgetHandler.InitCheckButton("cdspell", "Shopt", "cdspell")
        WidgetHandler.InitCheckButton("cdable_vars", "Shopt", "cdable_vars")
        WidgetHandler.InitCheckButton("checkhash", "Shopt", "checkhash")
        WidgetHandler.InitCheckButton("cmdhist", "Shopt", "cmdhist")
        WidgetHandler.InitCheckButton("force_fignore", "Shopt", "force_fignore")
        WidgetHandler.InitCheckButton("histreedit", "Shopt", "histreedit")
        WidgetHandler.InitCheckButton("no_empty_cmd", "Shopt", "no_empty_cmd_completion")
        WidgetHandler.InitCheckButton("autocd", "Shopt", "autocd")
        WidgetHandler.InitCheckButton("checkjobs", "Shopt", "checkjobs")
        WidgetHandler.InitCheckButton("globstar", "Shopt", "globstar")
        WidgetHandler.InitCheckButton("dirspell", "Shopt", "dirspell")
        WidgetHandler.InitCheckButton("direxpand", "Shopt", "direxpand")
        WidgetHandler.InitCheckButton("globasciiranges", "Shopt", "globasciiranges")
        WidgetHandler.InitCheckButton("dotglob", "Shopt", "dotglob")
        WidgetHandler.InitCheckButton("extglob", "Shopt", "extglob")
        WidgetHandler.InitCheckButton("nocaseglob", "Shopt", "nocaseglob")
        WidgetHandler.InitCheckButton("nocasematch", "Shopt", "nocasematch")
        WidgetHandler.InitCheckButton("localvar_inherit", "Shopt", "localvar_inherit")
        WidgetHandler.InitCheckButton("show_editmode", "Readline", "show_editmode")
        WidgetHandler.InitCheckButton("git_color", "Git", "git_color")
        WidgetHandler.InitCheckButton("git_aliases", "Git", "git_aliases")
        WidgetHandler.InitCheckButton("git_ssh_remember", "Git", "git_ssh_remember")
        WidgetHandler.InitCheckButton("vim_backup", "Vim", "vim_backup")
        WidgetHandler.InitCheckButton("vim_jump", "Vim", "jump_back")
        WidgetHandler.InitCheckButton("vim_sline", "Vim", "start_line")
        WidgetHandler.InitCheckButton("vim_expandtab", "Vim", "expandtab")
        WidgetHandler.InitCheckButton("vim_wrap", "Vim", "wrap_line")
        WidgetHandler.InitCheckButton("vim_cd", "Vim", "chdir")
        WidgetHandler.InitCheckButton("vim_indent", "Vim", "filetype_indent")
        WidgetHandler.InitCheckButton("vim_cmd", "Vim", "show_command")
        WidgetHandler.InitCheckButton("vim_match", "Vim", "highlight_matches")
        WidgetHandler.InitCheckButton("vim_syntax", "Vim", "syntax_hilight")
        WidgetHandler.InitCheckButton("vim_bg", "Vim", "dark_background")
        WidgetHandler.InitCheckButton("vim_icase", "Vim", "ignore_case")
        WidgetHandler.InitCheckButton("vim_scase", "Vim", "smart_case")
        WidgetHandler.InitCheckButton("vim_isearch", "Vim", "incremental_search")
        WidgetHandler.InitCheckButton("vim_hilight", "Vim", "highlight_brackets")
        WidgetHandler.InitCheckButton("vim_number", "Vim", "show_lineno")
        WidgetHandler.InitCheckButton("vim_save", "Vim", "autosave")
        WidgetHandler.InitCheckButton("vim_hiline", "Vim", "highlight_line")
        WidgetHandler.InitCheckButton("vim_hicol", "Vim", "highlight_column")
        WidgetHandler.InitCheckButton("vim_ruler", "Vim", "ruler")
        WidgetHandler.InitCheckButton("vim_wildmenu", "Vim", "wildmenu")
        WidgetHandler.InitCheckButton("vim_foldenable", "Vim", "foldenable")
        WidgetHandler.InitCheckButton("nano_backup", "Nano", "nano_backup")
        WidgetHandler.InitCheckButton("nano_const", "Nano", "show_position")
        WidgetHandler.InitCheckButton("nano_line_numbers", "Nano", "line_numbers")
        WidgetHandler.InitCheckButton("nano_indent", "Nano", "auto_indent")
        WidgetHandler.InitCheckButton("nano_colors", "Nano", "syntax_highlight")
        WidgetHandler.InitCheckButton("nano_nohelp", "Nano", "hide_help")
        WidgetHandler.InitCheckButton("nano_case", "Nano", "case_sensitive")
        WidgetHandler.InitCheckButton("nano_boldtext", "Nano", "bold_text")
        WidgetHandler.InitCheckButton("nano_emptyspace", "Nano", "empty_space")
        WidgetHandler.InitCheckButton("nano_history", "Nano", "history")
        WidgetHandler.InitCheckButton("nano_rbdel", "Nano", "rebind_delete")
        WidgetHandler.InitCheckButton("nano_mouse", "Nano", "enable_mouse")
        WidgetHandler.InitCheckButton("nano_logpos",  "Nano", "log_position")
        WidgetHandler.InitCheckButton("nano_nowrap", "Nano", "no_wrap")
        WidgetHandler.InitCheckButton("nano_tabspace", "Nano", "tab_to_spaces")
        WidgetHandler.InitCheckButton("nano_colorui", "Nano", "set_uicolors")

        # Extra steps, does not (yet?) catch the case when 'use_vivid' is enabled,
        # and 'use_lscolors' is toggled afterwards, the other dropdowns sensitivity
        # gets of sync, this does have impact beyond the incorrect state
        self.use_vivid = WidgetHandler.InitCheckButton("use_vivid", "LSColors", "use_vivid")
        self.use_vivid.connect("toggled", WidgetHandler.DisableChilds, None, "ls_colors.grid", ("use_lscolors", "ls_custom", "use_vivid", "vivid_", ), True)
        WidgetHandler.DisableChilds(self.use_vivid, None, "ls_colors.grid", ("use_lscolors", "ls_custom", "use_vivid", "vivid_"), True)

        # GtkDropDown
        WidgetHandler.InitDropDown("prompt_style", "Style", "prompt_style", dicts.prompt_styles)
        WidgetHandler.InitDropDown("color_style", "Style", "color_style", dicts.color_styles)
        WidgetHandler.InitDropDown("color_date", "Style", "color_date", dicts.colors)
        WidgetHandler.InitDropDown("color_font", "Style", "color_font", dicts.colors)
        WidgetHandler.InitDropDown("color_host", "Style", "color_host", dicts.colors)
        WidgetHandler.InitDropDown("color_ps", "Style", "color_ps", dicts.colors)
        WidgetHandler.InitDropDown("color_ps0", "Style", "color_ps0", dicts.colors)
        WidgetHandler.InitDropDown("color_ps2", "Style", "color_ps2", dicts.colors)
        WidgetHandler.InitDropDown("color_ps3", "Style", "color_ps3", dicts.colors)
        WidgetHandler.InitDropDown("color_ps4", "Style", "color_ps4", dicts.colors)
        WidgetHandler.InitDropDown("color_separator", "Style", "color_separator", dicts.colors)
        WidgetHandler.InitDropDown("color_time", "Style", "color_time", dicts.colors)
        WidgetHandler.InitDropDown("color_uptime", "Style", "color_uptime", dicts.colors)
        WidgetHandler.InitDropDown("color_user", "Style", "color_user", dicts.colors)
        WidgetHandler.InitDropDown("color_wdir", "Style", "color_wdir", dicts.colors)
        WidgetHandler.InitDropDown("show_mem", "Style", "mem", dicts.memory_types)
        WidgetHandler.InitDropDown("termcap_mb", "Termcap", "less_blink", dicts.less_foreground_colors)
        WidgetHandler.InitDropDown("termcap_md", "Termcap", "less_bold", dicts.less_foreground_colors)
        WidgetHandler.InitDropDown("termcap_us", "Termcap", "less_underline", dicts.less_foreground_colors)
        WidgetHandler.InitDropDown("termcap_rs", "Termcap", "less_reverse", dicts.less_foreground_colors)
        WidgetHandler.InitDropDown("termcap_mh", "Termcap", "less_dim", dicts.less_foreground_colors)
        WidgetHandler.InitDropDown("termcap_sof", "Termcap", "less_standout_foreground", dicts.less_foreground_colors)
        WidgetHandler.InitDropDown("termcap_sob", "Termcap", "less_standout_background", dicts.less_background_colors)
        WidgetHandler.InitDropDown("history_control", "Advanced", "history_control", dicts.history_types)
        WidgetHandler.InitDropDown("color_cd_banner", "Style", "color_cd_banner", dicts.colors)
        WidgetHandler.InitDropDown("color_cd_empty", "Style", "color_cd_empty", dicts.colors)
        WidgetHandler.InitDropDown("color_cd_mkdir", "Style", "color_cd_mkdir", dicts.colors)
        WidgetHandler.InitDropDown("globsort", "Advanced", "glob_sort", dicts.globsort_modes)
        WidgetHandler.InitDropDown("bat_theme", "Advanced", "bat_theme", dicts.bat_themes)
        WidgetHandler.InitDropDown("bellstyle", "Readline", "bellstyle", dicts.bell_styles)
        WidgetHandler.InitDropDown("editmode", "Readline", "editing_mode", dicts.edit_modes)
        WidgetHandler.InitDropDown("vim_foldmethod", "Vim", "foldmethod", dicts.vim_foldmethods)
        WidgetHandler.InitDropDown("nano_functions_fg", "Nano", "function_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_functions_bg", "Nano", "function_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_keys_fg", "Nano", "key_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_keys_bg", "Nano", "key_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_status_fg", "Nano", "status_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_status_bg", "Nano", "status_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_title_fg", "Nano", "title_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_title_bg", "Nano", "title_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_number_fg", "Nano", "number_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_number_bg", "Nano", "number_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_error_fg", "Nano", "error_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_error_bg", "Nano", "error_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_stripe_fg", "Nano", "stripe_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_stripe_bg", "Nano", "stripe_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("nano_selected_fg", "Nano", "selected_color_fg", dicts.nano_fg_colors)
        WidgetHandler.InitDropDown("nano_selected_bg", "Nano", "selected_color_bg", dicts.nano_bg_colors)
        WidgetHandler.InitDropDown("ls_exec", "LSColors", "exec", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_gen", "LSColors", "generic", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_log", "LSColors", "logs", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_deb", "LSColors", "deb", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_rpm", "LSColors", "rpm", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_dirs", "LSColors", "dirs", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_jpeg", "LSColors", "jpeg", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_png", "LSColors", "png", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_gif", "LSColors", "gif", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_mp3", "LSColors", "mp3", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_ogg", "LSColors", "ogg", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_flac", "LSColors", "flac", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_tar", "LSColors", "tar", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_targz", "LSColors", "targz", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_tarbz2", "LSColors", "tarbz2", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_tarxz", "LSColors", "tarxz", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_zip", "LSColors", "zip", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_rar", "LSColors", "rar", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_link", "LSColors", "link", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_socket", "LSColors", "socket", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_pipe", "LSColors", "pipe", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_blockdev", "LSColors", "blockdev", dicts.ls_colors)
        WidgetHandler.InitDropDown("ls_chardev", "LSColors", "chardev", dicts.ls_colors)
        WidgetHandler.InitDropDown("gcc_color_error", "GCC", "gcc_color_error", dicts.gcc_colors)
        WidgetHandler.InitDropDown("gcc_color_warn", "GCC", "gcc_color_warn", dicts.gcc_colors)
        WidgetHandler.InitDropDown("gcc_color_notes", "GCC", "gcc_color_notes", dicts.gcc_colors)
        WidgetHandler.InitDropDown("gcc_color_caret", "GCC", "gcc_color_caret", dicts.gcc_colors)
        WidgetHandler.InitDropDown("gcc_color_locus", "GCC", "gcc_color_locus", dicts.gcc_colors)
        WidgetHandler.InitDropDown("gcc_color_quote", "GCC", "gcc_color_quote", dicts.gcc_colors)
        WidgetHandler.InitDropDown("grep_color_ms", "GREP", "grep_color_ms", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_mc", "GREP", "grep_color_mc", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_sl", "GREP", "grep_color_sl", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_cx", "GREP", "grep_color_cx", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_fn", "GREP", "grep_color_fn", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_ln", "GREP", "grep_color_ln", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_bn", "GREP", "grep_color_bn", dicts.grep_colors)
        WidgetHandler.InitDropDown("grep_color_se", "GREP", "grep_color_se", dicts.grep_colors)
        WidgetHandler.InitDropDown("vivid_colorscheme", "LSColors", "vivid_colorscheme", dicts.vivid_colorschemes)

        # GtkLabel
        WidgetHandler.InitLabel("about.prefix", os.getenv('BSNG_PREFIX'))
        WidgetHandler.InitLabel("about.version", f"{os.getenv('BSNG_VERSION')} ({os.getenv('BSNG_CODENAME')})")

        # GtkLinkButton
        WidgetHandler.InitLink("about.log", f"file://{os.getenv('HOME')}/.bashstyle-ng.log")

        view = iconbook.IconBook()
        view.InitIconBook()

        cfgui = configui.ConfigUI(config.cfo, config.udc, config.fdc)
        cfgui.InitConfigUI()

        suui = configui.StartupUI(config.cfo, config.udc, config.fdc)
        suui.InitStartupUI()

        keytree = keybindings.KeyTree(config.cfo, config.udc, config.fdc)
        keytree.InitTree()

        pbuilder = promptbuilder.PromptBuilder(config.cfo, config.udc, config.fdc)
        pbuilder.InitPromptBuilder()

        self.bashstyle = gtkbuilder.get_object("bashstyle")
        self.bashstyle.connect("close-request", self.destroy, None)

        self.revert_user = gtkbuilder.get_object("revert_user")
        self.revert_user.connect("clicked", self.restart, False)

        self.restart_btn = gtkbuilder.get_object("restart")
        self.restart_btn.connect("clicked", self.restart, False)

        self.revert_factory = gtkbuilder.get_object("revert_factory")
        self.revert_factory.connect("clicked", self.restart, True)

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

        css.bashstyle_gtk_css()
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

if __name__ == "__main__":
    lock.Check()
    app = BashStyleNG()
    app.run()
