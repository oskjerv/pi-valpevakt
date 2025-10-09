#!/bin/bash
# run_main.sh - launcher for Raspberry Pi camera project
# reads external config for paths

# NOT IN USE AT THE MOMENT.
# MEANT TO BE A WRAPPER SCRIPT.

# Load external config (must be outside repo)
CONFIG_FILE="$HOME/.valpevakt_config"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file $CONFIG_FILE not found!"
    exit 1
fi
source "$CONFIG_FILE"

# Check that PROJECT_PATH is set
if [ -z "$PROJECT_PATH" ]; then
    echo "PROJECT_PATH not defined in config!"
    exit 1
fi

# Move to project root
cd "$PROJECT_PATH" || exit 1

# Optional: activate virtualenv
# source .venv/bin/activate

# Ensure logs folder exists
mkdir -p logs

# Set config path for Python
export CONFIG_PATH="${CONFIG_PATH:-$PROJECT_PATH/config/settings.yaml}"

# Run Python script
python3 src/main.py >> logs/app.log 2>&1
