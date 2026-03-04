#!/bin/sh
printenv > /etc/environment
crontab /app/scripts/task_scheduler/crontab
cron -f