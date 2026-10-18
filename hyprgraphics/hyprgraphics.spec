# Image loading and rendering helpers for Hyprland. Fedora 44 ships 0.1.5; Hyprland 0.56
# needs >= 0.5.1.

Name:           hyprgraphics
Version:        0.5.1
Epoch:          1
Release:        3%{?dist}
Summary:        Hyprland graphics and image utilities library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprgraphics
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libheif)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libjxl_cms)
BuildRequires:  pkgconfig(libjxl_threads)
BuildRequires:  pkgconfig(libmagic)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)

%description
Graphics and image utilities (PNG, JPEG, WebP, JPEG XL, HEIF, SVG loading) used across
the Hyprland ecosystem.

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
%{_libdir}/libhyprgraphics.so.*

%files devel
%{_includedir}/hyprgraphics/
%{_libdir}/libhyprgraphics.so
%{_libdir}/pkgconfig/hyprgraphics.pc

%changelog
* Mon Oct 19 2026 Jari Lehtinen <jari@feature.fi> - 1:0.5.1-3
- Epoch 1, as arcaneon/arcos's earlier builds had: an install from them otherwise never takes this package

* Sun Oct 18 2026 Christoph Pracht - 0.5.1-2
- Rebuild: the COPR files of -1 were removed with the old epoch-1 builds

* Fri Oct 16 2026 Christoph Pracht - 0.5.1-1
- Initial package
