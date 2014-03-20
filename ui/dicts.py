#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2014 Christopher Bratusek		#
#							#
#########################################################

groups = {
	  "style" : "0",
	  "alias" : "1",
	  "advanced" : "2",
	  "readline" : "3",
	  "vim" : "5",
	  "nano" : "6",
	  "ls" : "7",
	  "custom" : "8",
	 }

color_styles = {
		 0 : "normal",
		 1 : "bright",
		 2 : "dimmed",
		 3 : "inverted",
		 4 : "underlined",
		}
		
man_styles = {
	      0 : "mostlike",
	      1 : "bold",
	      2 : "nebula",
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

color_keys = {
	      1 : "color_user",
	      2 : "color_host",
	      3 : "color_date",
	      4 : "color_time",
	      5 : "color_wdir",
	      6 : "color_font",
	      7 : "color_separator",
	      8 : "color_uptime",
	      9 : "color_ps234",
	     }

colors = {
	   1 : "$black",
	   2 : "$red",
	   3 : "$green",
	   4 : "$yellow",
	   5 : "$blue",
	   6 : "$magenta",
	   7 : "$cyan",
	   8 : "$white",
	   9 : "$coldblue",
	  10 : "$smoothblue",
	  11 : "$iceblue",
	  12 : "$turqoise",
	  13 : "$smoothgreen",
	  14 : "$winered",
	  15 : "$brown",
	  16 : "$silver",
	  17 : "$ocher",
	  18 : "$orange",
	  19 : "$purple",
	  20 : "$pink",
	  21 : "$cream",
	 }

prompt_styles = {
		  0 : "separator",
		  1 : "vector",
		  2 : "clock",
		  3 : "clock-ad",
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

counters = {
	    1 : "\\$(count_files +f)",
	    2 : "\\$(count_files -f)",
	   }

load_getters = {
		1 : "\\$(show_system_load 1)",
		2 : "\\$(show_system_load 10)",
		3 : "\\$(show_system_load 15)",
	       }

memory_getters = {
		  1 : "\\$(show_mem --used)",
		  2 : "\\$(show_mem --free)",
		  3 : "\\$(show_mem --used-percent)",
		  4 : "\\$(show_mem --free-percent)",
		 }

battery_getters = {
		   1 : "\\$(show_battery_load --acpi)",
		   2 : "\\$(show_battery_load --apm)",
		  }

space_getters = {
		  1 : "\\$(show_space --used <device>)",
		  2 : "\\$(show_space --free <device>)",
		  3 : "\\$(show_space --used-percent <device>)",
		  4 : "\\$(show_space --free-percent <device>)",
		 }

symbolic_colors = {
		   1 : "$usercolor",
		   2 : "$hostcolor",
		   3 : "$datecolor",
		   4 : "$timecolor",
		   5 : "$wdircolor",
		   6 : "$fontcolor",
		   7 : "$sepacolor",
		   8 : "$upcolor",
		   9 : "$pscolor",
		  }
