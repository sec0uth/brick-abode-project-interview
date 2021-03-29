#!/bin/sh
set -e

# store directory with source files
data_source="$JUNIPER_DEV_SOURCE"

# ensure exists
if [ -z "$data_source" ]; then
    echo "[-] missing data source"
    exit 1
fi

if [ ! -e "$data_source" ]; then
    echo "[-] no such data source directory: $data_source"
    exit 2
fi

# update pip
pip3 install -U pip

# make dependencies install.
pushd "$data_source"
pip3 install -r requirements.txt
popd
