#!/usr/bin/env sh

echo "Starting nginx..."
nginx

echo "Copying static..."
cp -r source/static /data/html
ls -la /data/html

echo "Starting loop..."
while true;do
    pgrep nginx >/dev/null || exit 1
    python3 -u pystatus.py
    sleep 60
done
