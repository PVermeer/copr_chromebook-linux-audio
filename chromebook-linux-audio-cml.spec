%global repository chromebook-linux-audio
%global maincommit e171791e615cb52b808b2b4108ce7ac71298a827
%global deprepository alsa-ucm-conf-cros
%global depcommit 1908a457c7f2bf8b63264fe3b1e0522ea632ac5a
%global versioncommit %(echo -n %{maincommit} | head -c 8)

Name: chromebook-linux-audio
Version: 0.0.1
Release: %{versioncommit}%{?dist}
License: BSD 3-Clause License
Summary: RPM package to enable audio support on Chrome devices.
Url: https://github.com/WeirdTreeThing/%{repository}

Requires: alsa-sof-firmware
Requires: alsa-ucm
Requires: wireplumber
Requires: git
Requires: python3

Patch1: disable_git_clone.patch

%define workdir %{_builddir}/%{repository}
%define bindir %{_bindir}/%{name}
%define buildbindir $RPM_BUILD_ROOT%{bindir}

%description
RPM package to install chromebook-linux-audio to enable audio support on Chrome devices. All credits go to https://github.com/WeirdTreeThing.

This packages runs the script on install so it will work on immutable devices. If a device is NOT supported it will fail to install.

THe original script comes from https://github.com/mikaelvz/chromebook-linux-audio.

%prep
# Cleanup
rm -rf $RPM_BUILD_ROOT

%install
# Get chromebook-linux-audio script
git clone https://github.com/WeirdTreeThing/%{repository} %{buildbindir}
cd %{buildbindir}
git reset --hard %{maincommit}
%autopatch 1
rm -rf .git

# Get chromebook-linux-audio script dependency
git clone https://github.com/WeirdTreeThing/%{deprepository} %{buildbindir}/%{deprepository}
cd %{buildbindir}/%{deprepository}
git reset --hard %{depcommit}
rm -rf .git

%files
%{bindir}

%post
# Patch1 has disabled the dependency git clone in the script and
# this is now provided in this binary. Copy it to correct location
# where the script expect it. 
mkdir /tmp/%{deprepository}
mv %{buildbindir}/%{deprepository} /tmp

# Run the script
cd %{bindir}
./setup-audio
