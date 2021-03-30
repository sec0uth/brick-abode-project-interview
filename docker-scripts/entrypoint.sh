#!/bin/sh
set -e

# has key?
if [ -e ~/.ssh/id_rsa ]; then
    # create ssh agent and export agent environment variables
    eval "$(ssh-agent)"

    # add key to agent
    ssh-add ~/.ssh/id_rsa
fi

# pass execution to received args in current shell
"$@"
