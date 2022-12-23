#!/bin/zsh -f

source ../venv/bin/activate
PROJECT_ROOT=${0:a:h}/..
export DOCBUILD=True

# Add all the source sub-folders *except* the desktop implementation of the TI packages to PYTHONPATH
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

# Add the mocks for the TI packages to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/tests/mocks:$src_paths"

# Create the dummy stdin file
for n in {1..20}
do
  echo >> stdin.txt
done

echo "Python path is set to: $PYTHONPATH"
make html < stdin.txt
rm stdin.txt
unset DOCBUILD
deactivate
