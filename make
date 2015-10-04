#!/bin/bash
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3    	#
#							#
# Copyright 2007 - 2015 Christopher Bratusek		#
#							#
#########################################################

CF_MODULES=( base color )
MK_MODULES=( build install messages checks actions )
MK_VERSION=1.0.7

for mod in ${CF_MODULES[@]}; do
	source .configure/${mod}
done
for mod in ${MK_MODULES[@]}; do
	source .make/${mod}
done

xcount=0
pcount=$#

if [[ ${pcount} -eq 0 ]]; then
	help_message
else
	while [[ ${xcount} -lt ${pcount} ]]; do
		case ${1} in
			clean )		make_clean ;;
			pot )		generate_pot ;;
			po )		update_po ;;
			build )		make_build ;;
			install )	make_install ;;
			remove )	make_remove ;;
			news )		make_news ;;
			* )		help_message ;;
		esac
		shift
		xcount=$(($xcount+1))
	done
fi

unset xcount pcount
tput sgr0
