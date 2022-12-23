#!/bin/zsh -f

source ../venv/bin/activate
PROJECT_ROOT=${0:a:h}/..

src_paths="$PROJECT_ROOT/src"
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

echo "Python path is set to: $PYTHONPATH"
make html
deactivate
