# Hyprland's IPC wire protocol library (hyprpm, start-hyprland). Not in Fedora 44.

Name:           hyprwire
Version:        0.3.1
Release:        2%{?dist}
Summary:        Hyprland wire protocol library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwire
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprutils) >= 0.9.0
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(pugixml)

%description
A fast and consistent wire protocol for IPC, used by Hyprland.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config files and the hyprwire-scanner code generator for %{name}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprwire.so.*

%files devel
%{_bindir}/hyprwire-scanner
%{_includedir}/hyprwire/
%{_libdir}/libhyprwire.so
%{_libdir}/pkgconfig/hyprwire.pc
%{_libdir}/pkgconfig/hyprwire-scanner.pc
%{_libdir}/cmake/hyprwire-scanner/

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 0.3.1-2
- Rebuild: an install from arcaneon/arcos had the same version, built against its libraries

* Sun Oct 18 2026 Jari Lehtinen <jari@feature.fi> - 0.3.1-1
- Initial package for the Nightdrive COPR
