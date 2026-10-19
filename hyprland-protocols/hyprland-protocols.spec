# Wayland protocol definitions specific to Hyprland (global shortcuts, toplevel export, ...).

Name:           hyprland-protocols
Version:        0.8.0
Release:        1%{?dist}
Summary:        Wayland protocol extensions for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cmake
# Its CMake project declares C since 0.8.0 (nothing is compiled, but CMake checks for a compiler)
BuildRequires:  gcc

%description
Wayland protocol extensions used by Hyprland and its portal.

%package devel
Summary:        Wayland protocol extensions for Hyprland

%description devel
Protocol XML files and pkg-config file for Hyprland's Wayland protocol extensions.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE
%{_datadir}/hyprland-protocols/
%{_datadir}/pkgconfig/hyprland-protocols.pc

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 0.8.0-1
- 0.8.0: the workspace image capture source protocol

* Fri Oct 16 2026 Christoph Pracht - 0.7.1-1
- Initial package
