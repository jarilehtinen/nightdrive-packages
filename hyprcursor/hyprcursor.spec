# Cursor theme format and library used by Hyprland. Fedora 44 ships 0.1.11 (built against
# the old hyprlang); this rebuild tracks our hyprlang.

Name:           hyprcursor
Version:        0.1.13
Release:        2%{?dist}
Summary:        Hyprland cursor format, library and utilities

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprcursor
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(hyprlang) >= 0.4.2
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(tomlplusplus)

%description
Library and utilities for the hyprcursor theme format, which supports scalable (SVG)
cursors.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config file for %{name}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/hyprcursor-util
%{_libdir}/libhyprcursor.so.*

%files devel
%{_includedir}/hyprcursor/
%{_includedir}/hyprcursor.hpp
%{_libdir}/libhyprcursor.so
%{_libdir}/pkgconfig/hyprcursor.pc

%changelog
* Sun Oct 18 2026 Christoph Pracht - 0.1.13-2
- Rebuild: the COPR files of -1 were removed with the old epoch-1 builds

* Fri Oct 16 2026 Christoph Pracht - 0.1.13-1
- Initial package
