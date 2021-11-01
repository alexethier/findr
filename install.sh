#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

PROJECT_NAME="zfind"
SKIP_CLEANUP=false

while [[ $# > 0 ]]
do
    # ${1} is unbound so default it to ''
    key="${1-}"
    value="${2-}"

    # If arguments come in the form a=b
    if [[ $1 == *'='* ]]
    then
        IFS='=' read -ra key_pair <<< "$1"
        key="${key_pair[0]}"
        value="${key_pair[1]}"
    fi

    case $key in
        -s)
            SKIP_CLEANUP=true
            ;;
        --skip)
            SKIP_CLEANUP=true
            ;;
        -v)
            set -x
            ;;
        *)
            echo "Unknown option passed: $key"
            exit 1
            ;;
    esac
    shift
done

pip install wheel
pip list | tr -s ' ' | grep -e "^$PROJECT_NAME " | cut -d' ' -f1 | xargs -I {} pip uninstall -y {} || true
python3 setup.py bdist_wheel
ls -1 ./dist | grep -e ".whl$" | xargs -I {} pip install ./dist/{}

if [ "$SKIP_CLEANUP" == "false" ]; then
  rm -rf ./dist && rm -rf ./build && rm -rf "$PROJECT_NAME.egg-info"
fi
