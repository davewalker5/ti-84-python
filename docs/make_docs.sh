#!/bin/zsh -f

source ../venv/bin/activate
PROJECTDIR=${0:a:h}/..
export PYTHONPATH="$PROJECTDIR/src:$PROJECTDIR/src/common:$PROJECTDIR/src/maths"
echo "Python path is set to: $PYTHONPATH"
make html
deactivate
