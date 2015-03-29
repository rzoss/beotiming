#!/bin/bash

PYTHON=/usr/bin/python3
PROG=beotiming.py
PROGPATH=/home/pi/beotiming/

cd $PROGPATH
while [ 1 ]
do
	$PYTHON $PROG
	sleep 1
done
