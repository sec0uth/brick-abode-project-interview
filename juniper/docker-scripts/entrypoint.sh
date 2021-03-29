#!/bin/sh
set -e

# enforces file existence
if [ ! -e requirements.txt ] \
    || [ ! -e cli.py ]; then
    echo "[-] missing data source: requirements.txt and cli.py"
    exit 1
fi

# has key?
if [ -e ~/.ssh/id_rsa ]; then
    # create ssh agent and 
    SSH_AUTH_SOCK="$(mktemp)"
    ssh-agent

    # add key to agent
    ssh-add ~/.ssh/id_rsa
fi

# update pip
pip3 install -U pip

cd "$data_source"

# make dependencies install
pip3 install -r requirements.txt

# test stuff
python3 cli.py