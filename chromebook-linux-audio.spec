%global repository chromebook-linux-audio
%global maincommit 4617151f8ade809b3ef92621d75bbc2a08589741
%global deprepository alsa-ucm-conf-cros
%global depcommit 1908a457c7f2bf8b63264fe3b1e0522ea632ac5a
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
Patch2: disable_max98357a.patch

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
%autopatch 2
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
