#!/bin/bash
until sudo python main.py; do
  echo "Salame 'main.py' crashed with exit code $?. Restarting..." >&2
  sleep 1
done
