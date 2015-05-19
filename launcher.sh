#!/bin/bash

# https://stackoverflow.com/questions/696839/how-do-i-write-a-bash-script-to-restart-a-process-if-it-dies/697064#697064
# Remember to: chmod 755 launcher.sh
#
# Add to chronjob:
# sudo crontab -e
# Add line:
# @reboot sh /home/pi/salame/launcher.sh >/home/pi/logs/cronlog.log 2>&1

until sudo python /home/pi/salame/main.py; do
  echo "Salame 'main.py' crashed with exit code $?. Restarting..." >&2
  sleep 1
done
