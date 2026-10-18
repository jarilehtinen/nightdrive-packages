# Shared utility library of the Hyprland stack. Fedora 44 ships 0.7.1; Hyprland 0.56 needs >= 0.14.

Name:           hyprutils
Version:        0.14.2
Release:        1%{?dist}
Summary:        Hyprland utilities library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprutils
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(pixman-1)

%description
Small C++ library of utilities used across the Hyprland ecosystem.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

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
%{_libdir}/libhyprutils.so.*

%files devel
%{_includedir}/hyprutils/
%{_libdir}/libhyprutils.so
%{_libdir}/pkgconfig/hyprutils.pc

%changelog
* Fri Oct 16 2026 Christoph Pracht - 0.14.2-1
- Initial package
