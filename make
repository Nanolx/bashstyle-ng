#!/bin/bash
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3    	#
#							#
# Copyright 2007 - 2018 Christopher Bratusek		#
#							#
#########################################################

CF_MODULES=( base color )
MK_MODULES=( build install messages checks actions )
MK_VERSION=1.1.1

for mod in "${CF_MODULES[@]}"; do
	source "${PWD}"/.configure/"${mod}"
done

for mod in "${MK_MODULES[@]}"; do
	source "${PWD}"/.make/"${mod}"
done

if [[ $# -eq 0 ]]; then
	help_message
else
	for opt in ${@}; do
		case ${opt} in
			clean )		make_clean ;;
			pot )		generate_pot ;;
			po )		update_po ;;
			build )		make_build ;;
			install )	make_install ;;
			remove )	make_remove ;;
			news )		build_news ;;
			readme )	build_readme ;;
			info )		build_doc_info ;;
			html )		build_doc_html ;;
			* )		help_message ;;
		esac
		shift
	done
fi

tput sgr0
