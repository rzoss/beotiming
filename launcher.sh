#!/bin/bash

PYTHON=/usr/bin/python3
PROG=beotiming.py
PROGPATH=/home/pi/beotiming/
CONFIG=https://github.com/rzoss/beotiming.git
export TZ="/usr/share/zoneinfo/Europe/Zurich"

# Note: killing bash scripts does not work with BusyBox's "killall"
kill_first_by_name()
{
	local PROCESS_NAME=$1
	ps ax | grep -m 1 "$PROCESS_NAME" | awk '{print $1}' | xargs kill -9
}

start()
{
	cd $PROGPATH
	while [ 1 ]
	do
		echo "********** start beotiming.py **********" >> /var/log/beotiming.log
		wget $CONFIG
		$PYTHON $PROG
		sleep 1
	done
}

stop()
{
	kill_first_by_name "launcher.sh"
	kill_first_by_name "beotiming.py"
}

case "$1" in
	start)
		start
		;;
	stop)
		stop
		;;
esac
