#!/bin/sh

echo '* * * * * cd /app && PYTHONPATH=/app /usr/local/bin/poetry run python src/processing/schedulers/task_scheduler/scheduler_runner.py' | crontab -
exec cron -f