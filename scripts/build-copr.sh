#!/bin/bash

set -e

copr_build_webhook=$1

echo -e "\n=== Sending build request to Copr ===\n"

curl -X POST $copr_build_webhook
echo "Succeeded"

echo -e "\n=== Awaiting status ===\n"

build_state=""
until [ "$build_state" = "succeeded" ] || [ "$build_state" = "failed" ]; do

  build_state=$(curl -s -X 'GET' \
    'https://copr.fedorainfracloud.org/api_3/package/?ownername=pvermeer&projectname=chromebook-linux-audio&packagename=chromebook-linux-audio&with_latest_build=true&with_latest_succeeded_build=false' \
    -H 'accept: application/json' | jq -r '.builds.latest.state')

  echo "Copr build status: $build_state"

  if [ "$build_state" = "succeeded" ]; then
    exit 0
  elif [ "$build_state" = "failed" ]; then
    exit 1
  else
    sleep 10
  fi
done
