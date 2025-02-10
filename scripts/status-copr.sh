#!/bin/bash

set -e

source ./scripts/bash-color.sh

no_fail=$([ "$1" == "--no-fail" ] && echo "true" || echo "false")

owner="pvermeer"
project="chromebook-linux-audio"
package="chromebook-linux-audio"

echo_color "\n=== Getting status ===\n"

build_state=$(curl -s -X 'GET' \
  "https://copr.fedorainfracloud.org/api_3/package/?ownername=$owner&projectname=$project&packagename=$package&with_latest_build=true&with_latest_succeeded_build=false" \
  -H 'accept: application/json' | jq -r '.builds.latest.state')

echo "Copr build status: $build_state"

if [ "$no_fail" = "true" ]; then
  exit 0
fi

if [ "$build_state" = "failed" ]; then
  exit 1
else
  exit 0
fi
