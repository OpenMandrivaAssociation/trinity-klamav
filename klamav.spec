#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg klamav
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications
%define tde_tdeappdir %{tde_appdir}/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:			trinity-%{tde_pkg}
Summary:        Frontend for clamav
Version:		0.46
Release:		%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

Group:			Applications/Utilities

Vendor:			Trinity Project
Packager:		Francois Andriot <francois.andriot@free.fr>
#URL:			http://www.trinitydesktop.org/
Url:            http://klamav.sourceforge.net/

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tde-cmake >= %{tde_version}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext
BuildRequires:	curl-devel
BuildRequires:	gmp-devel

# SQLITE3 support
BuildRequires:  pkgconfig(sqlite3)

#BuildRequires:	unsermake

# CLAMAV support
BuildRequires:  clamav
BuildRequires:  clamav-devel
Requires:		clamav

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
A TDE front-end for the Clam AntiVirus antivirus toolkit.

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DBUILD_ALL=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build
chmod u+r %{buildroot}%{tde_bindir}/ScanWithKlamAV

%find_lang %{tde_pkg}
	

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%attr(111,root,root) %{tde_bindir}/ScanWithKlamAV
%{tde_bindir}/klamav
%{tde_bindir}/klammail
%{tde_tdeappdir}/klamav.desktop
%{tde_datadir}/apps/klamav/
%{tde_datadir}/apps/konqueror/servicemenus/klamav-dropdown.desktop
%{tde_tdedocdir}/HTML/en/klamav/
%{tde_datadir}/icons/hicolor/32x32/apps/klamav.png
%{tde_datadir}/icons/hicolor/48x48/apps/klamav.png

