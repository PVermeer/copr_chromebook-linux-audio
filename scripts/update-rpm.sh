#!/bin/bash

set -e

print_spec=$([ "$1" == "--print-spec" ] && echo "true" || echo "false")

spec_file=./chromebook-linux-audio.spec

main_repo=$(grep '%global repository\s.*$' $spec_file | awk '{ print $3 }')
dep_repo=$(grep '%global deprepository\s.*$' $spec_file | awk '{ print $3 }')

current_main_commit=$(grep '%global maincommit\s.*$' $spec_file | awk '{ print $3 }')
current_dep_commit=$(grep '%global depcommit\s.*$' $spec_file | awk '{ print $3 }')

update_status="current"
new_main_commit=""
new_dep_commit=""

get_new_commits() {
  echo -e "\n=== Fetching dependency git commits ===\n"

  new_main_commit=$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/WeirdTreeThing/chromebook-linux-audio/commits/HEAD")

  echo "Script commit: $current_main_commit -> $new_main_commit"

  new_dep_commit=$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/WeirdTreeThing/alsa-ucm-conf-cros/commits/HEAD")

  echo "UCM conf commit: $current_dep_commit -> $new_dep_commit"

  if [ -z "$new_main_commit" ] || [ -z "$new_dep_commit" ]; then
    echo "Could not fetch new commits"
    exit 1
  fi
}

update_rpm() {

  get_new_commits

  if [ "$current_main_commit" = "$new_main_commit" ] && [ "$current_dep_commit" = "$new_dep_commit" ]; then

    echo -e "\nNo changes detected\n"
  else
    echo -e "\n=== Changes detected, updating RPM spec === \n"

    sed -i -e "s/maincommit\s.*/maincommit $new_main_commit/" ./$spec_file
    sed -i -e "s/depcommit\s.*/depcommit $new_dep_commit/" ./$spec_file

    update_status="updated"

    if [ "$print_spec" = "true" ]; then
      echo "= Printing new spec file:\n"
      cat $spec_file
    fi
  fi
}
