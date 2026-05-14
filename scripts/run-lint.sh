#!/usr/bin/env bash

export PROJECT_ROOT=$( cd "$(dirname "$0")/.." ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"

# Detect Python syntax errors or undefined names
flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics

# Lint the source - exit-zero treats all errors as warnings and the width is set
# based on the GitHub editor width of 127 chars
flake8 src --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Detect unused methods
vulture src 
