# Hyprland's XDG desktop portal backend: screencasting, screenshots, global shortcuts.

Name:           xdg-desktop-portal-hyprland
Version:        1.4.1
Epoch:          1
Release:        2%{?dist}
Summary:        XDG desktop portal backend for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  hyprwayland-scanner-devel >= 0.4.2
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(hyprlang) >= 0.2.0
BuildRequires:  pkgconfig(hyprutils) >= 0.2.6
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3) >= 1.1.82
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(sdbus-c++) >= 2.0.0
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)

Requires:       dbus
Requires:       pipewire
Requires:       xdg-desktop-portal
# File chooser and other interfaces this backend doesn't implement.
Recommends:     xdg-desktop-portal-gtk

%description
An XDG desktop portal backend for Hyprland: screencasting, screenshots, global shortcuts
and a share picker for choosing what to share.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%{_bindir}/hyprland-share-picker
%{_libexecdir}/%{name}
%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/%{name}.service

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 1:1.4.1-2
- Epoch 1, as arcaneon/arcos's earlier builds had: an install from them otherwise never takes this package

* Fri Oct 16 2026 Christoph Pracht - 1.4.1-1
- Initial package
