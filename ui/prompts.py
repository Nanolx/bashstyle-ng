#!/usr/bin/env bashstyle --python
#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2015 Christopher Bratusek		#
#							#
#########################################################

empty_pc=r""""""

separator_ps=r"""\\u @ \h | \d | \\t | \\$(truncpwd)$ -> """

vector_ps=r"""\┌( \u @ \h )─( \$(date +%I:%M%P) -:- \$(date +%m)/\$(date +%d) )\└( \$(truncpwd) )·> """

floating_clock_pc=r"""let prompt_x=$(tput cols)-29
tput sc
tput cup 0 ${prompt_x}
echo -n \"[ $(date '+%a, %d %b %y') :: $(date +%T) ]\"
tput rc

PRE_PROMPT_COMMAND"""

floating_clock_ps=r"""[ \u @ \h : \$(truncpwd) ] """

clock_advanced_pc=r"""host=$(echo -n $HOSTNAME | sed -e \"s/[\.].*//\")
dirchar=$(ini_get directory_indicator)
trunc_symbol=$(ini_get pwdcut)
trunc_length=$(($(echo $trunc_symbol | wc -m)-1))

j=4 k=6 l=8 m=10 newPWD=\"${PWD}\" fill=\"\"

let promptsize=$(echo -n \"--( $(whoami) @ $host )---(${PWD})-----\" | wc -c | tr -d \" \")
let fillsize=${COLUMNS}-${promptsize}

while [ \"$fillsize\" -gt \"0\" ]; do
	fill=\"${fill}─\"; let fillsize=${fillsize}-1
done

if [ \"$fillsize\" -lt \"0\" ]; then
	let cutt=${trunc_length}-${fillsize}
	xPWD=\"${trunc_symbol}$(echo -n $PWD | sed -e \"s/\(^.\{$cutt\}\)\(.*\)/\\2/\")\"
	newPWD=\"${xPWD//\//$dirchar}\"
else	newPWD=\"${PWD//\//$dirchar}\"
fi

PRE_PROMPT_COMMAND

_newPWD () {
	echo -e $newPWD
}

echo -en \"\\033[2;$((${COLUMNS}-29))H\"
echo -en \"( $(date +%H:%M) : $(date '+%a, %d %b %y') )────┐\"
echo -en \"\\033[2;${COLUMNS}H\"
i=${LINES}

while [ $i -ge 4 ]; do
   if [[ $i == $j ]]; then
	echo -en \"\\033[$j;$((${COLUMNS}-29))H\"
	echo -en \"( system-load: $(show_system_load 1) )────────\"
   fi
   if [[ $i == $k ]]; then
	echo -en \"\\033[$k;$((${COLUMNS}-29))H\"
	echo -en \"( cpu-load: $(show_cpu_load) )────────────\"
   fi
   if [[ $i == $l ]]; then
	echo -en \"\\033[$l;$((${COLUMNS}-29))H\"
	echo -en \"( ram: $(show_mem --used)mb / $(show_mem --free)mb )─────\"
   fi
   if [[ $i == $m ]]; then
	echo -en \"\\033[$m;$((${COLUMNS}-29))H\"
	echo -en \"( processes: $(count_processes) )──────────\"
   fi
   echo -en \"\\033[$(($i-1));${COLUMNS}H│\"
   let i=$i-1
done
let prompt_line=${LINES}-1"""

clock_advanced_ps=r"""\[\\033[\${prompt_line};0H\]\┌─( \u @ \h )─\${fill}─( \$(_newPWD) )────┘\└─( uptime: \$(show_uptime) : $ )·> """

elite_ps=r"""\┌─[ \u @ \h ]─[ job #\# ]─[ \$(show_tty) ]─[ \$(date +%H:%M:%S): \$(date +%m/%d/%y) : \$(show_uptime) ]\└─[ $ : \$(truncpwd) ]·> """

poweruser_pc=r"""
local one=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\)/\\1/\" -e \"s/ //g\")
local five=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\).*/\\2/\" -e \"s/ //g\")
local diff1_5=$(echo -e \"scale = scale ($one) \\nx=$one - $five\\n if (x>0) {print \\\"up\\\"} else {print \\\"down\\\"}\\n print x \\nquit \\n\" | bc)
loaddiff=\"$(echo -n \"${one}${diff1_5}\" | sed -e 's/down\-/down/g')\"

let files=$(ls -l | grep \"^-\" | wc -l | tr -d \" \")
let hiddenfiles=$(ls -l -d .* | grep \"^-\" | wc -l | tr -d \" \")
let executables=$(ls -l | grep ^-..x | wc -l | tr -d \" \")
let directories=$(ls -l | grep \"^d\" | wc -l | tr -d \" \")
let hiddendirectories=$(ls -l -d .* | grep \"^d\" | wc -l | tr -d \" \")-2
let linktemp=$(ls -l | grep \"^l\" | wc -l | tr -d \" \")

if [ \"$linktemp\" -eq \"0\" ]
then
links=\"\"
else
links=\" ${linktemp}l\"
fi
unset linktemp
let devicetemp=$(ls -l | grep \"^[bc]\" | wc -l | tr -d \" \")

if [ \"$devicetemp\" -eq \"0\" ]
then
devices=\"\"
else
devices=\" ${devicetemp}bc\"
fi
unset devicetemp

PRE_PROMPT_COMMAND"""

poweruser_ps=r"""\[ \$(date +%T) - \$(date +%D) ]
[ \u @ \h ]\ [ \${files}.\${hiddenfiles}-\${executables}x \$(show_size)
${directories}.\${hiddendirectories}d\${links}\${devices} ][ \${loaddiff} ][
$(ps ax | wc -l | sed -e \\\"s: ::g\\\")proc ]\[ \$(truncpwd) ] $ """

dirks_ps=r"""\[ \\t ] \u \$(truncpwd) $ """

dotprompt_ps=r"""\.:[ \u @ \h ]:. .:[ \$(truncpwd) ]:..:[·> """

sepang_ps=r"""\⊏⁅ \u ⁑ \h ⁆⁅ \d ⁑ \\t ⁑ \$(show_uptime) ⁆⊐\⊏⁅ \$(truncpwd) ⁆⊐≻ """

quirk_ps=r"""\ -( \u / \h )-( \$(show_tty) )-( uptime: \$(show_uptime) )-( \$(date +%H:%M)
$(date +%d-%b-%y ) )-( files: \$(count_files +f) / folders: \$(count_files -d) )-\ -< \$(truncpwd) >- """

sputnik_ps=r"""\♦♦( \u @ \h : Space on /: \$(show_space --used /) used of \$(show_space --total /) )♦♦( \$(truncpwd) )♦♦\♦♦( \$(date +%H:%M) → \$(date \\\"+%a, %d %b %y\\\") : uptime : \$(show_uptime) \$ )♦♦ """

ayoli_pc=r"""newPWD=\"${PWD}\"
user=\"whoami\"
host=$(echo -n $HOSTNAME | sed -e \"s/[\.].*//\")
datenow=$(date \"+%a, %d %b %y\")
let promptsize=$(echo -n \"┌( $user @ $host ddd., DD mmm YY)( ${PWD} )┐\" | wc -c | tr -d \" \")

let fillsize=${COLUMNS}-${promptsize}

fill=\"\"
while [ \"$fillsize\" -gt \"0\" ]
do
    fill=\"${fill}─\"
	let fillsize=${fillsize}-1
done
if [ \"$fillsize\" -lt \"0\" ]
then
    let cutt=3-${fillsize}
    newPWD=\"...$(echo -n $PWD | sed -e \"s/\(^.\{$cutt\}\)\(.*\)/\2/\")\"
fi

PRE_PROMPT_COMMAND"""

ayoli_ps=r"""┌─( \u @ \h \$(date \"+%a, %d %b %y\") )─\${fill}─( \$newPWD
)─<└─( \$(date \"+%H:%M\") \$ )─> """
