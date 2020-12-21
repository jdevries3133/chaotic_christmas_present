#!/bin/bash

# This comes from the song_maker_gallery project. It is an example of a bash
# script that also handles a subprocess. I think I will need to do something
# like this to gracefully spin up and spin down many tcp servers

# Start script for easy startup and shutdown. In production, it is worth
# considering that this script does not end with "exec", which will hide
# and potentially slow the child processes, so this is not best used in
# every scenario.

my_exit () {
    [ "$started" ] && pid=$!
    [ "$pid" ] && kill "$pid"
    echo "start.sh: Killed sc_daemon (pid $pid)"
}
trap my_exit EXIT

source ../venv/bin/activate

started=y
python bot/sc_daemon.py &
gunicorn screenshot_bot.wsgi:application --bind 0.0.0.0:8000

exit 0
