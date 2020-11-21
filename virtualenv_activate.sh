#!/bin/bash

if [ "$0" == "bash" ] || [ "$0" == "-bash" ]; then
  source ./venv/bin/activate 
  echo "venv activated"
else
  echo -e "Example usage:\nsource $0\nOr:\n. $0"
fi
