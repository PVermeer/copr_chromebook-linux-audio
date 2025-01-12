#!/bin/bash

set -e

apply_patches=$([ "$1" == "--apply-patches" ] && echo "true" || echo "false")

# Get current commits in spec file
source ./scripts/update-rpm.sh

# Checkout commits
echo -e "\n=== Checking out submodules ===\n"

echo -e "$main_repo: $(cd "./$main_repo" && git reset --hard $current_main_commit)"
echo -e "$dep_repo: $(cd "./$dep_repo" && git reset --hard $current_dep_commit)"

echo -e "\n"

# Apply patches
if [ "$apply_patches" = "true" ]; then
  echo -e "\n=== Applying patches ==="

  echo -e "\nSubmodule <$main_repo>:"
  (cd "./$main_repo" && git apply -v ../*.patch)
fi
