%define	name	cdrdao
%define version 1.2.2
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%define release %mkrel 4
%if %build_plf
%define distsuffix plf
%endif

Summary:	Cdrdao - Write CDs in disk-at-once mode
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving/Cd burning
URL:		http://cdrdao.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/cdrdao/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	cdrecord-devel
BuildRequires: libvorbis-devel
BuildRequires: libmad-devel
BuildRequires: libao-devel
BuildRequires:	ImageMagick
BuildRequires: desktop-file-utils

%description
Writes CDs in disc-at-once (DAO) mode allowing
control over pre-gaps (length down to 0, nonzero audio
data) and sub-channel information like ISRC codes. All
data that is written to the disc must be specified with
a text file. Audio data may be in WAVE or raw format.

%package	gcdmaster
Summary:	Graphical front end to cdrdao for composing audio CDs
Group:		Archiving/Cd burning
Obsoletes:	cdrdao-xdao cdrdao-xcdrdao
BuildRequires:	libgnomeuimm2.6-devel
Provides:	cdrdao-xdao cdrdao-xcdrdao
Requires:	%{name} = %{version}
Requires(post): shared-mime-info
Requires(postun): shared-mime-info
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description    gcdmaster
gcdmaster allows the creation of toc-files for cdrdao and
can control the recording process. Its main application is
the composition of audio CDs from one or more audio files.
It supports PQ-channel editing, entry of meta data like
ISRC codes/CD-TEXT and non destructive cut of the audio data.

%if %build_plf
%package toc2mp3
Summary:	Command line mp3 encoder front end to cdrdao
Group:		Sound
BuildRequires:	liblame-devel
Requires:	%{name} = %{version}

%description toc2mp3
This is a command line mp3 encoder that converts audio CD disc images
(toc files) to mp3 files. Special care is taken that the mp3 files can
be played in sequence without having unwanted noise at the transition
points. CD-TEXT information (if available) is used to set ID3 (v2)
tags and to construct the name of the mp3 files.

This package is in PLF, as it violates some patents for mp3 encoding.
%endif

%prep
%setup -q

%build
export CXXFLAGS="%optflags -DENABLE_NLS"
%configure2_5x
%make

%install
rm -rf %buildroot
%makeinstall

# Menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%name-gcdmaster <<EOF
?package(cdrdao-gcdmaster): command="%{_bindir}/gcdmaster" needs="X11" \
icon="gcdmaster.png" section="System/Archiving/CD Burning" \
title="Gcdmaster" longtitle="Graphical front end to cdrdao for composing audio CDs" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="AudioVideo;DiscBurning" \
  --add-category="X-MandrivaLinux-System-Archiving-CDBurning" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

  
# icon
install -d $RPM_BUILD_ROOT%{_miconsdir}
install -d $RPM_BUILD_ROOT%{_iconsdir}
install -d $RPM_BUILD_ROOT%{_liconsdir}
convert -scale 16x16 xdao/gcdmaster.png $RPM_BUILD_ROOT%{_miconsdir}/gcdmaster.png
convert -scale 32x32 xdao/gcdmaster.png $RPM_BUILD_ROOT%{_iconsdir}/gcdmaster.png
ln -s %{_datadir}/pixmaps/gcdmaster.png $RPM_BUILD_ROOT%{_liconsdir}/gcdmaster.png
 
%post gcdmaster
update-mime-database %_datadir/mime > /dev/null
%{update_menus}
%{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null

%postun gcdmaster
%{clean_menus}
update-mime-database %_datadir/mime > /dev/null
if [ -x %{_bindir}/update-desktop-database ]; then %{_bindir}/update-desktop-database %{_datadir}/applications > /dev/null ; fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README README.PlexDAE
%doc %{_mandir}/man1/*
%attr(6755,root,cdwriter) %{_bindir}/cdrdao
%{_bindir}/toc2cue
%{_bindir}/toc2cddb
%{_bindir}/cue2toc
%{_datadir}/%{name}

%files	gcdmaster
%defattr(-,root,root)
%{_bindir}/gcdmaster
%{_datadir}/applications/gcdmaster.desktop
%{_datadir}/application-registry/gcdmaster.applications
%_datadir/gcdmaster
%_datadir/mime-info/gcdmaster.keys
%_datadir/mime-info/gcdmaster.mime
%_datadir/mime/packages/gcdmaster.xml
%_datadir/pixmaps/*
%{_menudir}/*
%{_iconsdir}/*

%if %build_plf
%files toc2mp3
%defattr(-,root,root)
%{_bindir}/toc2mp3
%endif

