#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2016 Christopher Bratusek		#
#							#
#########################################################

color_styles = {
		 0 : "normal",
		 1 : "bright",
		 2 : "dimmed",
		 3 : "inverted",
		 4 : "underlined",
		}

less_foreground_colors = {
		   0 : "$lfblack",
		   1 : "$lfred",
		   2 : "$lfgreen",
		   3 : "$lfyellow",
		   4 : "$lfblue",
		   5 : "$lfmagenta",
		   6 : "$lfcyan",
		   7 : "$lfwhite",
		   8 : "$lfcoldblue",
		   9 : "$lfsmoothblue",
		  10 : "$lficeblue",
		  11 : "$lfturqoise",
		  12 : "$lfsmoothgreen",
		  13 : "$lfwinered",
		  14 : "$lfbrown",
		  15 : "$lfsilver",
		  16 : "$lfocher",
		  17 : "$lforange",
		  18 : "$lfpurple",
		  19 : "$lfpink",
		  20 : "$lfcream",
		}

less_background_colors = {
		   0 : "$lbblack",
		   1 : "$lbred",
		   2 : "$lbgreen",
		   3 : "$lbyellow",
		   4 : "$lbblue",
		   5 : "$lbmagenta",
		   6 : "$lbcyan",
		   7 : "$lbwhite",
}

grep_colors = {
		0 : "01;38;5;0",
		1 : "01;38;5;1",
		2 : "01;38;5;2",
		3 : "01;38;5;3",
		4 : "01;38;5;4",
		5 : "01;38;5;5",
		6 : "01;38;5;6",
		7 : "01;38;5;7",
		8 : "01;38;5;33",
		9 : "01;38;5;111",
	       10 : "01;38;5;45",
	       11 : "01;38;5;60",
	       12 : "01;38;5;42",
	       13 : "01;38;5;637",
	       14 : "01;38;5;684",
	       15 : "01;38;5;761",
	       16 : "01;38;5;690",
	       17 : "01;38;5;714",
	       18 : "01;38;5;604",
	       19 : "01;38;5;213",
	       20 : "01;38;5;5344",
	      }

colors = {
	   0 : "$black",
	   1 : "$red",
	   2 : "$green",
	   3 : "$yellow",
	   4 : "$blue",
	   5 : "$magenta",
	   6 : "$cyan",
	   7 : "$white",
	   8 : "$coldblue",
	   9 : "$smoothblue",
	  10 : "$iceblue",
	  11 : "$turqoise",
	  12 : "$smoothgreen",
	  13 : "$winered",
	  14 : "$brown",
	  15 : "$silver",
	  16 : "$ocher",
	  17 : "$orange",
	  18 : "$purple",
	  19 : "$pink",
	  20 : "$cream",
	 }

prompt_styles = {
		  0 : "separator",
		  1 : "vector",
		  2 : "clock",
		  3 : "equinox",
		  4 : "elite",
		  5 : "poweruser",
		  6 : "dirks",
		  7 : "dot_prompt",
		  8 : "sepa_ng",
		  9 : "quirk",
		 10 : "sputnik",
		 11 : "ayoli",
		}

history_types = {
		 0 : "erasedups",
		 1 : "ignoredups",
		 2 : "ignorespace",
		 3 : "ignoreboth",
		}

bell_styles = {
		0 : "audible",
		1 : "visible",
		2 : "none",
	      }

edit_modes = {
	      0 : "emacs",
	      1 : "vi",
	     }

memory_types = {
		0 : "free",
		1 : "used",
		2 : "both",
		3 : "none",
	       }

vim_colors = {
	       0 : "default",
	       1 : "adaryn",
	       2 : "advantage",
	       3 : "desert",
	       4 : "gobo",
	       5 : "impact",
	       6 : "nightshade",
	       7 : "nightwish",
	       8 : "wombat",
	       9 : "asu1dark",
	      10 : "candycode",
	      11 : "dw_orange",
	      12 : "fruit",
	      13 : "relaxedgreen",
	      14 : "tango",
	      15 : "molokai",
	      16 : "vividchalk",
	      17 : "meta5",
	      18 : "woju",
	      19 : "lightning",
	      20 : "papercolor",
	      21 : "solarized",
	     }

vim_foldmethods = {
	       0 : "indent",
	       1 : "marker",
	       2 : "manual",
	       3 : "expr",
	       4 : "syntax",
	       5 : "diff",
	}

nano_colors = {
              0 : "white",
              1 : "black",
              2 : "red",
              3 : "blue",
              4 : "green",
              5 : "yellow",
              6 : "magenta",
              7 : "cyan",
}

ls_colors = {
	      0 : "$lblack",
	      1 : "$lred",
	      2 : "$lgreen",
	      3 : "$lyellow",
	      4 : "$lblue",
	      5 : "$lmagenta",
	      6 : "$lcyan",
	      7 : "$lwhite",
	      8 : "$lcoldblue",
	      9 : "$lsmoothblue",
	     10 : "$liceblue",
	     11 : "$lturqoise",
	     12 : "$lsmoothgreen",
	     13 : "$lwinered",
	     14 : "$lbrown",
	     15 : "$lsilver",
	     16 : "$locher",
	     17 : "$lorange",
	     18 : "$lpurple",
	     19 : "$lpink",
	     20 : "$lcream",
	    }


##### Keybindings #####

keybindings = {
	"undo",
	"upcase_word",
	"capitalize_word",
	"downcase_word",
	"transpose_words",
	"transpose_chars",
	"unix_word_rubout",
	"kill_word",
	"possible_filename_completions",
	"possible_hostname_completions",
	"possible_username_completions",
	"possible_variable_completions",
	"kill_line",
	"unix_line_discard",
	"beginning_of_line",
	"end_of_line",
	"clear_screen",
	"history_search_forward",
	"history_search_backward",
	"complete_path",
	"alias_expand_line",
	"backward_char",
	"backward_delete_char",
	"delete_char",
	"forward_char",
	"backward_word",
	"forward_word",
	"overwrite_mode",
	"menu_complete",
	"menu_complete_backward",
	"rerun_root",
	"backward_kill_line",
	"list_keys"
}


##### IconView Stuff #####

iconview_icons = ["bs-ng-style", "bs-ng-alias", "bs-ng-advanced",
		  "bs-ng-shopts", "bs-ng-git", "bs-ng-readline",
		  "bs-ng-vim", "bs-ng-nano", "bs-ng-ls", "bs-ng-man",
		  "bs-ng-keys", "bs-ng-custom",  "bs-ng-config",
		  "bs-ng-doc", "bs-ng-info" ]

iconview_labels = {
	"bs-ng-style" : _("General Style"),
	"bs-ng-alias" : _("Aliases"),
	"bs-ng-advanced" : _("Advanced"),
	"bs-ng-readline" : _("Readline"),
	"bs-ng-vim" : _("Vi improved"),
	"bs-ng-nano" : _("GNU Nano"),
	"bs-ng-ls" : _("LS colors"),
	"bs-ng-custom" : _("Custom Prompt Builder"),
	"bs-ng-shopts" : _("Shell Options"),
	"bs-ng-git" : _("Git"),
	"bs-ng-info" : _("About BashStyle-NG"),
	"bs-ng-keys" : _("Keybindings"),
	"bs-ng-config" : _("Configuration"),
	"bs-ng-doc" : _("Documentation"),
	"bs-ng-man" : _("Manpage Colors"),
}

notebook_pages = {

	_("General Style") : 1,
	_("Aliases") : 2,
	_("Advanced") : 3,
	_("Readline") : 4,
	_("Vi improved") : 5,
	_("GNU Nano") : 6,
	_("LS colors") : 7,
	_("Manpage Colors") : 15,
	_("Custom Prompt Builder") : 8,
	_("Shell Options") : 10,
	_("Git") : 9,
	_("About BashStyle-NG") : 12,
	_("Keybindings") : 11,
	_("BashStyle-NG StartUp") : 13,
	_("Configuration") : 14,
	_("Documentation") : 0,
}

##### Custom Prompt Builder #####

counters_p_c = {
	    1 : "\\$(systemkit countoverallfiles)",
	    2 : "\\$(systemkit countvisiblefiles)",
	   }

counters_ps1 = {
	    1 : "\\$(systemkit countoverallfiles)",
	    2 : "\\$(systemkit countvisiblefiles)",
	   }

load_getters_p_c = {
		1 : "$(systemkit load1)",
		2 : "$(systemkit load5)",
		3 : "$(systemkit load15)",
	       }

load_getters_ps1 = {
		1 : "\\$(systemkit load1)",
		2 : "\\$(systemkit load5)",
		3 : "\\$(systemkit load15)",
	       }

memory_getters_p_c = {
		  1 : "$(systemkit usedram)",
		  2 : "$(systemkit freeram)",
		  3 : "$(systemkit usedram%)",
		  4 : "$(systemkit freeram%)",
		 }

memory_getters_ps1 = {
		  1 : "\\$(systemkit usedram)",
		  2 : "\\$(systemkit freeram)",
		  3 : "\\$(systemkit usedram%)",
		  4 : "\\$(systemkit freeram%)",
		 }

space_getters_p_c = {
		  1 : "$(systemkit usedspace <device>)",
		  2 : "$(systemkit freespace <device>)",
		  3 : "$(systemkit usedspace% <device>)",
		  4 : "$(systemkit freespace% <device>)",
		 }

space_getters_ps1 = {
		  1 : "\\$(systemkit usedspace <device>)",
		  2 : "\\$(systemkit freespace <device>)",
		  3 : "\\$(systemkit usedspace% <device>)",
		  4 : "\\$(systemkit freespace% <device>)",
		 }

symbolic_colors_p_c = {
		   1 : "${eusercolor}",
		   2 : "${ehostcolor}",
		   3 : "${edatecolor}",
		   4 : "${etimecolor}",
		   5 : "${ewdircolor}",
		   6 : "${efontcolor}",
		   7 : "${esepacolor}",
		   8 : "${eupcolor}",
		   9 : "${epscolor}",
		  10 : "${eps2color}",
		  11 : "${eps3color}",
		  12 : "${eps4color}",
		  }

symbolic_colors_ps1 = {
		   1 : "${usercolor}",
		   2 : "${hostcolor}",
		   3 : "${datecolor}",
		   4 : "${timecolor}",
		   5 : "${wdircolor}",
		   6 : "${fontcolor}",
		   7 : "${sepacolor}",
		   8 : "${upcolor}",
		   9 : "${pscolor}",
		  10 : "${ps2color}",
		  11 : "${ps3color}",
		  12 : "${ps4color}",
		  }
