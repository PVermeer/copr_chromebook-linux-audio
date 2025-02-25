#!/bin/bash

set -e

source ./scripts/bash-color.sh
bash ./scripts/checkout-deps.sh --apply-patches

echo_color "\n=== RPM build ==="

rm -rf ./rpmbuild
mkdir -p ./rpmbuild/SOURCES
cp *.patch ./rpmbuild/SOURCES

echo_color "\nRPM Lint"
rpmlint ./chromebook-linux-audio.spec

echo_color "\nRPM Build"
rpmbuild --define "_topdir $PWD/rpmbuild" --noclean -ba ./chromebook-linux-audio.spec

echo_color "\n=== RPM Contents ==="

# One-by-one for some separation
for file in ./rpmbuild/RPMS/**/*.rpm; do
  echo_color "\nRPM <$file>:"

  echo_color "\nFiles:"
  rpm -qvlp $file

  echo_color "\nScripts:"
  rpm -qp --scripts $file
done
