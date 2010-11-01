#!/bin/bash

if [[ ! -e $PWD/.configure/results ]]; then
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

		build ) build && touch .make/build_done;;

		clean ) clean ;;

		distclean ) distclean ;;

		export ) git_export $HOME/Desktop/bashstyle-ng-$2 ;;

		install ) if [[ $EUID != 0 ]]; then
				echo -e "\n${RED}You're not root!\n"
				exit 1
			  fi
			  if [[ -e $PWD/.make/build_done ]]; then
				installdirs_create && install_bsng && post_install
			  else 	echo -e "\n${RED}You need to run ./make all first!\n"
			  fi ;;

		remove ) if [[ $EUID != 0 ]]; then
				echo -e "\n${RED}You're not root!\n"
				exit 1
			fi
			pre_remove && remove_bsng ;;

		changelog ) $PWD/.make/changelog ;;

		* ) help_message ;;

	esac
	shift
	xcount=$(($xcount+1))
done

unset xcount pcount

tput sgr0
