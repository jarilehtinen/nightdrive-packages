# Build-time code generator for Wayland protocols, used by aquamarine, Hyprland and the portal.

Name:           hyprwayland-scanner
Version:        0.4.6
Release:        2%{?dist}
Summary:        Hyprland implementation of wayland-scanner

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pugixml)

%description
A Hyprland implementation of wayland-scanner that generates C++ bindings for Wayland
protocols.

%package devel
Summary:        CMake and pkg-config files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
CMake config and pkg-config file for finding %{name} at build time.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/hyprwayland-scanner

%files devel
%{_libdir}/cmake/hyprwayland-scanner/
%{_libdir}/pkgconfig/hyprwayland-scanner.pc

%changelog
* Sun Oct 18 2026 Christoph Pracht - 0.4.6-2
- Rebuild: the COPR files of -1 were removed with the old epoch-1 builds

* Fri Oct 16 2026 Christoph Pracht - 0.4.6-1
- Initial package
