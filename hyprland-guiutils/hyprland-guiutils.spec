# Small GUI helpers Hyprland launches itself (dialogs, run prompt, welcome/update screens).
# Hyprland warns at every start when they're missing.

Name:           hyprland-guiutils
Version:        0.2.2
Release:        2%{?dist}
Summary:        GUI utilities used by Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-guiutils
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# The Qt utilities this replaces have the same programs (hyprland-dialog, -update-screen, -donate-screen), and
# hyprland-qt-support was only their Qt style
Obsoletes:      hyprland-qtutils < 0.2
Obsoletes:      hyprland-qt-support < 0.2

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)

%description
GUI utilities that Hyprland starts on its own: hyprland-dialog, hyprland-run,
hyprland-welcome, hyprland-update-screen and hyprland-donate-screen.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/hyprland-dialog
%{_bindir}/hyprland-donate-screen
%{_bindir}/hyprland-run
%{_bindir}/hyprland-update-screen
%{_bindir}/hyprland-welcome

%changelog
* Sun Oct 18 2026 Jari Lehtinen <jari@feature.fi> - 0.2.2-2
- Obsoletes hyprland-qtutils and hyprland-qt-support (Nightdrive COPR)

* Fri Oct 16 2026 Christoph Pracht - 0.2.2-1
- Initial package
