#!/bin/bash

set -e
set -o pipefail

echo -e "Checking for unpatched input statements in functions.py:\n"

! grep -Ev '^.*#.*$' ./chromebook-linux-audio/functions.py | grep -E 'input\(.*\)'
