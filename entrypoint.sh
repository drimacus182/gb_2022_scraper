#!/bin/sh

# Freeze environment for cron jobs
printenv | sed 's/^\(.*\)$/export \1/g' > /code/.env.sh
chmod +x /code/.env.sh

#fix link-count, as cron is being a pain, and docker is making hardlink count >0 (very high)
#touch /etc/crontab /etc/cron.*/*
touch /code/cron
service cron start

# Hand off to the CMD
exec "$@"
