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
MK_MODULES=( build clean install )
MK_VERSION=1.0.2

for mod in ${CF_MODULES[@]}; do
	source .configure/${mod}
done
for mod in ${MK_MODULES[@]}; do
	source .make/${mod}
done

help_message () {

	echo -e "\n${GREEN}${APP_NAME} ${MAGENTA}v${APP_VERSION}${WHITE} / ${YELLOW}(Make ${MK_VERSION}) ${CYAN}help
	\n${WHITE}Rules:"

	echo -e "	${ORANGE}help${WHITE} *|${GREEN} Display this help message
	${ORANGE}pot${WHITE} *|${GREEN} Generate .pot files
	${ORANGE}po${WHITE} *|${GREEN} Update .po files
	${ORANGE}build${WHITE} *|${GREEN} Build necessary files
	${ORANGE}install${WHITE} *|${GREEN} Install ${APP_NAME}
	${ORANGE}remove${WHITE} *|${GREEN} Remove ${APP_NAME}
	${ORANGE}clean${WHITE} *|${GREEN} Clean build directory" | column -t -s \*
	tput sgr0

}

case ${1} in
	clean )		clean && exit 0;;
	distclean )	clean && exit 0;;
	changelog )	.make/changelog && exit 0 ;;
	help )		help_message && exit 0 ;;
esac

if [[ ! -e .configure/results ]]; then
	echo -e "\n${RED}You need to run ./configure first!\n"
	exit 1
else	source .configure/results
	source .make/files
fi

xcount=0
pcount=$#

if [[ ${pcount} -eq 0 ]]; then
	help_message
else
	while [[ ${xcount} -lt ${pcount} ]]; do
		case ${1} in
			pot )		generate_pot ;;
			po )		update_po;;
			build )		echo -e "\n${GREEN}Building ${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
					build && touch .make/build_done && echo ;;
			install )	if [[ -e .make/build_done ]]; then
						echo -e "\n${GREEN}Installing ${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
						if [[ ${EUID} != 0 ]]; then
							echo -e "\n${RED}You need to be root to install ${APP_NAME}\n"
						else
							installdirs_create && install_bsng && post_install
						fi
					else 	echo -e "\n${RED}You need to run './make build' first!\n"
						exit 1
					fi ;;
			remove ) 	if [[ ${EUID} != 0 ]]; then
						echo -e "\n${RED}You need to be root to remove ${APP_NAME}\n"
					else
						echo -e "\n${GREEN}Removing ${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
						remove_bsng
					fi ;;
			* )		help_message ;;
		esac
		shift
		xcount=$(($xcount+1))
	done
fi

unset xcount pcount
tput sgr0
