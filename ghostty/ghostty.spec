# Ghostty, a terminal: Nightdrive offers it in Install › Software › Terminals. Not in Fedora 44 nor on Flathub.
# Ghostty needs one exact Zig release (build.zig.zon's minimum_zig_version) and Fedora has a newer one, so the build
# uses Zig's own static build (Source1/2). Its Zig dependencies are fetched once into Source3 by sources.sh when the
# SRPM is made (.copr/Makefile): the build itself is offline (PACKAGING.md in the source).

%global zig_version 0.15.2
# Zig's binary has no build id and its own debug info layout
%global debug_package %{nil}

Name:           ghostty
Version:        1.3.1
Release:        1%{?dist}
Summary:        Fast, native terminal emulator with GPU rendering

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
# The release tarball, not GitHub's: it has the generated UI files (no blueprint-compiler needed)
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://ziglang.org/download/%{zig_version}/zig-x86_64-linux-%{zig_version}.tar.xz
Source2:        https://ziglang.org/download/%{zig_version}/zig-aarch64-linux-%{zig_version}.tar.xz
Source3:        ghostty-%{version}-deps.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  gettext
BuildRequires:  ncurses
BuildRequires:  systemd-rpm-macros
# The man pages and their HTML
BuildRequires:  pandoc-cli


%description
Ghostty is a fast, feature-rich terminal emulator that uses platform-native UI (GTK on Linux) and GPU acceleration.

%prep
%setup -q
tar -xf %{_sourcedir}/zig-%{_arch}-linux-%{zig_version}.tar.xz
mkdir cache && tar -xzf %{SOURCE3} -C cache

%build
# zig build compiles and installs in one go: in %%install, as rpmbuild empties the buildroot when that starts

%install
# Fedora's libraries where they are stable; the ones Ghostty pins tightly (glslang, SPIRV-Cross, simdutf, highway) stay
# bundled
DESTDIR=%{buildroot} ZIG_GLOBAL_CACHE_DIR=$PWD/zig-cache ./zig-%{_arch}-linux-%{zig_version}/zig build \
    --prefix %{_prefix} \
    --system $PWD/cache/p \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Dversion-string=%{version} \
    -fsys=fontconfig -fsys=freetype -fsys=harfbuzz -fsys=libpng -fsys=zlib -fsys=oniguruma -fsys=gtk4-layer-shell \
    -fno-sys=glslang -fno-sys=spirv-cross -fno-sys=simdutf -fno-sys=highway
# Fedora's ncurses-term owns the ghostty terminfo entry, not xterm-ghostty (the TERM Ghostty sets)
rm %{buildroot}%{_datadir}/terminfo/g/ghostty
# libghostty-vt is for other programs embedding Ghostty's parser: not needed by the app
rm -rf %{buildroot}%{_prefix}/lib/libghostty-vt* %{buildroot}%{_includedir}/ghostty %{buildroot}%{_datadir}/pkgconfig/libghostty-vt.pc
%find_lang com.mitchellh.ghostty

%files -f com.mitchellh.ghostty.lang
%license LICENSE
%{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty/
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_datadir}/man/man1/ghostty.1*
%{_datadir}/man/man5/ghostty.5*
%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/nvim/site/*/ghostty.vim
%{_userunitdir}/app-com.mitchellh.ghostty.service
%{_datadir}/vim/vimfiles/*/ghostty.vim
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/zsh/site-functions/_ghostty

%changelog
* Tue Oct 20 2026 Jari Lehtinen <jari@feature.fi> - 1.3.1-1
- First package, for Nightdrive's Install › Software › Terminals
