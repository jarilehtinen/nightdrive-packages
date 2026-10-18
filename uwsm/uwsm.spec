# Universal Wayland Session Manager: runs Hyprland as a systemd user session, so apps,
# services and autostart are managed by systemd and shut down cleanly on logout.

Name:           uwsm
Version:        0.27.1
Release:        1%{?dist}
Summary:        Universal Wayland Session Manager

License:        MIT
URL:            https://github.com/Vladimir-csp/uwsm
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  meson
BuildRequires:  python3-devel
# meson checks for the runtime modules at configure time.
BuildRequires:  python3-dbus
BuildRequires:  python3-pyxdg
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros

Requires:       python3-dbus
Requires:       python3-pyxdg
# waitpid binds the login session to the graphical session.
Requires:       util-linux
# whiptail, for `uwsm select`
Recommends:     newt

%description
uwsm wraps standalone Wayland compositors into a set of systemd units on the fly, binding
the graphical session to the login session and managing XDG autostart, environment and
application slices.

%prep
%autosetup -p1

%build
%meson \
    -Duuctl=enabled \
    -Duwsm-app=enabled \
    -Dfumon=disabled \
    -Dttyautolock=disabled \
    -Dwait-tray=disabled
%meson_build

%install
%meson_install
# meson installs the licence itself; %%license below takes it from the source tree.
rm -rf %{buildroot}%{_datadir}/licenses/%{name}

%files
%license LICENSE
%doc %{_docdir}/%{name}/
%{_bindir}/uwsm
%{_bindir}/uwsm-app
%{_bindir}/uuctl
%{_bindir}/uwsm-terminal
%{_bindir}/uwsm-terminal-scope
%{_bindir}/uwsm-terminal-service
%{_datadir}/%{name}/
%{_datadir}/applications/uuctl.desktop
%{_libexecdir}/%{name}/
%{_userunitdir}/*
%{_mandir}/man1/uwsm.1*
%{_mandir}/man1/uwsm-app.1*
%{_mandir}/man1/uuctl.1*
%{_mandir}/man3/uwsm-plugins.3*

%changelog
* Fri Oct 16 2026 Christoph Pracht - 0.27.1-1
- Initial package
