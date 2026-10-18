# Wayland protocol definitions specific to Hyprland (global shortcuts, toplevel export, ...).

Name:           hyprland-protocols
Version:        0.7.1
Release:        1%{?dist}
Summary:        Wayland protocol extensions for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  cmake

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
* Fri Oct 16 2026 Christoph Pracht - 0.7.1-1
- Initial package
