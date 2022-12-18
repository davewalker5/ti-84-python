#!/bin/zsh -f

export PROJECT_ROOT=$( cd "$(dirname "$0")" ; pwd -P )
source "$PROJECT_ROOT/venv/bin/activate"

src_paths=""
for dir in $PROJECT_ROOT/src/* ; do
  dir_name=$dir:t
  if [ -d "$dir" ] && [ "$dir_name" != "__pycache__" ] && [ "$dir_name" != "ti_desktop" ]; then
    if [ "$src_paths" != "" ] ; then
      src_paths="$src_paths:$dir"
    else
      src_paths=$dir
    fi
  fi
done

export PYTHONPATH="$PROJECT_ROOT/tests/mocks:$src_paths"

coverage run --branch --source src -m unittest discover
coverage html -d cov_html
