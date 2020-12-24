#!/bin/sh

# Kill all zombie python process listening on any port.
lsof -i -P -n | grep LISTEN | grep "^Python" | cut -c 9-16 | xargs kill
