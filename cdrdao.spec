%global optflags %{optflags} -Wno-narrowing -Wno-c++11-narrowing

#define _disable_rebuild_configure 1

Name:		cdrdao
Version:	1.2.5
Release:	1
Summary:	Write CDs in disk-at-once mode
License:	GPLv2+
Group:		Archiving/Cd burning
Url:		https://cdrdao.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/cdrdao/%{name}-%{version}.tar.bz2
Patch1:		mkisofs-changelog.patch

BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(ao)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:  pkgconfig(gtkmm-3.0)

%description
Writes CDs in disc-at-once (DAO) mode allowing control over pre-gaps
(length down to 0, nonzero audio data) and sub-channel information
like ISRC codes. All data that is written to the disc must be
specified with a text file. Audio data may be in WAVE or raw format.

%package	toc2mp3
Summary:	Command line MP3 encoder front end to cdrdao
Group:		Sound
BuildRequires:	lame-devel
Requires:	%{name} = %{version}

%description	toc2mp3
This is a command line MP3 encoder that converts audio CD disc images
(toc files) to MP3 files. Special care is taken that the MP3 files can
be played in sequence without having unwanted noise at the transition
points. CD-TEXT information (if available) is used to set ID3 (v2)
tags and to construct the name of the MP3 files.

This package is in restricted as it violates some patents for MP3 encoding.

%package	gcdmaster
Summary:	Graphical frontend for the cdrdao CD writing tool
Group:		Sound
Requires:	%{name} = %{EVRD}

%description	gcdmaster
Graphical frontend for the cdrdao CD writing tool

%prep
%autosetup -p1
# Remove ancient copies of autoconf internal files
rm -f scsilib/conf/*.m4
# And a check for prehistoric stuff
sed -i -e 's,^AM_GCONF,#AM_GCONF,' configure.ac

%build
export CXXFLAGS="%{optflags} -DENABLE_NLS"
%configure
%make_build

%install
%make_install

%files
%doc README README.PlexDAE
%doc %{_mandir}/man1/*
%attr(6755,root,cdwriter) %{_bindir}/cdrdao
%{_bindir}/toc2cue
%{_bindir}/toc2cddb
%{_bindir}/cue2toc
%{_datadir}/%{name}

%files gcdmaster
%{_bindir}/gcdmaster
%{_datadir}/application-registry/gcdmaster.applications
%{_datadir}/applications/gcdmaster.desktop
%{_datadir}/gcdmaster/glade/Preferences.glade
%{_datadir}/gcdmaster/glade/ProjectChooser.glade
%{_datadir}/glib-2.0/schemas/org.gnome.gcdmaster.gschema.xml
%{_datadir}/mime-info/gcdmaster.keys
%{_datadir}/mime-info/gcdmaster.mime
%{_datadir}/mime/packages/gcdmaster.xml
%{_datadir}/pixmaps/gcdmaster-doc.png
%{_datadir}/pixmaps/gcdmaster.png

%files toc2mp3
%{_bindir}/toc2mp3
