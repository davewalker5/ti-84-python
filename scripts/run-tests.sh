#!/usr/bin/env bash

export PROJECT_ROOT=$( cd "$(dirname "$0")/.." ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"
source "$PROJECT_ROOT/scripts/set-pythonpath.sh"

echo Project root = $PROJECT_ROOT
echo Python Path  = $PYTHONPATH

python -m unittest
