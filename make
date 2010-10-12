#!/bin/bash

source $PWD/.configure/results

MODULES=( adjust build clean color files help i18n install installdirs )

for mod in ${MODULES[@]}; do
	source $PWD/.make/$mod
done

if [[ ! -e $PWD/.configure/results ]]; then
	echo -e "\n${RED}You need to run configure first!\n"
	exit 1
fi

if [[ $1 == *destdir* ]]; then
	export DESTDIR=${1/*=}
	shift
fi

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
		 pre_remove && remove_bsng && installdirs_remove ;;

	changelog ) $PWD/.make/changelog ;;

	* ) help_message ;;

esac

unset DESTDIR
tput sgr0
