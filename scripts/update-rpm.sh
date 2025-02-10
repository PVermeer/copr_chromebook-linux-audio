#!/bin/bash

set -e

source ./scripts/bash-color.sh
source ./scripts/spec-file.sh

# Parameters
print_spec="false"
no_update="false"

while [[ "$#" -gt 0 ]]; do
  case $1 in
  --print-spec)
    print_spec="true"
    shift
    ;;
  --no-update)
    no_update="true"
    shift
    ;;
  *)
    echo "Unknown parameter passed: $1"
    exit 1
    ;;
  esac
done

update_status="current"

echo_color "\n=== Checking for changes ===\n"

echo_color "Fetching dependency git commits"

new_main_commit=$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/WeirdTreeThing/chromebook-linux-audio/commits/HEAD")
new_dep_commit=$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/WeirdTreeThing/alsa-ucm-conf-cros/commits/HEAD")

echo "Script commit: $current_main_commit -> $new_main_commit"
echo "UCM conf commit: $current_dep_commit -> $new_dep_commit"

if [ -z "$new_main_commit" ] || [ -z "$new_dep_commit" ]; then
  echo "Could not fetch new commits"
  exit 1
fi

if [ "$current_main_commit" = "$new_main_commit" ] && [ "$current_dep_commit" = "$new_dep_commit" ]; then

  echo -e "\nNo changes detected"
else
  echo -e "\nChanges detected"

  echo_color "\n=== Updating RPM spec ===\n"

  if [ "$no_update" = "true" ]; then
    echo "RPM spec not updated because '--no-update' was passed"
  else
    sed -i -e "s/maincommit\s.*/maincommit $new_main_commit/" ./$spec_file
    sed -i -e "s/depcommit\s.*/depcommit $new_dep_commit/" ./$spec_file

    echo "RPM spec updated"
    update_status="updated"
  fi

  if [ "$print_spec" = "true" ]; then
    echo_color "\nNew spec file:"
    cat $spec_file
  fi
fi
