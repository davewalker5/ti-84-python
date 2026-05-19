#!/usr/bin/env bash

export PROJECT_ROOT=$( cd "$(dirname "$0")/.." ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"
source "$PROJECT_ROOT/scripts/set-pythonpath.sh"
OUTPUT_FILE="$PROJECT_ROOT/docs/source/dependencies.png"

pip install pydeps
rm -f "$OUTPUT_FILE"
pydeps "$dir" --noshow --reverse --rankdir BT -T png -o "$OUTPUT_FILE"
