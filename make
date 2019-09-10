#!/bin/bash
#########################################################
# 							#
# This is BashStyle-NG  				#
#							#
# Licensed under GNU GENERAL PUBLIC LICENSE v3    	#
#							#
# Copyright 2007 - 2019 Christopher Bratusek		#
#							#
#########################################################

##############################
# Setup
##############################
shopt -s extglob
TOP_PID=$$

CWD=$(dirname "$(readlink -m "${BASH_SOURCE[0]}")")

MK_VERSION=2.0.0
source "${CWD}/.settings"

##############################
# Color Settings
##############################
set_colors () {
	RED="\033[01;31m"
	GREEN="\033[01;32m"
	YELLOW="\033[01;33m"
	BLUE="\033[01;34m"
	MAGENTA="\033[01;35m"
	CYAN="\033[01;36m"
	WHITE="\033[01;37m"

	case ${TERM} in
		*xterm*color )
			ORANGE="\033[01;38;5;202m"
			SILVER="\033[01;38;5;246m"
		;;
		* )
			ORANGE=${YELLOW}
			SILVER=${WHITE}
		;;
	esac
}

set_colors

##############################
# Screen messages
##############################
help_message () {
	echo -e "\n${GREEN}${APP_NAME} ${MAGENTA}v${APP_VERSION}${WHITE} /${YELLOW} Make v${MK_VERSION} ${CYAN}help
	\n${WHITE}Rules:"

	echo -e "	${ORANGE}help${WHITE} *|${GREEN} Display this help message
	${ORANGE}pot${WHITE} *|${GREEN} Generate .pot files
	${ORANGE}po${WHITE} *|${GREEN} Update .po files
	${ORANGE}info${WHITE} *|${GREEN} Generate Info documentation
	${ORANGE}html${WHITE} *|${GREEN} Generate HTML documentation
	${ORANGE}news${WHITE} *|${GREEN} Generate NEWS file
	${ORANGE}build${WHITE} *|${GREEN} Build necessary files
	${ORANGE}install${WHITE} *|${GREEN} Install ${APP_NAME}
	${ORANGE}remove${WHITE} *|${GREEN} Remove ${APP_NAME}
	${ORANGE}clean${WHITE} *|${GREEN} Clean build directory" | column -t -s \*
	echo
	tput sgr0

	exit 0
}

run_configure_message () {
	echo -e "\n${RED}You need to run './configure' first!\n"
}

run_make_build_message () {
	echo -e "\n${RED}You need to run './make build' first!\n"
}

check_root_message () {
	echo -e "\n${RED}You need to be root to ${1} ${APP_NAME}\n"
}

build_message () {
	echo -e "\n${WHITE}Building ${GREEN}${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
}

build_end_message () {
	echo -e "\n${WHITE}You may want to continue with 'sudo ./make install'.\n"
}

install_message () {
	echo -e "\n${GREEN}Installing ${BLUE}${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
}

remove_message () {
	echo -e "\n${RED}Removing ${BLUE}${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
}

clean_message () {
	echo -e "\n${RED}Cleaning Up ${BLUE}${APP_NAME}${YELLOW} v${APP_VERSION} ${CYAN}${CODENAME}\n"
}

post_install_message () {
	echo -e "\t${WHITE}+${BLUE} post-installation tasks"
}

thanks_message () {
	echo -e "\n${SILVER}Thanks for using ${GREEN}${APP_NAME}!\n"
}

##############################
# Load configure results
##############################

[[ $# -eq 0 ]] && help_message

case ${1} in
	pot | po | build | install | remove )
		if [[ ! -f "${CWD}/.configure_results" ]]; then
			run_configure_message
			kill -s TERM "${TOP_PID}"
		else	source "${CWD}/.configure_results"
		fi
	;;
esac

##############################
# Filelist: clean
##############################
CLEAN_FILES=(data/bashstyle data/bashstyle-config-helper data/bashstyle-ng.pc
	     ui/bashstyle.ui.h rc/bashstyle-rc i18n/??/*.mo i18n/*.pot
	     .configure_results .make/build_done ui/#bashstyle.ui#
	     ui/bashstyle.ui~ doc/bashstyle.info doc/*.gz )

CLEAN_DIRS=(doc/html)

##############################
# Filelist: install
##############################
DATA_FILES=("${CWD}/data/bashstyle-ng.ini:${DATADIR}"
	    "${CWD}/data/bashstyle-ng.desktop:${DESKTOPDIR}"
	    "${CWD}/rc/bashstyle-rc:${DATADIR}/rc")

for ui in "${CWD}/ui"/*.py "${CWD}/ui"/*.ui; do
	DATA_FILES+=("${ui}:${DATADIR}/ui")
done

for rc in "${CWD}/rc"/*_* ; do
	DATA_FILES+=("${rc}:${DATADIR}/rc")
done

for html in "${CWD}/doc/html"/*.html; do
	DOC_FILES+=("${html}:${DOCDIR}")
done

MAN_FILES=("${CWD}/doc/bashstyle.1:${MANDIR}")

for lang in ${APP_LANGUAGES}; do
	LOCALE_FILES+=("${CWD}/i18n/${lang}"/{bashstyle,bashstyle-rc}.mo:"${LOCALEDIR}/${lang}/LC_MESSAGES")
done

BIN_FILES=("${CWD}/data/bashstyle:${BINDIR}"
	   "${CWD}/data/bashstyle-config-helper:${BINDIR}")

for function in "${CWD}/functions"/*; do
	BIN_FILES+=("${function}:${BINDIR}")
done

for icon in "${CWD}/data/icons"/*.png; do
	ICON_FILES+=("${icon}:${ICONDIR}")
done

PC_FILES=("${CWD}/data/bashstyle-ng.pc:${PCDIR}")

##############################
# Filelist: remove
##############################
for lang in ${APP_LANGUAGES}; do
	LOCALE_REMOVE+=("${LOCALEDIR}/${lang}"/{bashstyle,bashstyle-rc}.mo)
done

for function in "${CWD}/functions"/*; do
	BIN_REMOVE+=("${BINDIR}/$(basename "${function}")")
done

for icon in "${CWD}/data/icons"/*.png; do
	ICON_REMOVE+=("${ICONDIR}/$(basename "${icon}")")
done

REMOVE_FILES=("${LOCALE_REMOVE[@]}"
	      "${BINDIR}"/bashstyle
	      "${BINDIR}"/bashstyle-config-helper
	      "${BIN_REMOVE[@]}"
	      "${ICON_REMOVE[@]}"
	      "${PCDIR}"/bashstyle-ng.pc
	      "${MANDIR}"/bashstyle.1
	      "${DATADIR}"
	      "${DESKTOPDIR}"/bashstyle-ng.desktop
	      "${DOCDIR}")

##############################
# Checks
##############################
check_built () {
	if [[ ! -f "${CWD}/.build_done" ]]; then
		run_make_build_message
		kill -s TERM "${TOP_PID}"
	fi
}

check_root () {
	if [[ ${EUID} -ne 0 ]]; then
		check_root_message "${1}"
		kill -s TERM "${TOP_PID}"
	fi
}

##############################
# Build Actions
##############################
build_news () {
	echo -e "\t${WHITE}+${CYAN} NEWS file"
	makeinfo --no-validate  --no-headers "${CWD}/doc/news.texi" \
		> NEWS || kill -s TERM "${TOP_PID}"
}

build_readme () {
	echo -e "\t${WHITE}+${CYAN} README file"
	makeinfo --no-validate  --no-headers \
		"${CWD}/doc/userdoc_introduction.texi" > README \
		|| kill -s TERM "${TOP_PID}"
}

build_doc_info () {
	echo -e "\t${WHITE}+${CYAN} Info documentation"
	makeinfo -I "${CWD}/doc/" "${CWD}/doc/userdoc.texi" \
		-o "${CWD}/doc/bashstyle.info" || kill -s TERM "${TOP_PID}"
}

build_doc_html () {
	echo -e "\t${WHITE}+${CYAN} HTML documentation"
	makeinfo -I "${CWD}/doc/" --html "${CWD}/doc/userdoc.texi" \
		-o "${CWD}/doc/html" || kill -s TERM "${TOP_PID}"
}

gzip_man () {
	echo -e "\t${WHITE}+${CYAN} compressing manpages"
	for manpage in "${MAN_FILES[@]}"; do
		gzip -c "${manpage/:*}" > \
			"${manpage/:*}.gz" || kill -s TERM "${TOP_PID}"
	done
}

generate_pot () {
	echo -e "\t${WHITE}+${CYAN} translation templates"
	echo -e "\t${WHITE}  *${YELLOW} bashstyle.pot"
	intltool-extract --type=gettext/glade "ui/bashstyle.ui" >/dev/null
	xgettext -L python --from-code=utf-8 --keyword=_ --keyword=N_ \
		--output="${CWD}/i18n/bashstyle.pot" \
		"${CWD}/ui"/*.py "${CWD}/ui/bashstyle.ui.h" >/dev/null \
		|| kill -s TERM "${TOP_PID}"

	echo -e "\t${WHITE}  *${YELLOW} bashstyle-rc.pot"
	xgettext -o "${CWD}/i18n/bashstyle-rc.pot" -L shell --from-code=utf-8 \
		"${CWD}/rc/bashstyle-rc" "${CWD}/rc"/settings_* \
		"${CWD}"/functions/* "${CWD}/rc"/function_* 2>/dev/null \
		|| kill -s TERM "${TOP_PID}"
}

update_po () {
	if [[ ! -f ${CWD}/i18n/bashstyle.pot || ! -f ${CWD}/i18n/bashstyle-rc.pot ]]; then
		echo -e "\n${RED}You need to run './make pot' first!\n"
		kill -s TERM "${TOP_PID}"
	fi

	echo -e "\t${WHITE}+${CYAN} gui translations"
	for lang in ${APP_LANGUAGES}; do
		echo -e "\t${WHITE} *${MAGENTA} ${lang}"
		msgmerge -q -o i18n/"${lang}"/bashstyle.po i18n/"${lang}"/bashstyle.po \
			i18n/bashstyle.pot >/dev/null || kill -s TERM "${TOP_PID}"
	done

	echo -e "\t${WHITE}+${CYAN} bashstyle-rc translations"
	for lang in ${APP_LANGUAGES}; do
		echo -e "\t${WHITE} *${MAGENTA} ${lang}"
		msgmerge -q -o i18n/"${lang}"/bashstyle-rc.po i18n/"${lang}"/bashstyle-rc.po \
			i18n/bashstyle-rc.pot >/dev/null || kill -s TERM "${TOP_PID}"
	done
}

generate_mo () {
	echo -e "\t${WHITE}+${CYAN} gui translations"
	for lang in ${APP_LANGUAGES}; do
		echo -e "\t${WHITE} *${MAGENTA} ${lang}"
		msgfmt --output-file="${CWD}/i18n/${lang}/bashstyle.mo" \
			"${CWD}/i18n/${lang}/bashstyle.po" || kill -s TERM "${TOP_PID}"
	done

	echo -e "\t${WHITE}+${CYAN} bashstyle-rc translations"
	for lang in ${APP_LANGUAGES}; do
		echo -e "\t${WHITE} *${MAGENTA} ${lang}"
		msgfmt --output-file="${CWD}/i18n/${lang}/bashstyle-rc.mo" \
			"${CWD}/i18n/${lang}/bashstyle-rc.po" || kill -s TERM "${TOP_PID}"
	done
}

##############################
# Install Actions
##############################
post_install () {
	if [ "${DISABLE_POSTINSTALL}" -ne 1 ]; then
		post_install_message
		gtk-update-icon-cache -q -f "${PREFIX}/share/icons/hicolor"
	fi
}

post_remove () {
	return 0
}

installdirs_create ()
{
	echo -e "\t${WHITE}+${MAGENTA} directories"
	mkdir -p "${DESTDIR}/${DATADIR}"
	for directory in "${DATADIR_LIST[@]}"; do
		mkdir -p "${DESTDIR}/${DATADIR}/${directory}"
	done

	mkdir -p "${DESTDIR}/${LOCALEDIR}"
	for directory in "${LOCALEDIR_LIST[@]}"; do
		mkdir -p "${DESTDIR}/${LOCALEDIR}/${directory}"
	done

	mkdir -p "${DESTDIR}/${BINDIR}" "${DESTDIR}/${ICONDIR}" \
		"${DESTDIR}/${PCDIR}" "${DESTDIR}/${DOCDIR}" \
		"${DESTDIR}/${DESKTOPDIR}" "${DESTDIR}/${MANDIR}"
}

inst ()
{
	FILE=${2/:*}
	DEST=${2/*:}

	case ${1} in
		bin )	install -m755 "${FILE}" "${DESTDIR}${DEST}" ;;
		man )	install -m644 "${FILE}".gz "${DESTDIR}${DEST}" ;;
		* )	install -m644 "${FILE}" "${DESTDIR}${DEST}" ;;
	esac
}

install_bsng () {
	echo -e "\t${WHITE}+${YELLOW} data files"
	for file in "${DATA_FILES[@]}" "${LOCALE_FILES[@]}" \
		"${PC_FILES[@]}" "${ICON_FILES[@]}"; do
		inst data "${file}"
	done

	echo -e "\t${WHITE}+${GREEN} executable files"
	for file in "${BIN_FILES[@]}"; do
		inst bin "${file}"
	done

	echo -e "\t${WHITE}+${CYAN} documentation and manual pages"
	for file in "${DOC_FILES[@]}"; do
		inst doc "${file}"
	done

	for file in "${MAN_FILES[@]}"; do
		inst man "${file}"
	done
}

remove_bsng () {
	echo -e "\t${WHITE}+${RED} all files"
	for file in "${REMOVE_FILES[@]}"; do
		rm -rf "${file}"
	done
}

##############################
# Tasks
##############################
make_build () {
	build_message
	generate_mo
	build_doc_html
	gzip_man
	build_end_message
	touch "${CWD}/.build_done"
}

make_install () {
	check_built
	check_root "install"
	install_message
	installdirs_create
	install_bsng
	post_install
	thanks_message
}

make_remove () {
	check_root "remove"
	remove_message
	remove_bsng
	post_remove
}

make_clean () {
	clean_message
	for file in "${CLEAN_FILES[@]}"; do
		rm -f "${file}"
	done

	for dir in "${CLEAN_DIRS[@]}"; do
		rm -rf "${dir}"
	done
}

##############################
# Main Loop
##############################
for opt in "${@}"; do
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

tput sgr0
