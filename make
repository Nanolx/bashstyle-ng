#!/bin/bash

if [[ $1 == *clean* ]]; then
	source $PWD/.make/clean
	clean
	exit 0
elif [[ ! -e $PWD/.configure/results ]]; then
	echo -e "\n${RED}You need to run configure first!\n"
	exit 1
else	source $PWD/.configure/results
fi

MODULES=( adjust build clean color files help i18n install installdirs )

for mod in ${MODULES[@]}; do
	source $PWD/.make/$mod
done

if [[ $1 == *verbose ]]; then
	VERBOSE="true"
	shift
fi

xcount=0
pcount=$#

while [[ $xcount -lt $pcount ]]; do
	case $1 in

		pot ) generate_pot ;;

		po ) update_po;;

		build ) echo -e "\n${YELLOW}Building BashStyle-NG:\n"
			build && touch .make/build_done && echo ;;

		clean ) clean ;;

		distclean ) distclean ;;

		export ) git_export $HOME/Desktop/bashstyle-ng-$2 ;;

		install ) if [[ -e $PWD/.make/build_done ]]; then
				echo -e "\n${GREEN}Installing BashStyle-NG:\n"
				installdirs_create && install_bsng && post_install
			  else 	echo -e "\n${RED}You need to run ./make build first!\n"
			  fi ;;

		remove ) echo -e "\n${RED}Removing BashStyle-NG:\n"
			remove_bsng ;;

		changelog ) $PWD/.make/changelog ;;

		* ) help_message ;;

	esac
	shift
	xcount=$(($xcount+1))
done

unset xcount pcount

tput sgr0
