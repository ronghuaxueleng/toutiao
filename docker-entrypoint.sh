#!/bin/bash
set -e
set -o errexit
set -o pipefail
set -o nounset

crontab -r && crontab crontab.list
/usr/bin/mitmdump -s mproxy.py --set block_global=false --mode socks5
exec "$@"