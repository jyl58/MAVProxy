#!/bin/sh

pid=$(ps -ef | grep "SCREEN" | grep -v grep | awk '{print $2}')

if [ -n "$pid" ]; then
	sudo kill -9 "$pid"
fi

(screen -dm mavproxy.py --master=/dev/ttyACM0,115200 --out=udpin:0.0.0.0:15440 --default-modules=Formation) > /dev/null 2>&1 &

exit 0
