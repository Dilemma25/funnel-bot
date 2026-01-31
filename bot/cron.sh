#!/bin/bash

PROJECT_DIR="/home/dilemma/projects/telegram-bot-funnel/bot"
LOG_FILE="/home/dilemma/projects/telegram-bot-funnel/bot/var/log/scheduler.log"
LOG_DIR="$(dirname "$LOG_FILE")"

mkdir -p "$LOG_DIR"

cd "$PROJECT_DIR"

echo "$(date): Starting scheduler" >> "$LOG_FILE" 2>&1
poetry run python -m src.scheduler.runner >> "$LOG_FILE" 2>&1
echo "$(date): Scheduler finished" >> "$LOG_FILE" 2>&1