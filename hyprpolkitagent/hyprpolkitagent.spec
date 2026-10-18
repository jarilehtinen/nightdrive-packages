# Polkit authentication agent for Hyprland: the password dialog for privileged actions.
# Started with the graphical session (systemd user unit, enabled globally in the image).

Name:           hyprpolkitagent
Version:        0.2.0
Release:        1%{?dist}
Summary:        Polkit authentication agent for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpolkitagent
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprtoolkit)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(sdbus-c++) >= 2

Requires:       polkit

%description
A polkit authentication agent for Hyprland, built on hyprtoolkit.

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
%{_libexecdir}/hyprpolkitagent
%{_userunitdir}/%{name}.service
%{_datadir}/dbus-1/services/org.hyprland.hyprpolkitagent.service

%changelog
* Fri Oct 16 2026 Christoph Pracht - 0.2.0-1
- Initial package
