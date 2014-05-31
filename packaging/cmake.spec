%define release_prefix 1

Name:           cmake
Version:        2.8.5
Release:        %{release_prefix}
License:        BSD
Summary:        Cross-platform make system
Url:            http://www.cmake.org
Group:          Development/Tools
Source0:        http://www.cmake.org/files/v2.8/cmake-%{version}.tar.gz
Source1:        macros.cmake
BuildRequires:  expat-devel
BuildRequires:  pkgconfig(libarchive) >= 2.8.0
BuildRequires:  pkgconfig(zlib)
BuildRequires:  procps
BuildRequires:  pkgconfig(ncurses)

%description
CMake is used to control the software compilation process using simple platform
and compiler independent configuration files. CMake generates native makefiles
and workspaces that can be used in the compiler environment of your choice.
CMake is quite sophisticated: it is possible to support complex environments
requiring system configuration, pre-processor generation, code generation, and
template instantiation.


%prep
%setup -q -n cmake-%{version}

# Fixup permissions
find -name \*.h -o -name \*.cxx -print0 | xargs -0 chmod -x

%build
cat > %{buildroot}build-flags.cmake << EOF
set(CMAKE_SKIP_RPATH YES CACHE BOOL "Skip rpath" FORCE)
set(CMAKE_USE_RELATIVE_PATHS YES CACHE BOOL "Use relative paths" FORCE)
set(CMAKE_VERBOSE_MAKEFILE ON CACHE BOOL "Verbose build" FORCE)
set(CMAKE_C_FLAGS "%{optflags}" CACHE STRING "C flags" FORCE)  
set(CMAKE_CXX_FLAGS "%{optflags}" CACHE STRING "C++ flags" FORCE)  
set(CMAKE_SKIP_BOOTSTRAP_TEST ON CACHE BOOL "Skip BootstrapTest" FORCE)
set(BUILD_CursesDialog YES CACHE BOOL "Build curses GUI" FORCE)
set(MINGW_CC_LINUX2WIN_EXECUTABLE "" CACHE FILEPATH "Never detect mingw" FORCE)
set(CMAKE_USE_SYSTEM_LIBARCHIVE YES CACHE BOOL "" FORCE)
EOF
rm -rf %{_target_platform} && mkdir %{_target_platform}
cd %{_target_platform} && ../bootstrap \
                          --prefix=%{_prefix} \
                          --docdir=/share/doc/cmake-%{version} \
                          --mandir=/share/man \
                          --datadir=/share/cmake \
                          --%{?with_bootstrap:no-}system-libs \
                          --parallel=`/usr/bin/getconf _NPROCESSORS_ONLN` \
                          --init=%{buildroot}build-flags.cmake \
                          --system-libs \
                          --no-system-curl

make VERBOSE=1 %{?_smp_mflags}

%install
%makeinstall -C %{_target_platform} DESTDIR=%{buildroot}
find %{buildroot}%{_datadir}/%{name}/Modules -name '*.sh*' -type f | xargs chmod -x
mkdir -p %{buildroot}%{_datadir}/emacs/site-lisp
cp -a Example %{buildroot}%{_datadir}/doc/%{name}-%{version}/
install -m 0644 Docs/cmake-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/
# Install cmake rpm macros
install -D -p -m 0644 %{_sourcedir}/macros.cmake \
  %{buildroot}%{_sysconfdir}/rpm/macros.cmake

%remove_docs

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/macros.cmake
%{_bindir}/ccmake
%{_bindir}/cmake
%{_bindir}/cpack
%{_bindir}/ctest
%{_datadir}/%{name}/*
%{_datadir}/emacs/*
