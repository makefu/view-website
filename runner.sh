#!/bin/sh
cd "$(dirname "$(readlink -f "$0")")"
export DISPLAY=:99
Xvfb $DISPLAY 2>/dev/null >/dev/null  &
trap "kill $(jobs -p)" INT TERM EXIT
python init.py "$@"
