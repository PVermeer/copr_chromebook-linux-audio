%global repository chromebook-linux-audio
%global maincommit e171791e615cb52b808b2b4108ce7ac71298a827
%global deprepository alsa-ucm-conf-cros
%global depcommit 00b399ed00930bfe544a34358547ab20652d71e3
%global mainversioncommit %(echo -n %{maincommit} | head -c 8)
%global depversioncommit %(echo -n %{depcommit} | head -c 8)

Name: chromebook-linux-audio
Version: 0.0.1
Release: %{mainversioncommit}.%{depversioncommit}%{?dist}
License: BSD 3-Clause License
Summary: RPM package to enable audio support on Chrome devices.
Url: https://github.com/WeirdTreeThing/%{repository}

BuildRequires: alsa-sof-firmware
BuildRequires: alsa-ucm
BuildRequires: git
BuildRequires: python3
BuildRequires: wireplumber

Requires: alsa-sof-firmware
Requires: alsa-ucm

Patch1: disable_git_clone.patch

%define workdir %{_builddir}/%{repository}
%define datadir %{_datadir}/%{name}
%define builddatadir $RPM_BUILD_ROOT/%{datadir}

%description
RPM package to install chromebook-linux-audio to enable audio support on Chrome devices. All credits go to https://github.com/WeirdTreeThing.

This packages runs the script on install so it will work on immutable devices. If a device is NOT supported it will fail to install.

The original script comes from https://github.com/mikaelvz/chromebook-linux-audio.

%prep
# Get chromebook-linux-audio script
git clone https://github.com/WeirdTreeThing/%{repository} %{workdir}
cd %{workdir}
git reset --hard %{maincommit}
%autopatch 1
rm -rf .git

# Get chromebook-linux-audio script dependency
git clone https://github.com/WeirdTreeThing/%{deprepository} %{workdir}/%{deprepository}
cd %{workdir}/%{deprepository}
git reset --hard %{depcommit}
rm -rf .git

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}
mv %{workdir} $RPM_BUILD_ROOT/%{_datadir}

%files
%{datadir}

%post
# Patch1 has disabled the dependency git clone in the script and
# this is now provided in this binary. Copy it to correct location
# where the script expect it. 
cp -r %{datadir}/%{deprepository} /tmp

# Run the script
cd %{datadir}
./setup-audio

# Cleanup
rm -rf /tmp/%{deprepository}
