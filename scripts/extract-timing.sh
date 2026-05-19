#!/usr/bin/env bash

export PROJECT_ROOT=$( cd "$(dirname "$0")/.." ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"
source "$PROJECT_ROOT/scripts/set-pythonpath.sh"

python "$PROJECT_ROOT/src/support/extract_timings.py" "$@"
