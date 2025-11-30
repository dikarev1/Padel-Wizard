#!/bin/bash
set -e

PROJECT_DIR="/root/stuff/padel_wizard"
VENV="$PROJECT_DIR/venv/bin/python3"

echo "→ Pulling latest changes..."
cd $PROJECT_DIR
git pull

echo "→ Installing dependencies..."
$PROJECT_DIR/venv/bin/pip install -r requirements.txt

echo "→ Applying migrations (if any)..."
# python3 -m padel_wizard_bot.migrate  # пример

echo "→ Restarting bot..."
supervisorctl restart padel

echo "→ Done."

