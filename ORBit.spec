%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1
%define __libtoolize /bin/true

%define major	0
%define lib_name %mklibname %{name} %{major}

Summary:	High-performance CORBA Object Request Broker
Name:		ORBit
Version:	0.5.17
Release:	22
Group:		System/Libraries
License:	LGPLv2+ and GPLv2+
Url:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/stable/sources/ORBit//ORBit-%{version}.tar.bz2
# (fc) 0.5.17-2mdk don't add -I/usr/include to LIBIDL_INCLUDEDIR
Patch0:		ORBit-0.5.17-fixinclude.patch
# (fc) 0.5.17-9mdk fix warnings in m4 macros
Patch1:		ORBit-underquoted.patch
# (fc) 0.5.17-9mdk fix build with autoconf 2.5x and libtool 1.5
Patch2:		ORBit-0.5.17-ac25.patch
Patch3:		ORBit-0.5.17-format-strings.patch
Patch4:		ORBit-0.5.17-fix-makefile.patch
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	pkgconfig(glib)
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libtool
BuildRequires:	automake1.4
BuildRequires:	autoconf2.1

%description
ORBit is a high-performance CORBA ORB (object request
broker). It allows programs to send requests and 
receive replies from other programs, regardless of
the locations of the two programs.

You will need to install this package and the
related header files, libraries and utilities
if you want to write programs that use CORBA
technology.

%package -n %{lib_name}
Summary:	Libraries for high-performance CORBA Object Request Broker
Group:		System/Libraries

%description -n %{lib_name}
ORBit is a high-performance CORBA ORB (object request
broker). It allows programs to send requests and 
receive replies from other programs, regardless of
the locations of the two programs.

This package contains libraries used by ORBit.

%package -n %{lib_name}-devel
Summary:	Development libraries, header files and utilities for ORBit
Group:		Development/GNOME and GTK+
Requires:	glib-devel
# (gb) starting of 0.5.17 version, I can't see any change requiring a
# specific dep on release, aka rpmlint fix possible
Requires:	%{name} = %{version}-%{release}
# indent is called by orbit-idl
Requires:	indent
Requires:	tcp_wrappers-devel
Requires:	%{lib_name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
ORBit is a high-performance CORBA ORB (object request
broker) with support for the C language. It allows
programs to send requests and receive replies from
other programs, regardless of the locations of the
two programs.

This package contains the header files, libraries and 
utilities necessary to write programs that use CORBA
technology.

%prep
%setup -q
%patch0 -p1 -b .fixinclude
%patch1 -p1 -b .warnings
#%patch2 -p1 -b .ac25
%patch3 -p1
%patch4 -p1
# needed by patches 0 & 2 and fix build
# [gb] also update aclocal.m4 with new libtool.m4
rm -f configure
#aclocal-1.4
#automake-1.4
autoconf-2.13
cd libIDL
rm -f configure
libtoolize --force
#aclocal-1.4
#automake-1.4
autoconf-2.13
cd ..

# cputoolize to get updated config.{sub,guess}
%{?__cputoolize: %{__cputoolize} -c popt}
%{?__cputoolize: %{__cputoolize} -c libIDL}

%build
LIBTOOL='/usr/bin/libtool --tag=CC' %configure2_5x

#don't use macro, parallel compilation is broken
%make LIBTOOL='libtool --tag=CC' -j1

# 1 test fails on ppc
#%ifnarch ppc
#make check
#%endif

%install
%makeinstall_std  LIBTOOL=libtool

%multiarch_binaries %{buildroot}%{_bindir}/orbit-config

%multiarch_binaries %{buildroot}%{_bindir}/libIDL-config

mkdir -p %{buildroot}%{_sysconfdir}/CORBA/servers

%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/ior-decode
%{_bindir}/name-client
%{_bindir}/*-server
%{_bindir}/orbit-ird
%{_datadir}/idl
%{_sysconfdir}/CORBA

%files -n %{lib_name}
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%doc docs/*
%{_bindir}/libIDL-config
%{multiarch_bindir}/multiarch-*/libIDL-config

%{_bindir}/orbit-config
%{multiarch_bindir}/orbit-config

%{_bindir}/orbit-idl
%{_includedir}/*
%{_infodir}/libIDL.info*
%{_libdir}/*.sh
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%changelog
* Thu Aug 18 2011 GÃ¶tz Waschk <waschk@mandriva.org> 0.5.17-20mdv2012.0
+ Revision: 695115
- workaround breakage of the macro multiarch

* Tue Aug 17 2010 GÃ¶tz Waschk <waschk@mandriva.org> 0.5.17-19mdv2011.0
+ Revision: 570901
- fix build

* Thu Aug 13 2009 GÃ¶tz Waschk <waschk@mandriva.org> 0.5.17-18mdv2010.0
+ Revision: 416010
- update build deps
- fix format strings
- rebuild with system libtool
- update license

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5.17-17mdv2009.0
+ Revision: 237708
- use _disable_ld_as_needed as well
- use _disable_ld_no_undefined as it's too ugly to fix

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 03 2008 Olivier Blin <blino@mandriva.org> 0.5.17-16mdv2008.1
+ Revision: 141036
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Sep 11 2007 David Walluck <walluck@mandriva.org> 0.5.17-16mdv2008.0
+ Revision: 84304
- autoconf2.5 doesn't seem to work
- can't call aclocal-1.4 or automake-1.4 since it requires autoconf2.5
- version Obsoletes

  + Thierry Vignaud <tv@mandriva.org>
    - use %%mkrel
    - convert prereq


* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.5.17-13mdk
- Rebuild

* Mon Feb 28 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.17-12mdk
- rpmlint fixes
- remove unused stuff in orbit-config, thus colaterally making it
  multiarch (one way, not fully)

* Thu Feb 03 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.5.17-11mdk
- the -devel package needs tcp_wrappers-devel

* Mon Jan 31 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.5.17-10mdk
- don't run tests on ppc because a dynany test fails
- multiarch

* Fri Oct 01 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.17-9mdk
- Patch1 (Fedora): fix warning in m4 macro
- Patch2: fix build with autoconf 2.5x and libtool 1.5

* Fri Sep 17 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.17-8mdk
- Fix build

* Thu Feb 26 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.17-7mdk
- Distlint fixes

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.17-6mdk
- cputoolize, update aclocal.m4 with new libtool.m4

* Thu Jul 10 2003 Götz Waschk <waschk@linux-mandrake.com> 0.5.17-5mdk
- rebuild for new rpm

* Wed Jun 04 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 0.5.17-4mdk
- Rebuild to get new deps

* Tue Apr 22 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 0.5.17-3mdk
- Fix build
- mklibnamification

* Mon Jul 22 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.17-2mdk
- Patch0: no longer add -I/usr/include and -L/usr/lib for -config scripts

* Fri Jun 07 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.17-1mdk
- Release 0.5.17

* Mon Jun 03 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.16-1mdk
- Release 0.5.16
- Disable parallel compilation

* Sun Jun 02 2002 Stefan van der Eijk <stefan@eijk.nu> 0.5.15-3mdk
- BuildRequires

* Wed May 29 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.15-2mdk
- Automated rebuild with gcc 3.1-1mdk

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.15-1mdk
- Release 0.5.15

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.14-1mdk
- Release 0.5.14

* Mon Jan 07 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.13-1mdk
- Release 0.5.13
- Add missing files

* Mon Nov 05 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.12-1mdk
- Release 0.5.12

* Thu Oct 25 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.11-1mdk
- Release 0.5.11
- Libification

* Sat Oct 06 2001 Stefan van der Eijk <stefan@eijk.nu> 0.5.8-3mdk
- BuildRequires:	byacc flex

* Mon Jul 23 2001 Stefan van der Eijk <stefan@eijk.nu> 0.5.8-2mdk
- BuildRequires:	glib-devel
- Copyright --> License

* Mon May 14 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.8-1mdk
- Release 0.5.8
- Clean specfile

* Mon Feb 05 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.7-1mdk
- Release 0.5.7

* Wed Dec 20 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.6-1mdk
- Release 0.5.6

* Tue Dec 05 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.5-1mdk
- Release 0.5.5

* Fri Oct 13 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 0.5.4-1mdk
- new version
- added some files

* Tue Sep 05 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.3-2mdk
- Rebuild to remove bad rpath

* Thu Jul 27 2000 dam's <damien@mandrakesoft.com> 0.5.3-1mdk
- updated to 0.5.3

* Thu Jul 27 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.2-3mdk
- correct pre/post uninstall scripts for devel (thanks Anton)
- use more macros

* Thu Jul 20 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.5.2-2mdk
- add depend of devel on Orbit
- BM
- recreate tar file to remove date from one file

* Tue Jul 04 2000 dam's <damien@mandrakesoft.com> 0.5.2-1mdk
- updated. Make mc-4.5.51 compilable.
- cleanup spec.

* Mon Apr 10 2000 Daouda Lo <daouda@mandrakesoft.com> 0.5.1-2mdk
- adjust new group .
- cleanup spec .

* Fri Oct 01 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- 0.5.1

* Tue Sep 07 1999 Daouda LO <daouda@mandrakesoft.com>
- 0.4.94

* Wed Aug 18 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- add defattr for devel package

* Wed Aug 18 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added dependency for ORBit-devel

* Tue Aug 17 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 0.4.93

* Wed Aug 04 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- upgraded to 0.4.92

* Mon Jun 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Last CVS version from Mon Jun 28 1999.

* Sat Jun 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Add libIDL-config to ORBit-devel

* Sat May 01 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sat Apr 10 1999 Michael Fulbright <drmike@redhat.com>
- version 0.4.3

* Tue Apr 06 1999 Michael Fulbright <drmike@redhat.com>
- fixed some user permissions in the tarball

* Thu Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 0.4.1 and 0.4.2 in one day, woohoo!

* Mon Feb 22 1999 Michael Fulbright <drmike@redhat.com>
- unlibtoolize

* Mon Feb 15 1999 Michael Fulbright <drmike@redhat.com>
- updated to version 0.3.98

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- updated to version 0.3.97

* Fri Feb 05 1999 Michael Fulbright <drmike@redhat.com>
- updated to version 0.3.96

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- updated to version 0.3.91

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated for GNOME freeze, version 0.3.90

* Mon Nov 23 1998 Pablo Saratxaga <srtxg@chanae.alphanet.ch>
- improved %%files section, and added use of %%{prefix} and install-info
  (well,... no. The info file has not dir info inside, commented out)

