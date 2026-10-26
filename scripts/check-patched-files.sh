#!/bin/bash

set -e
set -o pipefail

echo -e "Checking for unpatched read commands in setup-audio:\n"

! grep -nE '^[[:space:]]*read([[:space:]]|$)|[;&|][[:space:]]*read([[:space:]]|$)|\bthen[[:space:]]+read([[:space:]]|$)' ./chromebook-linux-audio/setup-audio
