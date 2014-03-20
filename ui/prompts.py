#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2013 Christopher Bratusek		#
#							#
#########################################################

empty_pc=r""

separator_ps=r"\\n\u @ \h | \d | \\t | \\$(trunc_pwd)\n$ -> "

vector_ps=r"\\n┌( \u @ \h )─( \$(date +%I:%M%P) -:- \$(date +%m)/\$(date +%d) )\\n└( \$(trunc_pwd) )·> "

floating_clock_pc=r"let prompt_x=$(tput cols)-29\
\ntput sc\
\ntput cup 0 ${prompt_x}\
\necho -n \"[ $(date '+%a, %d %b %y') :: $(date +%T) ]\"\
\ntput rc"

floating_clock_ps=r"[ \u @ \h : \$(trunc_pwd) ] "

clock_advanced_pc=r"host=$(echo -n $HOSTNAME | sed -e \"s/[\.].*//\")\
\ndirchar=$(ini_get directory_indicator)\
\ntrunc_symbol=$(ini_get pwdcut)\
\ntrunc_length=$(($(echo $trunc_symbol | wc -m)-1))\
\n\
\nj=4 k=6 l=8 m=10 newPWD=\"${PWD}\" fill=\"\"\
\n\
\nlet promptsize=$(echo -n \"--( $(whoami) @ $host )---(${PWD})-----\" | wc -c | tr -d \" \")\
\nlet fillsize=${COLUMNS}-${promptsize}\
\n\
\nwhile [ \"$fillsize\" -gt \"0\" ]; do\
\n	fill=\"${fill}─\"; let fillsize=${fillsize}-1\
\ndone\
\n\
\nif [ \"$fillsize\" -lt \"0\" ]; then\
\n	let cutt=${trunc_length}-${fillsize}\
\n	xPWD=\"${trunc_symbol}$(echo -n $PWD | sed -e \"s/\(^.\{$cutt\}\)\(.*\)/\\2/\")\"\
\n	newPWD=\"${xPWD//\//$dirchar}\"\
\nelse	newPWD=\"${PWD//\//$dirchar}\"\
\nfi\
\n\
\n_newPWD () {\
\n	echo -e $newPWD \
\n}\
\n\
\necho -en \"\\033[2;$((${COLUMNS}-29))H\"\
\necho -en \"( $(date +%H:%M) : $(date '+%a, %d %b %y') )────┐\"\
\necho -en \"\\033[2;${COLUMNS}H\"\
\ni=${LINES}\
\n\
\nwhile [ $i -ge 4 ]; do\
\n   if [[ $i == $j ]]; then\
\n	echo -en \"\\033[$j;$((${COLUMNS}-29))H\"\
\n	echo -en \"( system-load: $(show_system_load 1) )────────\"\
\n   fi\
\n   if [[ $i == $k ]]; then\
\n	echo -en \"\\033[$k;$((${COLUMNS}-29))H\"\
\n	echo -en \"( cpu-load: $(show_cpu_load) )────────────\"\
\n   fi\
\n   if [[ $i == $l ]]; then\
\n	echo -en \"\\033[$l;$((${COLUMNS}-29))H\"\
\n	echo -en \"( ram: $(show_mem --used)mb / $(show_mem --free)mb )─────\"\
\n   fi\
\n   if [[ $i == $m ]]; then\
\n	echo -en \"\\033[$m;$((${COLUMNS}-29))H\"\
\n	echo -en \"( processes: $(count_processes) )──────────\"\
\n   fi\
\n   echo -en \"\\033[$(($i-1));${COLUMNS}H│\"\
\n   let i=$i-1\
\ndone\
\nlet prompt_line=${LINES}-1"

clock_advanced_ps=r"\[\\033[\${prompt_line};0H\]\\n┌─( \u @ \h )─\${fill}─( \$(_newPWD) )────┘\\n└─( uptime: \$(show_uptime) : $ )·> "

elite_ps=r"\\n┌─[ \u @ \h ]─[ job #\# ]─[ \$(show_tty) ]─[ \$(date +%H:%M:%S): \$(date +%m/%d/%y) : \$(show_uptime) ]\\n└─[ $ : \$(trunc_pwd) ]·> "

poweruser_pc=r"\
\nlocal one=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\)/\\1/\" -e \"s/ //g\")\
\nlocal five=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\).*/\\2/\" -e \"s/ //g\")\
\nlocal diff1_5=$(echo -e \"scale = scale ($one) \\nx=$one - $five\\n if (x>0) {print \\\"up\\\"} else {print \\\"down\\\"}\\n print x \\nquit \\n\" | bc)\
\nloaddiff=\"$(echo -n \"${one}${diff1_5}\" | sed -e 's/down\-/down/g')\"\
\
\nlet files=$(ls -l | grep \"^-\" | wc -l | tr -d \" \")\
\nlet hiddenfiles=$(ls -l -d .* | grep \"^-\" | wc -l | tr -d \" \")\
\nlet executables=$(ls -l | grep ^-..x | wc -l | tr -d \" \")\
\nlet directories=$(ls -l | grep \"^d\" | wc -l | tr -d \" \")\
\nlet hiddendirectories=$(ls -l -d .* | grep \"^d\" | wc -l | tr -d \" \")-2\
\nlet linktemp=$(ls -l | grep \"^l\" | wc -l | tr -d \" \")\
\
\nif [ \"$linktemp\" -eq \"0\" ]\
\nthen\
\nlinks=\"\"\
\nelse\
\nlinks=\" ${linktemp}l\"\
\nfi\
\nunset linktemp\
\nlet devicetemp=$(ls -l | grep \"^[bc]\" | wc -l | tr -d \" \")\
\
\nif [ \"$devicetemp\" -eq \"0\" ]\
\nthen\
\ndevices=\"\"\
\nelse\
\ndevices=\" ${devicetemp}bc\"\
\nfi\
\nunset devicetemp"

poweruser_ps=r"\\n[ \$(date +%T) - \$(date +%D) ]\
[ \u @ \h ]\ [ \${files}.\${hiddenfiles}-\${executables}x \$(show_size) \
\${directories}.\${hiddendirectories}d\${links}\${devices} ][ \${loaddiff} ][ \
\$(ps ax | wc -l | sed -e \\\"s: ::g\\\")proc ]\\n[ \$(trunc_pwd) ] $ "

dirks_ps=r"\\n[ \\t ] \u \$(trunc_pwd) $ "

dotprompt_ps=r"\\n.:[ \u @ \h ]:. .:[ \$(trunc_pwd) ]:.\n.:[·> "

sepang_ps=r"\\n⊏⁅ \u ⁑ \h ⁆⁅ \d ⁑ \\t ⁑ \$(show_uptime) ⁆⊐\\n⊏⁅ \$(trunc_pwd) ⁆⊐≻ "

quirk_ps=r"\\n -( \u / \h )-( \$(show_tty) )-( uptime: \$(show_uptime) )-( \$(date +%H:%M) \
\$(date +%d-%b-%y ) )-( files: \$(count_files +f) / folders: \$(count_files -d) )-\\n -< \$(trunc_pwd) >- "

sputnik_ps=r"\\n♦♦( \u @ \h : Space on /: \$(show_space --used /) used of \$(show_space --total /) )♦♦( \$(trunc_pwd) )♦♦\\n♦♦( \$(date +%H:%M) → \$(date \\\"+%a, %d %b %y\\\") : uptime : \$(show_uptime) \$ )♦♦ "

ayoli_pc=r"newPWD=\"${PWD}\"\
\nuser=\"whoami\"\
\nhost=$(echo -n $HOSTNAME | sed -e \"s/[\.].*//\")\
\ndatenow=$(date \"+%a, %d %b %y\")\
\nlet promptsize=$(echo -n \"┌( $user @ $host ddd., DD mmm YY)( ${PWD} )┐\" | wc -c | tr -d \" \")\
\n\
\nlet fillsize=${COLUMNS}-${promptsize}\
\n\
\nfill=\"\"\
\nwhile [ \"$fillsize\" -gt \"0\" ]\
\ndo\
\n    fill=\"${fill}─\"\
\n	let fillsize=${fillsize}-1\
\ndone\
\nif [ \"$fillsize\" -lt \"0\" ]\
\nthen\
\n    let cutt=3-${fillsize}\
\n    newPWD=\"...$(echo -n $PWD | sed -e \"s/\(^.\{$cutt\}\)\(.*\)/\2/\")\"\
\nfi"

ayoli_ps=r"┌─( \u @ \h \$(date \"+%a, %d %b %y\") )─\${fill}─( \$newPWD \
)─<\n└─( \$(date \"+%H:%M\") \$ )─> "
