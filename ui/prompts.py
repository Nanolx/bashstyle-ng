#coding=utf-8
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3		#
#							#
# Copyright 2007 - 2018 Christopher Bratusek		#
#							#
#########################################################

empty_pc=r""""""

separator_ps=r"""\\u @ \h | \d | \\t | \$(truncpwd) | \$(showuser) -> """

vector_ps=r"""\┌( \u @ \h )─( \$(date +%I:%M%P) -:- \$(date +%m)/\$(date +%d) )\└( \$(truncpwd) )·> """

clock_pc=r"""let prompt_x=$(tput cols)-29
tput sc
tput cup 0 ${prompt_x}
echo -n \"[ $(date '+%a, %d %b %y') :: $(date +%T) ]\"
tput rc"""

clock_ps=r"""[ \u @ \h : \$(truncpwd) ] """

equinox_pc=r"""host=${HOSTNAME/.*}
[[ ! ${dirchar} ]] && dirchar="/"
[[ ! ${trunc_symbol} ]] && trunc_symbol="«"
[[ ! ${trunc_length} ]] && trunc_length=1

j=4 k=6 l=8 m=10 n=12 newPWD=\"${PWD}\" fill=\"\"

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

_newPWD () {
	echo -e $newPWD
}

echo -en \"\\033[2;$((${COLUMNS}-29))H\"
echo -en \"( $(date +%H:%M) : $(date '+%a, %d %b %y') )────┐\"
echo -en \"\\033[3;${COLUMNS}H│\"
i=${LINES}

[[ ${i} -ge 16 ]] && while [ ${i} -ge 4 ]
do
	case ${i} in
		${j} )
			echo -en \"\\033[${j};$((${COLUMNS}-29))H\"
			echo -en \"( system-load: $(systemkit load1) )────────┤\"
		;;
		${k} )
			echo -en \"\\033[${k};$((${COLUMNS}-29))H\"
			echo -en \"( cpu-load: $(systemkit cpuload) )────────────┤\"
		;;
		${l} )
			echo -en \"\\033[${l};$((${COLUMNS}-29))H\"
			echo -en \"( ram: $(systemkit usedram)mb / $(systemkit freeram)mb )─────┤\"
		;;
		${m} )
			echo -en \"\\033[${m};$((${COLUMNS}-29))H\"
			echo -en \"( processes:${epscolor} $(systemkit processes) )──────────┤\"
		;;
		${n} )
			echo -en \"\\033[${n};$((${COLUMNS}-29))H\"
			if [ ${lastexit} -eq 0 ]; then
				echo -en \"( ✔: ${lastcommandprintable} )─┤\"
			elif [ ${lastexit} -eq 141 ]; then
				echo -en \"( ⊘: ${lastcommandprintable} )─┤\"
			else
				echo -en \"( ✘: ${lastcommandprintable} )─┤\"
			fi
		;;
		* )
			echo -en \"\\033[$((${i}));${COLUMNS}H│\"
		;;
	esac
	let i=${i}-1
done
let prompt_line=${LINES}-1"""

equinox_ps=r"""\[\\033[\${prompt_line};0H\]\┌─( \u @ \h )─\${fill}─( \$(_newPWD) )────┘\└─( uptime: \$(systemkit uptime) : \$(showuser) )·> """

elite_ps=r"""\┌─[ \u @ \h ]─[ job #\# ]─[ \$(systemkit tty) ]─[ \$(date +%H:%M:%S): \$(date +%m/%d/%y) : \$(systemkit uptime) ]\└─[ \$(showuser) : \$(truncpwd) ]·> """

poweruser_pc=r"""
local one=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\)/\\1/\" -e \"s/ //g\")
local five=$(uptime | sed -e \"s/.*load average: \(.*\...\), \(.*\...\), \(.*\...\).*/\\2/\" -e \"s/ //g\")
local diff1_5=$(echo -e \"scale = scale ($one) \\nx=$one - $five\\n if (x>0) {print \\\"up\\\"} else {print \\\"down\\\"}\\n print x \\nquit \\n\" | bc)
loaddiff=\"$(echo -n \"${one}${diff1_5}\" | sed -e 's/down\-/down/g')\"

let files=$(ls -l | grep -c \"^-\" | tr -d \" \")
let hiddenfiles=$(ls -l -d .* | grep -c \"^-\" | tr -d \" \")
let executables=$(ls -l | grep -c ^-..x | tr -d \" \")
let directories=$(ls -l | grep -c \"^d\" | tr -d \" \")
let hiddendirectories=$(ls -l -d .* | grep -c \"^d\" | tr -d \" \")-2
let linktemp=$(ls -l | grep -c \"^l\" | tr -d \" \")

if [ \"$linktemp\" -eq \"0\" ]
then
links=\"\"
else
links=\" ${linktemp}l\"
fi
unset linktemp
let devicetemp=$(ls -l | grep -c \"^[bc]\" | tr -d \" \")

if [ \"$devicetemp\" -eq \"0\" ]
then
devices=\"\"
else
devices=\" ${devicetemp}bc\"
fi
unset devicetemp"""

poweruser_ps=r"""\[ \$(date +%T) - \$(date +%D) ]
[ \u @ \h ]\ [ \${files}.\${hiddenfiles}-\${executables}x \$(systemkit dirsize)
${directories}.\${hiddendirectories}d\${links}\${devices} ][ \${loaddiff} ][
$(ps ax | wc -l | sed -e \\\"s: ::g\\\")proc ]\[ \$(truncpwd) ] \$(showuser) """

dirks_ps=r"""\[ \\t ] \u \$(truncpwd) $ """

dotprompt_ps=r"""\.:[ \u @ \h ]:. .:[ \$(truncpwd) ]:..:[·> """

sepang_ps=r"""\⊏⁅ \u ⁑ \h ⁆⁅ \d ⁑ \\t ⁑ \$(systemkit uptime) ⁆⊐\⊏⁅ \$(truncpwd) ⁆⊐≻ """

quirk_ps=r"""\ -( \u / \h )-( \$(systemkit tty) )-( uptime: \$(systemkit uptime) )-( \$(date +%H:%M)
$(date +%d-%b-%y ) )-( files: \$(systemkit countvisiblefiles) / folders: \$(systemkit countvisibledirs) )-\ -< \$(truncpwd) >- """

sputnik_ps=r"""\♦♦( \u @ \h : Space on /: \$(systemkit usedspace /) used of \$(systemkit totalspace /) )♦♦( \$(truncpwd) )♦♦\♦♦( \$(date +%H:%M) → \$(date \\\"+%a, %d %b %y\\\") : uptime : \$(systemkit uptime) \$(showuser) )♦♦ """

ayoli_pc=r"""newPWD=\"${PWD}\"
host=${HOSTNAME/.*}
datenow=$(date \"+%a, %d %b %y\")
let promptsize=$(echo -n \"┌( $(whoami) @ $host dd, DD mmm YY)( ${PWD} )┐\" | wc -c | tr -d \" \")

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
    newPWD=\"...${PWD:${cutt}}\"
fi"""

ayoli_ps=r"""┌─( \u @ \h \$(date \"+%a, %d %b %y\") )─\${fill}─( \$newPWD
)─<└─( \$(date \"+%H:%M\") \$ )─> """

styles_pc = {
	      1 : empty_pc,
	      2 : empty_pc,
	      3 : clock_pc,
	      4 : equinox_pc,
	      5 : empty_pc,
	      6 : poweruser_pc,
	      7 : empty_pc,
	      8 : empty_pc,
	      9 : empty_pc,
	     10 : empty_pc,
	     11 : empty_pc,
	     12 : ayoli_pc,
	    }

styles_ps1 = {
	       1 : separator_ps,
	       2 : vector_ps,
	       3 : clock_ps,
	       4 : equinox_ps,
	       5 : elite_ps,
	       6 : poweruser_ps,
	       7 : dirks_ps,
	       8 : dotprompt_ps,
	       9 : sepang_ps,
	      10 : quirk_ps,
	      11 : sputnik_ps,
	      12 : ayoli_ps,
	     }
