%{?_with_plf: %{expand: %%global build_plf 1}}

#####################
# Hardcode PLF build
%define build_plf 0
#####################

%if %{build_plf}
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

Name:		cdrdao
Version:	1.2.3
Release:	10%{?extrarelsuffix}
Summary:	Cdrdao - Write CDs in disk-at-once mode
License:	GPLv2+
Group:		Archiving/Cd burning
URL:		http://cdrdao.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/cdrdao/%{name}-%{version}.tar.bz2
Patch1:		mkisofs-changelog.patch
#gw from Fedora: fix version printing needed by k3b
Patch3:		cdrdao-1.2.3-version.patch
Patch10:	cdrdao-1.2.2-fix-str-fmt.patch
Patch11:	cdrdao-1.2.3-stat.patch
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(ao)
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

%description
Writes CDs in disc-at-once (DAO) mode allowing control over pre-gaps
(length down to 0, nonzero audio data) and sub-channel information
like ISRC codes. All data that is written to the disc must be
specified with a text file. Audio data may be in WAVE or raw format.

%if %{build_plf}
This package is in restricted as it violates some patents for MP3 encoding.
%endif

%package	gcdmaster
Summary:	Graphical front end to cdrdao for creating audio CDs
Group:		Archiving/Cd burning
BuildRequires:	pkgconfig(libgnomeuimm-2.6)
Provides:	cdrdao-xdao
Provides:	cdrdao-xcdrdao
Requires:	%{name} = %{version}

%description gcdmaster
gcdmaster allows the creation of toc-files for cdrdao and can control
the recording process. Its main application is the creation of audio
CDs from one or more audio files. It supports PQ-channel editing,
entry of meta data like ISRC codes/CD-TEXT and non-destructive cut of
the audio data.

%if %{build_plf}
%package	toc2mp3
Summary:	Command line MP3 encoder front end to cdrdao
Group:		Sound
BuildRequires:	liblame-devel
Requires:	%{name} = %{version}

%description	toc2mp3
This is a command line MP3 encoder that converts audio CD disc images
(toc files) to MP3 files. Special care is taken that the MP3 files can
be played in sequence without having unwanted noise at the transition
points. CD-TEXT information (if available) is used to set ID3 (v2)
tags and to construct the name of the MP3 files.

This package is in restricted as it violates some patents for MP3 encoding.
%endif

%prep
%setup -q
%patch1 -p1 -b .changelog
%patch3 -p1
%patch10 -p0 -b .str
%patch11 -p1 -b .stat

%build
export CXXFLAGS="%{optflags} -DENABLE_NLS"
%configure2_5x
%make

%install
%makeinstall

# Menu
perl -pi -e 's,gcdmaster.png,gcdmaster,g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="X-Fedora" \
  --remove-key="Encoding" \
  --add-category="GTK" \
  --add-category="AudioVideo" \
  --add-category="DiscBurning" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 16 xdao/gcdmaster.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/gcdmaster.png
convert -scale 32 xdao/gcdmaster.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/gcdmaster.png
install -m 644 xdao/gcdmaster.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/gcdmaster.png

%files
%doc README README.PlexDAE
%doc %{_mandir}/man1/*
%attr(6755,root,cdwriter) %{_bindir}/cdrdao
%{_bindir}/toc2cue
%{_bindir}/toc2cddb
%{_bindir}/cue2toc
%{_datadir}/%{name}

%files gcdmaster
%{_sysconfdir}/gconf/schemas/gcdmaster.schemas
%{_bindir}/gcdmaster
%{_datadir}/applications/gcdmaster.desktop
%{_datadir}/application-registry/gcdmaster.applications
%{_datadir}/gcdmaster
%{_datadir}/mime-info/gcdmaster.keys
%{_datadir}/mime-info/gcdmaster.mime
%{_datadir}/mime/packages/gcdmaster.xml
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*

%if %{build_plf}
%files toc2mp3
%{_bindir}/toc2mp3
%endif

