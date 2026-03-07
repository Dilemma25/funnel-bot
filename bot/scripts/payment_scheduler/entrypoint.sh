#!/bin/sh
printenv > /etc/environment
crontab /app/scripts/payment_scheduler/crontab
cron -f