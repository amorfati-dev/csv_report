#!/bin/bash

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment if it exists
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# Check if .env exists and is readable
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "Error: .env file not found in $SCRIPT_DIR"
    exit 1
fi

if [ ! -r "$SCRIPT_DIR/.env" ]; then
    echo "Error: Cannot read .env file. Check permissions."
    exit 1
fi

# Clear yagmail cache
rm -rf ~/.yagmail

# Execute the command in the same shell context
cd "$SCRIPT_DIR" && PYTHONPATH=src python -m csv_report.report.email 