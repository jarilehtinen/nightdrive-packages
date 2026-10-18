# Hyprland's screen locker. Not in Fedora 44.

Name:           hyprlock
Version:        0.9.6
Release:        2%{?dist}
Summary:        Screen locker for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprlock
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hyprwayland-scanner-devel >= 0.4.4
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprgraphics) >= 0.1.6
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.11.0
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.35
BuildRequires:  pkgconfig(xkbcommon)

%description
A simple, yet fast, multi-threaded and GPU-accelerated screen lock for Hyprland.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install
# The example config goes in the docs, as in the arcos package (nothing reads /usr/share/hypr/hyprlock.conf)
rm -rf %{buildroot}%{_datadir}/hypr

%files
%license LICENSE
%doc README.md assets/example.conf
%config(noreplace) %{_sysconfdir}/pam.d/hyprlock
%{_bindir}/hyprlock

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 0.9.6-2
- Rebuild: an install from arcaneon/arcos had the same version, built against its libraries

* Sun Oct 18 2026 Jari Lehtinen <jari@feature.fi> - 0.9.6-1
- Initial package for the Nightdrive COPR
