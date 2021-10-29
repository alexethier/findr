#!/bin/bash

PROJECT_NAME="findr"

pip install wheel
pip list | tr -s ' ' | grep -e "^$PROJECT_NAME " | cut -d' ' -f1 | xargs -I {} pip uninstall -y {}
python3 setup.py bdist_wheel
ls -1 ./dist | grep -e ".whl$" | xargs -I {} pip install ./dist/{}
rm -rf ./dist && rm -rf ./build && rm -rf "$PROJECT_NAME.egg-info"
