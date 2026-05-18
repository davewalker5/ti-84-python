#!/usr/bin/env bash

# Add all the source sub-folders *except* the desktop implementation of the TI packages to PYTHONPATH
src_paths="$PROJECT_ROOT/src"
for dir in $PROJECT_ROOT/src/* ; do
  dir_name=$(basename "$dir")
  if [ -d "$dir" ] && [ "$dir_name" != "__pycache__" ] && [ "$dir_name" != "ti_desktop" ] && [ "$dir_name" != "ti_84_python.egg-info" ]; then
    if [ "$src_paths" != "" ] ; then
      src_paths="$src_paths:$dir"
    else
      src_paths=$dir
    fi
  fi
done

# Add the mocks for the TI packages and the the supporting code folder to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/tests/mocks:$src_paths"
