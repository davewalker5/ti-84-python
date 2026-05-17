#!/usr/bin/env bash

export PROJECT_ROOT=$( cd "$(dirname "$0")/.." ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"

python "$PROJECT_ROOT/support/extract-pulses.py" "$@"
