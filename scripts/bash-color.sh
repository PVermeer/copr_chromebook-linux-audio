#!/bin/bash

blue='\033[1;34m'
teal='\033[1;36m'
green='\033[1;32m'
yellow='\033[1;33m'
orange='\033[38:5:202m'
red='\033[1;31m'
pink='\033[38:5:205m'
purple='\033[1;35m'
slate='\033[38:5:67m'
removecolor='\033[0m'
arrow='➜'
themecolor=$purple

THEME=$(gsettings get org.gnome.desktop.interface accent-color 2>/dev/null || echo "'purple'")
THEME=${THEME//\'/}

case $THEME in
"blue")
  themecolor=$blue
  ;;
"green")
  themecolor=$green
  ;;
"orange")
  themecolor=$orange
  ;;
"pink")
  themecolor=$pink
  ;;
"purple")
  themecolor=$purple
  ;;
"red")
  themecolor=$red
  ;;
"slate")
  themecolor=$slate
  ;;
"teal")
  themecolor=$teal
  ;;
"yellow")
  themecolor=$yellow
  ;;
*)
  themecolor=$purple
  ;;
esac

# Set stderr color
exec 9>&2
exec 8> >(
  while IFS='' read -r line || [ -n "$line" ]; do
    echo -e "${red}${line}${removecolor}"
  done
)
function undirect() { exec 2>&9; }
function redirect() { exec 2>&8; }
trap "redirect;" DEBUG
PROMPT_COMMAND='undirect;'
BASH_XTRACEFD=1 # set -x to stdout

# Color wrapper
echo_color() {
  local arguments=$@

  # Some shells (github actions!) dont pass the color
  # to the next line when provided before `\n`
  if [ "${arguments:0:2}" = "\n" ]; then
    arguments=${arguments#\\n}
    echo ""
  fi
  echo -e "${themecolor}$arguments${removecolor}"
}
