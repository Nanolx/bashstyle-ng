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
MK_VERSION=1.0.3

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

check_configure () {
	if [[ ! -e .configure/results ]]; then
		echo -e "\n${RED}You need to run ./configure first!\n"
		exit 1
	else	source ${PWD}/.configure/results
		source ${PWD}/.make/files
	fi
}

check_built () {
	if [[ ! -e ${PWD}/.make/build_done ]]; then
		echo -e "\n${RED}You need to run './make build' first!\n"
		exit 1
	fi
}

check_root () {
	if [[ ${EUID} != 0 ]]; then
		echo -e "\n${RED}You need to be root to ${1} ${APP_NAME}\n"
		exit 1
	fi
}

make_build () {
	check_configure && 
		echo -e "\n${Blue}Building ${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n" && 
		build && touch .make/build_done
}

make_install () {
	check_configure && check_built && check_root "install" &&
		echo -e "\n${GREEN}Installing ${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n" && 
		installdirs_create && install_bsng && 
		post_install
}

make_remove () {
	check_configure && check_root "remove" && \
		echo -e "\n${Red}Removing ${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n" && \
		remove_bsng
}

xcount=0
pcount=$#

if [[ ${pcount} -eq 0 ]]; then
	help_message
else
	while [[ ${xcount} -lt ${pcount} ]]; do
		case ${1} in
			clean )		clean ;;
			pot )		generate_pot ;;
			po )		update_po ;;
			build )		make_build ;;
			install )	make_install ;;
			remove )	make_remove ;;
			* )		help_message ;;
		esac
		shift
		xcount=$(($xcount+1))
	done
fi

unset xcount pcount
tput sgr0
