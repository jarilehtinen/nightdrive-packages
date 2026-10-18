# Parser for Hyprland's classic config language, still used by the portal and hypr* tools.
# Fedora 44 ships 0.6.4; Hyprland 0.56 needs >= 0.6.7.

Name:           hyprlang
Version:        0.6.8
Epoch:          1
Release:        3%{?dist}
Summary:        Official implementation library for the hypr config language

License:        LGPL-3.0-only
URL:            https://github.com/hyprwm/hyprlang
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(hyprutils) >= 0.7.1

%description
Library for parsing the hypr configuration language.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Headers and pkg-config file for %{name}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/libhyprlang.so.*

%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/libhyprlang.so
%{_libdir}/pkgconfig/hyprlang.pc

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 1:0.6.8-3
- Epoch 1, as arcaneon/arcos's earlier builds had: an install from them otherwise never takes this package

* Sun Oct 18 2026 Christoph Pracht - 0.6.8-2
- Rebuild: the COPR files of -1 were removed with the old epoch-1 builds

* Fri Oct 16 2026 Christoph Pracht - 0.6.8-1
- Initial package
