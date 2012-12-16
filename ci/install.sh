#!/bin/sh

PYTHON_VERSION=$(python --version 2>&1)

if [[ "$PYTHON_VERSION" >= "Python 3" ]]
then
  if [[ "$DJANGO" < "Django==1.5" ]]
  then
    exit
  fi
fi

pip install six==1.2.0 mock==0.7.2 $DJANGO --use-mirrors
