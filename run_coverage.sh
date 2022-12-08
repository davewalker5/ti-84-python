#!/bin/zsh -f

export PROJECT_ROOT=$( cd "$(dirname "$0")" ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"
export PYTHONPATH="$PROJECT_ROOT/src:$PROJECT_ROOT/src/maths"
coverage run --branch --source src -m unittest discover
coverage html -d cov_html
