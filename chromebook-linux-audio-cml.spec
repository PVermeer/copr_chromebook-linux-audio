%global repository chromebook-linux-audio
%global commit 99eef5cc3d2f82f451c34764f230f3d5d22239cf

Name: chromebook-linux-audio-cml
Version: 0.0.2
Release: 1%{?dist}
License: BSD 3-Clause License
Summary: RPM package to enable audio support on Chrome Comet Lake devices.
Url: https://github.com/WeirdTreeThing/%{repository}

BuildArch: noarch
BuildRequires: alsa-sof-firmware
BuildRequires: alsa-ucm
BuildRequires: wireplumber
BuildRequires: git
BuildRequires: python3

Requires: alsa-sof-firmware
Requires: alsa-ucm

Source0: %{name}-%{version}.tar.gz
Patch0: setup_audio.patch
Patch1: functions_py.patch

%define workdir %{_builddir}/%{repository}-%{commit}
%define filelist %{workdir}/filelist.txt

%description
RPM package to install chromebook-linux-audio to enable audio support on Chrome Comet Lake devices.

%prep
# cleanup
rm -rf %{workdir}

# get chromebook-linux-audio script
git clone https://github.com/WeirdTreeThing/%{repository} %{workdir}
cd %{workdir}
git reset --hard %{commit}

# patch script to save files in a specific folder
%autopatch

%build
# preparing directory
cd %{workdir}
mkdir -p %{workdir}/sysroot/lib/firmware/intel/sof-tplg
mkdir -p %{workdir}/sysroot/usr/share/alsa/ucm2/conf.d

# launch script
./setup-audio -b kled

# clean duplicate files
rm -f %{filelist}
find -L %{workdir}/sysroot -type f -print0 |
while IFS= read -r -d '' file; do
    file_search=$(echo $file | sed "s#^%{workdir}/sysroot##")
    if [ -f $file_search ]; then
        rm -f $file
    else
        echo "\"$file_search\"" >> %{filelist}
    fi
done
cat %{filelist}

%install
# install files to build directory
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -r %{workdir}/sysroot/* %{buildroot}/

# use filelist
%files -f %{filelist}

%changelog* Tue Oct 29 2024 mikaelvz <mikael@mvz.fr>
- add changelog in spec file (mikael@mvz.fr)

