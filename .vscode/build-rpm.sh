#!/bin/bash

rpmdev-setuptree
ln -sf ~/rpmbuild ./rpmbuild
cp *.patch ~/rpmbuild/SOURCES
rpmbuild -bb ./chromebook-linux-audio-cml.spec
