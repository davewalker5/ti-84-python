#!/usr/bin/env bash

export PROJECT_ROOT=$( cd "$(dirname "$0")/.." ; pwd -P )
export PYTHONPATH="$PROJECT_ROOT/src:$PROJECT_ROOT/tests/mocks"
source "$PROJECT_ROOT/venv/bin/activate"
source "$PROJECT_ROOT/scripts/set-pythonpath.sh"
export DOCBUILD=True

# Capture the current folder
CWD=`pwd`
cd "$PROJECT_ROOT/docs"

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

# Restore the working folder
cd "$CWD"
