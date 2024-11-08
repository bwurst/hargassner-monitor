#!/bin/bash
RUNNING=1

if [ -f /tmp/hargassner-rs232.pid ] ; then
  PID="$(</tmp/hargassner-rs232.pid)"
  if ! [ -d "/proc/$PID" ] ; then
    RUNNING=0
  fi
else
  RUNNING=0
fi

if [ "$RUNNING" == 0 ] ; then
  echo 'Hargassner-Monitor laeuft nicht, wird gestartet...'
  cd ~/hargassner-monitor/rs232/ ; screen -dmS rs232 -h 1000 ./bin/rs232monitor
fi
