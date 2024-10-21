#!/bin/sh

# set default value
UPDATE_INTERVAL=${UPDATE_INTERVAL:-600}

trap exit TERM

while true
do
	python3 /opt/update.py &
	sleep $UPDATE_INTERVAL &
	wait
done
