# Hyprland's idle daemon. Not in Fedora 44.

Name:           hypridle
Version:        0.1.8
Release:        2%{?dist}
Summary:        Idle daemon for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hypridle
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hyprwayland-scanner-devel >= 0.4.4
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(hyprland-protocols) >= 0.6.0
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.2.0
BuildRequires:  pkgconfig(sdbus-c++) >= 0.2.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Hyprland's idle management daemon: runs commands after a time of inactivity, such as
locking the screen or turning it off.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install
# The example config goes in the docs, as in the arcos package
rm -rf %{buildroot}%{_datadir}/hypr

%files
%license LICENSE
%doc README.md assets/example.conf
%{_bindir}/hypridle
%{_userunitdir}/hypridle.service

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 0.1.8-2
- Rebuild: an install from arcaneon/arcos had the same version, built against its libraries

* Sun Oct 18 2026 Jari Lehtinen <jari@feature.fi> - 0.1.8-1
- Initial package for the Nightdrive COPR
