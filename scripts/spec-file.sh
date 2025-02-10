#!/bin/bash

# Get some spec file info

spec_file=./chromebook-linux-audio.spec

main_repo=$(grep '%global repository\s.*$' $spec_file | awk '{ print $3 }')
dep_repo=$(grep '%global deprepository\s.*$' $spec_file | awk '{ print $3 }')

current_main_commit=$(grep '%global maincommit\s.*$' $spec_file | awk '{ print $3 }')
current_dep_commit=$(grep '%global depcommit\s.*$' $spec_file | awk '{ print $3 }')
