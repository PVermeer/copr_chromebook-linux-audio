%global repository chromebook-linux-audio
%global maincommit 4617151f8ade809b3ef92621d75bbc2a08589741
%global deprepository alsa-ucm-conf-cros
%global depcommit 1ace2f5bfc436fdf102ce62a1eccd1faef2aaaac
%global mainversioncommit %(echo -n %{maincommit} | head -c 8)
%global depversioncommit %(echo -n %{depcommit} | head -c 8)

Name: chromebook-linux-audio
Version: 0.0.3
Release: %{mainversioncommit}.%{depversioncommit}%{?dist}
License: BSD 3-Clause License
Summary: RPM package to enable audio support on Chrome devices.
Url: https://github.com/WeirdTreeThing/%{repository}

%package debug
Summary: Enable debug for %{name}

BuildRequires: alsa-sof-firmware
BuildRequires: alsa-ucm
BuildRequires: git
BuildRequires: python3
BuildRequires: wireplumber

Requires: alsa-sof-firmware
Requires: alsa-ucm

Patch1: disable_git_clone.patch
Patch2: disable_max98357a.patch
Patch3: disable_avs_dsp_firmware.patch
Patch4: use_sof_for_apl.patch
Patch5: disable_install_package.patch
Patch6: fail_platform_stoney.patch

%define workdir %{_builddir}/%{repository}
%define datadir %{_datadir}/%{name}
%define builddatadir $RPM_BUILD_ROOT/%{datadir}

%description
RPM package to install chromebook-linux-audio to enable audio support on Chrome devices. All credits go to https://github.com/WeirdTreeThing.

This packages runs the script on install so it will work on immutable devices. If a device is NOT supported it will fail to install.

The original script comes from https://github.com/mikaelvz/chromebook-linux-audio.

%description debug
Enable debug for %{name}

%prep
# Get chromebook-linux-audio script
git clone https://github.com/WeirdTreeThing/%{repository} %{workdir}
cd %{workdir}
git reset --hard %{maincommit}

%autopatch 1
%autopatch 2
%autopatch 3
%autopatch 4
%autopatch 5
%autopatch 6

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

%files debug
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

%post debug
# Patch1 has disabled the dependency git clone in the script and
# this is now provided in this binary. Copy it to correct location
# where the script expect it. 
cp -r %{datadir}/%{deprepository} /tmp

# Run the script
cd %{datadir}
./setup-audio --enable-debug

# Cleanup
rm -rf /tmp/%{deprepository}

%preun debug
# Run the script to disable debug
cd %{datadir}
./setup-audio --disable-debug
