# Hyprland 0.55+ is configured in Lua 5.5; Fedora 44 only has Lua 5.4. This package installs
# 5.5 alongside it (versioned library, headers and pkg-config name), so nothing in Fedora
# that uses the system Lua is affected.

%global major_minor 5.5

Name:           lua%{major_minor}
Version:        5.5.1
Release:        1%{?dist}
Summary:        Lua %{major_minor} language engine, installable alongside the system Lua

License:        MIT
URL:            https://www.lua.org/
Source0:        https://www.lua.org/ftp/lua-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  readline-devel

%description
Lua is a powerful, efficient, lightweight, embeddable scripting language. This package
provides Lua %{major_minor} as a versioned shared library (liblua-%{major_minor}.so) and the
lua%{major_minor} interpreter, without conflicting with the system Lua.

%package devel
Summary:        Development files for Lua %{major_minor}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config file (lua%{major_minor}) for building against Lua %{major_minor}.

%prep
%autosetup -n lua-%{version}
# Module search paths: /usr instead of /usr/local, and the arch libdir for C modules.
sed -i \
    -e 's|^#define LUA_ROOT\t"/usr/local/"|#define LUA_ROOT\t"%{_prefix}/"|' \
    -e 's|^#define LUA_CDIR\tLUA_ROOT "lib/lua/" LUA_VDIR "/"|#define LUA_CDIR\t"%{_libdir}/lua/" LUA_VDIR "/"|' \
    src/luaconf.h
grep -qP '^#define LUA_ROOT\t"%{_prefix}/"' src/luaconf.h
grep -qP '^#define LUA_CDIR\t"%{_libdir}/lua/"' src/luaconf.h

%build
cd src
core="lapi lcode lctype ldebug ldo ldump lfunc lgc llex lmem lobject lopcodes lparser lstate
      lstring ltable ltm lundump lvm lzio lauxlib lbaselib lcorolib ldblib liolib lmathlib
      loadlib loslib lstrlib ltablib lutf8lib linit"
for o in $core; do
    gcc %{optflags} -fPIC -DLUA_USE_LINUX -c "$o.c" -o "$o.o"
done
gcc %{build_ldflags} -shared -Wl,-soname,liblua-%{major_minor}.so \
    -o liblua-%{major_minor}.so $(for o in $core; do echo "$o.o"; done) -lm -ldl
gcc %{optflags} -DLUA_USE_LINUX -DLUA_USE_READLINE -c lua.c -o lua.o
gcc %{build_ldflags} -Wl,-E -o lua%{major_minor} lua.o -L. -llua-%{major_minor} -lm -ldl -lreadline

%install
install -Dpm 0755 src/liblua-%{major_minor}.so %{buildroot}%{_libdir}/liblua-%{major_minor}.so
install -Dpm 0755 src/lua%{major_minor} %{buildroot}%{_bindir}/lua%{major_minor}
install -d %{buildroot}%{_includedir}/lua%{major_minor}
install -pm 0644 src/lua.h src/luaconf.h src/lualib.h src/lauxlib.h src/lua.hpp \
    %{buildroot}%{_includedir}/lua%{major_minor}/
install -d %{buildroot}%{_libdir}/lua/%{major_minor} %{buildroot}%{_datadir}/lua/%{major_minor}
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/lua%{major_minor}.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/lua%{major_minor}

Name: Lua
Description: Lua %{major_minor} language engine
Version: %{version}
Libs: -L\${libdir} -llua-%{major_minor}
Libs.private: -lm -ldl
Cflags: -I\${includedir}
EOF

%check
LD_LIBRARY_PATH=src src/lua%{major_minor} -e 'assert(_VERSION == "Lua %{major_minor}")'

%files
%license doc/readme.html
%{_bindir}/lua%{major_minor}
%{_libdir}/liblua-%{major_minor}.so
%dir %{_libdir}/lua/%{major_minor}
%dir %{_datadir}/lua/%{major_minor}

%files devel
%{_includedir}/lua%{major_minor}/
%{_libdir}/pkgconfig/lua%{major_minor}.pc

%changelog
* Fri Oct 16 2026 Christoph Pracht - 5.5.1-1
- Initial package
