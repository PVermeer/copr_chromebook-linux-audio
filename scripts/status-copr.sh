#!/bin/bash

set -e

owner="pvermeer"
project="chromebook-linux-audio"
package="chromebook-linux-audio"

echo -e "\n=== Getting status ===\n"

build_state=$(curl -s -X 'GET' \
  "https://copr.fedorainfracloud.org/api_3/package/?ownername=$owner&projectname=$project&packagename=$package&with_latest_build=true&with_latest_succeeded_build=false" \
  -H 'accept: application/json' | jq -r '.builds.latest.state')

echo "Copr build status: $build_state"

if [ "$build_state" = "succeeded" ]; then
  exit 0
else
  exit 1
fi
