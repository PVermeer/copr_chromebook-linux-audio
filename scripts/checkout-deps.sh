#!/bin/bash

set -e

source ./scripts/bash-color.sh
source ./scripts/update-rpm.sh --no-update

apply_patches=$([ "$1" == "--apply-patches" ] && echo "true" || echo "false")

# Checkout commits
echo_color "\n=== Checking out submodules ==="

git submodule update --init --recursive

echo_color "\nSubmodule <$main_repo>:"
(cd "./$main_repo" && git reset --hard $current_main_commit)

echo_color "\nSubmodule <$dep_repo>:"
(cd "./$dep_repo" && git reset --hard $current_dep_commit)

# Apply patches
if [ "$apply_patches" = "true" ]; then
  echo_color "\n=== Applying patches ==="

  echo_color "\nSubmodule <$main_repo>:"

  cd "./$main_repo"

  # One-by-one so the filename of the patch is printed
  for file in ../*.patch; do
    echo_color "\nPatching <$file>:"
    git apply -v $file
  done

  cd ".."
fi