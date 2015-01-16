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

if [[ ! -e .configure/results ]]; then
	echo -e "\n${RED}You need to run configure first!\n"
	exit 1
fi

CF_MODULES=( base color results )
MK_MODULES=( build clean files install )

for mod in ${CF_MODULES[@]}; do
	source .configure/${mod}
done
for mod in ${MK_MODULES[@]}; do
	source .make/${mod}
done

help_message () {

	echo -e "\n${GREEN}BashStyle-NG ${MAGENTA}v${xVERSION}${WHITE} / ${YELLOW}(Make 1.0) ${CYAN}help
	\n${WHITE}Rules:"
	echo -e "${ORANGE}help${WHITE} *|${GREEN} Display this help message\
	\n${ORANGE}pot${WHITE} *|${GREEN} Generate .pot files\
	\n${ORANGE}po${WHITE} *|${GREEN} Update .po files\
	\n${ORANGE}build${WHITE} *|${GREEN} Build necessary files\
	\n${ORANGE}install${WHITE} *|${GREEN} Install BashStyle-NG\
	\n${ORANGE}remove${WHITE} *|${GREEN} Remove BashStyle-NG\
	\n${ORANGE}clean${WHITE} *|${GREEN} Clean build directory\
	\n${ORANGE}changelog${WHITE} *|${GREEN} Generate ChangeLog" | column -t -s \*
	echo
	tput sgr0

}

xcount=0
pcount=$#

while [[ ${xcount} -lt ${pcount} ]]; do
	case ${1} in
		pot )		generate_pot ;;
		po )		update_po;;
		build )		echo -e "\n${GREEN}BashStyle-NG${YELLOW} v${xVERSION} ${CYAN}${CODENAME}\n"
				tput sgr0
				build && touch .make/build_done && echo ;;
		clean )		clean ;;
		distclean )	distclean ;;
		install )	if [[ -e .make/build_done ]]; then
					echo -e "\n${GREEN}Installing BashStyle-NG:\n"
					installdirs_create && install_bsng && post_install
				else 	echo -e "\n${RED}You need to run 'make' first!\n"
				fi ;;
		remove ) 	echo -e "\n${RED}Removing BashStyle-NG:\n"
				remove_bsng ;;
		changelog )	.make/changelog ;;
		* )		help_message ;;
	esac
	shift
	xcount=$(($xcount+1))
done

unset xcount pcount
tput sgr0
