%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg klamav
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Summary:        Frontend for clamav
Version:		0.46
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}

License:	GPLv2+

Group:			Applications/Utilities

Url:            http://klamav.sourceforge.net/

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

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


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
chmod u+r %{buildroot}%{tde_prefix}/bin/ScanWithKlamAV

%find_lang %{tde_pkg}
	

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%attr(111,root,root) %{tde_prefix}/bin/ScanWithKlamAV
%{tde_prefix}/bin/klamav
%{tde_prefix}/bin/klammail
%{tde_prefix}/share/applications/tde/klamav.desktop
%{tde_prefix}/share/apps/klamav/
%{tde_prefix}/share/apps/konqueror/servicemenus/klamav-dropdown.desktop
%{tde_prefix}/share/doc/tde/HTML/en/klamav/
%{tde_prefix}/share/icons/hicolor/32x32/apps/klamav.png
%{tde_prefix}/share/icons/hicolor/48x48/apps/klamav.png

