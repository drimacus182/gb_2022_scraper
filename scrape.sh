#!/usr/bin/env bash

set -e


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd ${SCRIPT_DIR}

# Try to load frozen environment from .env.sh
touch .env.sh
source .env.sh || true

## Acquiring a lock
LOCK=.scrape.lock
remove_lock()
{
    rm -f "$LOCK"
}

lockfile -r 5 -l 7200 "$LOCK" || exit 1 # 2 hours
trap remove_lock EXIT
###

source env/bin/activate
mkdir -p data

env/bin/python3 scrape.py
