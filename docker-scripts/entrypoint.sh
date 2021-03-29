#!/bin/sh
set -e

# enforces file existence
if [ ! -e requirements.txt ]; then
    echo "[-] missing data source file: requirements.txt"
    exit 1
fi

# has key?
if [ -e ~/.ssh/id_rsa ]; then
    # create ssh agent and export agent environment variables
    eval "$(ssh-agent)"

    # add key to agent
    ssh-add ~/.ssh/id_rsa
fi

# update pip
pip3 install -U pip

# make dependencies install
pip3 install -r requirements.txt

# pass execution to received args in current shell
"$@"
