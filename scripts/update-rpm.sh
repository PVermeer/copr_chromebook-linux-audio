#!/bin/bash

update_rpm() {
  local spec_file=./chromebook-linux-audio.spec

  local current_main_commit=$(grep '%global maincommit\s.*$' $spec_file | awk '{ print $3 }')
  local current_dep_commit=$(grep '%global depcommit\s.*$' $spec_file | awk '{ print $3 }')

  local new_main_commit=$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/WeirdTreeThing/chromebook-linux-audio/commits/HEAD")
  local new_dep_commit=$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/WeirdTreeThing/alsa-ucm-conf-cros/commits/HEAD")

  if [ "$current_main_commit" = "$new_main_commit" ] && [ "$current_dep_commit" = "$new_dep_commit" ]; then

    echo "No changes detected"
  else
    echo "Changes detected, updating RPM spec"

    sed -i -e "s/maincommit\s.*/maincommit $new_main_commit/" ./$spec_file
    sed -i -e "s/depcommit\s.*/depcommit $new_dep_commit/" ./$spec_file

    update_status="updated"
  fi
}

update_status="current"
update_rpm
