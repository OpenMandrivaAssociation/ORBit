%define major	0
%define lib_name %mklibname %{name} %{major}

Summary: High-performance CORBA Object Request Broker
Name: ORBit
Version: 0.5.17
Release: 13mdk
Source0: ftp://ftp.gnome.org/pub/GNOME/stable/sources/ORBit//ORBit-%{version}.tar.bz2
# (fc) 0.5.17-2mdk don't add -I/usr/include to LIBIDL_INCLUDEDIR
Patch0:  ORBit-0.5.17-fixinclude.patch
# (fc) 0.5.17-9mdk fix warnings in m4 macros
Patch1:	 ORBit-underquoted.patch
# (fc) 0.5.17-9mdk fix build with autoconf 2.5x and libtool 1.5
Patch2:	 ORBit-0.5.17-ac25.patch
Group: System/Libraries
Url: http://www.gnome.org/
License: LGPL/GPL
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	glib-devel
BuildRequires:	tcp_wrappers-devel
%if %mdkversion >= 1010
BuildRequires:  automake1.4
BuildRequires:  autoconf2.5
%endif

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
Summary: Libraries for high-performance CORBA Object Request Broker
Group: System/Libraries

%description -n %{lib_name}
ORBit is a high-performance CORBA ORB (object request
broker). It allows programs to send requests and 
receive replies from other programs, regardless of
the locations of the two programs.

This package contains libraries used by ORBit.

%package -n %{lib_name}-devel
Summary: Development libraries, header files and utilities for ORBit
Group: Development/GNOME and GTK+
Requires: glib-devel
# (gb) starting of 0.5.17 version, I can't see any change requiring a
# specific dep on release, aka rpmlint fix possible
Requires: %{name} = %{version}
Requires(post): info-install
Requires(preun): info-install
# indent is called by orbit-idl
Requires: indent
Requires: tcp_wrappers-devel
Requires: %{lib_name} = %{version}
Obsoletes:	%{name}-devel
Provides: %{name}-devel = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}


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
%patch2 -p1 -b .ac25

# needed by patches 0 & 2 and fix build
# [gb] also update aclocal.m4 with new libtool.m4
rm -f configure
aclocal-1.4 && automake-1.4 && autoconf
cd libIDL
rm -f configure
libtoolize --force
aclocal-1.4 && automake-1.4 && autoconf
cd ..

# cputoolize to get updated config.{sub,guess}
%{?__cputoolize: %{__cputoolize} -c popt}
%{?__cputoolize: %{__cputoolize} -c libIDL}

%build

%configure2_5x

#don't use macro, parallel compilation is broken
make

# 1 test fails on ppc
%ifnarch ppc
make check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/orbit-config
%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/libIDL-config

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/CORBA/servers

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-devel
%_install_info libIDL.info

%preun -n %{lib_name}-devel
%_remove_install_info libIDL.info

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/ior-decode
%{_bindir}/name-client
%{_bindir}/*-server
%{_bindir}/orbit-ird
%{_datadir}/idl
%{_sysconfdir}/CORBA

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc docs/*
%{_bindir}/libIDL-config
%multiarch %{_bindir}/multiarch-*/libIDL-config
%{_bindir}/orbit-config
%multiarch %{multiarch_bindir}/orbit-config
%{_bindir}/orbit-idl
%{_includedir}/*
%{_infodir}/libIDL.info*
%{_libdir}/*.sh
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

