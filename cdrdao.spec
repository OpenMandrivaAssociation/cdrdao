%define	name	cdrdao
%define version 1.2.3
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%define release %mkrel 5
%define fname %name-%version
%if %build_plf
%define distsuffix plf
%if %mdvver >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

Summary:	Cdrdao - Write CDs in disk-at-once mode
Name:		%{name}
Version:	%{version}
Release:	%{release}%{?extrarelsuffix}
License:	GPLv2+
Group:		Archiving/Cd burning
URL:		http://cdrdao.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/cdrdao/%{fname}.tar.bz2
Patch1:		mkisofs-changelog.patch 
#gw from Fedora: fix version printing needed by k3b
Patch3:		cdrdao-1.2.3-version.patch
Patch10:	cdrdao-1.2.2-fix-str-fmt.patch
Patch11:	cdrdao-1.2.3-stat.patch
BuildRequires:	libvorbis-devel
BuildRequires:	libmad-devel
BuildRequires:	libao-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Writes CDs in disc-at-once (DAO) mode allowing control over pre-gaps
(length down to 0, nonzero audio data) and sub-channel information
like ISRC codes. All data that is written to the disc must be
specified with a text file. Audio data may be in WAVE or raw format.
%if %build_plf

This package is in PLF as it violates some patents for MP3 encoding.
%endif

%package	gcdmaster
Summary:	Graphical front end to cdrdao for creating audio CDs
Group:		Archiving/Cd burning
Obsoletes:	cdrdao-xdao cdrdao-xcdrdao
BuildRequires:	libgnomeuimm2.6-devel
Provides:	cdrdao-xdao cdrdao-xcdrdao

Requires:		%{name} = %{version}
Requires(post):		shared-mime-info
Requires(postun):	shared-mime-info
Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

%description    gcdmaster
gcdmaster allows the creation of toc-files for cdrdao and can control
the recording process. Its main application is the creation of audio
CDs from one or more audio files. It supports PQ-channel editing,
entry of meta data like ISRC codes/CD-TEXT and non-destructive cut of
the audio data.

%if %build_plf
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

This package is in PLF as it violates some patents for MP3 encoding.
%endif

%prep
%setup -q -n %fname
%patch1 -p1 -b .changelog
%patch3 -p1
%patch10 -p0 -b .str
%patch11 -p1 -b .stat

%build
export CXXFLAGS="%optflags -DENABLE_NLS"
%configure2_5x
%make

%install
rm -rf %buildroot
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
 
%define schemas gcdmaster
%if %mdkversion < 200900
%post gcdmaster
%post_install_gconf_schemas %schemas
%{update_menus}
%{update_icon_cache hicolor}

%postun gcdmaster
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%preun gcdmaster
%preun_uninstall_gconf_schemas %schemas

%clean
rm -rf %{buildroot}

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
%_sysconfdir/gconf/schemas/gcdmaster.schemas
%{_bindir}/gcdmaster
%{_datadir}/applications/gcdmaster.desktop
%{_datadir}/application-registry/gcdmaster.applications
%{_datadir}/gcdmaster
%{_datadir}/mime-info/gcdmaster.keys
%{_datadir}/mime-info/gcdmaster.mime
%{_datadir}/mime/packages/gcdmaster.xml
%{_datadir}/pixmaps/*
%{_iconsdir}/hicolor/*/apps/*

%if %build_plf
%files toc2mp3
%defattr(-,root,root)
%{_bindir}/toc2mp3
%endif

