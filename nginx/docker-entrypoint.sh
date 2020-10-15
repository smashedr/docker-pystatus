#!/usr/bin/env sh

set -e

echo "Starting nginx."

nginx

echo "Starting loop..."

while true;do
    pgrep nginx >/dev/null || exit 1
    bash status.sh
    sleep 60
done
