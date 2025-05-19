# Create an option to build locally without fetchting own repo
# for sourcing and patching
%bcond local 0

# Source repo 1
%global author WeirdTreeThing
%global source chromebook-linux-audio
%global sourcerepo https://github.com/WeirdTreeThing/chromebook-linux-audio
%global commit e02d690a8b46891795c3f8e3dbd192d41a8cee96
%global versioncommit %(echo -n %{commit} | head -c 8)

# Source repo 2
%global author2 WeirdTreeThing
%global source2 alsa-ucm-conf-cros
%global sourcerepo2 https://github.com/WeirdTreeThing/alsa-ucm-conf-cros
%global commit2 8eb9716a8a4d9cfcb1360a1325c7fe00f90fac6e
%global versioncommit2 %(echo -n %{commit2} | head -c 8)

# Own copr repo
%global coprrepo https://github.com/PVermeer/copr_chromebook-linux-audio
%global coprsource copr_chromebook-linux-audio

Name: chromebook-linux-audio
Version: 0.0.8
Release: 5.%{versioncommit}.%{versioncommit2}%{?dist}
License: BSD 3-Clause License
Summary: RPM package to enable audio support on Chrome devices.
Url: %{coprrepo}

%package debug
Summary: Enable debug for %{name}

BuildRequires: git

Requires: alsa-sof-firmware
Requires: alsa-ucm
Requires: python3
Requires: wireplumber 

%define workdir %{_builddir}/%{name}
%define coprdir %{workdir}/%{coprsource}
%define sourcedir %{workdir}/%{source}
%define sourcedir2 %{workdir}/%{source2}
%define datadir %{_datadir}/%{name}

%description
RPM package to install chromebook-linux-audio to enable audio support on Chrome devices. All credits go to https://github.com/%{author}.

This packages runs the script on install so it will work on immutable devices. If a device is NOT supported it will fail to install.

The original script comes from https://github.com/mikaelvz/chromebook-linux-audio.

%description debug
Enable debug for %{name}

%prep
# To apply working changes handle sources / patches locally
# COPR should clone the commited changes
%if %{with local}
  # Get sources / patches - local build
  mkdir -p %{coprdir}
  cp -r %{_topdir}/SOURCES/* %{coprdir}
%else
  # Get sources / patches - COPR build
  git clone %{coprrepo} %{coprdir}
  cd %{coprdir}
  rm -rf .git
  cd %{workdir}
%endif

# Get chromebook-linux-audio script
git clone %{sourcerepo} %{sourcedir}
cd %{sourcedir}
git reset --hard %{commit}

git apply %{coprdir}/patches/%{source}/*.patch

rm -rf .git
cd %{workdir}

# Get chromebook-linux-audio script dependency
git clone %{sourcerepo2} %{sourcedir2}
cd %{sourcedir2}
git reset --hard %{commit2}

rm -rf .git
cd %{workdir}

%build

%install
mkdir -p %{buildroot}/%{datadir}/%{source}
mkdir -p %{buildroot}/%{datadir}/%{source2}

cp -r %{workdir}/%{source}/* %{buildroot}/%{datadir}/%{source}
cp -r %{workdir}/%{source2}/* %{buildroot}/%{datadir}/%{source2}

%files
%{datadir}

%check

%files debug
%{datadir}

%post
# Copy source to the correct location where the script expect it. 
cp -r %{datadir}/%{source2} /tmp

# Run the script
cd %{datadir}/%{source}
./setup-audio

# Cleanup
rm -rf /tmp/%{source2}

%post debug
# Copy source to the correct location where the script expect it. 
cp -r %{datadir}/%{source2} /tmp

# Run the script
cd %{datadir}/%{source}
./setup-audio --enable-debug

# Cleanup
rm -rf /tmp/%{source2}

%preun debug
# Run the script to disable debug
cd %{datadir}/%{source}
./setup-audio --disable-debug
