#!/bin/sh
#
# Start PyDoc documentation server at all interfaces.

# Assuming python version 3.6 does not support providing 
# a custom interface to bind the server, a small patch is 
# required for host to access container port.

# default listen port
listen_port=8080

# accept script argument as custom listen port
if [ -n "$1" ]; then
    listen_port="$1"
fi

# patch pydoc.py module
patch --force /usr/lib/python3.6/pydoc.py \
    /usr/share/docker-scripts/patches/pydoc.py.diff

# start the server replacing current shell
exec python3 -m pydoc -p "$listen_port"
