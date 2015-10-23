%define release_prefix 1

Name:           cmake
Version:        2.8.5
Release:        %{?release_prefix:%{release_prefix}.}1.22.%{?dist}%{!?dist:tizen}
VCS:            external/cmake#submit/trunk/20130114.061649-0-gf2a7db895d9f34a09ad785ec20c1e242b4a17ec6
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
%changelog
* Mon Sep 16 2013 UkJung Kim <ujkim@samsung.com> - submit/trunk/20130114.061649 
- PROJECT: external/cmake
- COMMIT_ID: f2a7db895d9f34a09ad785ec20c1e242b4a17ec6
- PATCHSET_REVISION: f2a7db895d9f34a09ad785ec20c1e242b4a17ec6
- CHANGE_OWNER: \"UkJung Kim\" <ujkim@samsung.com>
- PATCHSET_UPLOADER: \"UkJung Kim\" <ujkim@samsung.com>
- CHANGE_URL: http://slp-info.sec.samsung.net/gerrit/136787
- PATCHSET_REVISION: f2a7db895d9f34a09ad785ec20c1e242b4a17ec6
- TAGGER: UkJung Kim <ujkim@samsung.com>
- Gerrit patchset approval info:
- UkJung Kim <ujkim@samsung.com> Verified : 1
- Newton Lee <newton.lee@samsung.com> Code Review : 2
- CHANGE_SUBJECT: Removed curl dependency by using cmake internal curl.
- [Version] 2.8.5
- [Project] GT-I8800
- [Title] Removed curl dependency by using cmake internal curl.
- [BinType] PDA
- [Customer] Open
- [Issue#] N/A
- [Problem] N/A
- [Cause] N/A
- [Solution] Removed curl dependency by using cmake internal curl.
- [Team] SCM
- [Developer] UkJung Kim <ujkim@samsung.com>
- [Request] N/A
- [Horizontal expansion] N/A
- [SCMRequest] N/A
* Fri Jul  8 2011 Ulf Hofemeier <ulf.hofemeier@linux.intel.com> - 2.8.3
- Removed cmake utilities Windows build directory as this is not needed for MeeGo BMC#20850
* Thu Dec 30 2010 Fathi Boudra <fathi.boudra@nokia.com> - 2.8.3
- New upstream release (BMC#11847)
- Merge cmake and cmake-gui in a single spec file for an easier maintainability
  and allow to use a single project for cmake and link cmake-gui project
  (BMC#11848)
- Remove add_findlibarchive_cmake_module.patch - merged upstream
- Add postchecks_buffer_overflow.patch to fix build in postchecks repository
  on buffer overflow error
* Mon Aug 16 2010 Fathi Boudra <fathi.boudra@nokia.com> - 2.8.2
- Use pkgconfig BuildRequires when possible.
* Fri Aug 13 2010 Fathi Boudra <fathi.boudra@nokia.com> - 2.8.2
- Drop cmake-gui to avoid to be blocked by Qt
- Remove BuildRequires: pkgconfig(QtGui), desktop-file-utils, libX11-devel
* Thu Aug 12 2010 Fathi Boudra <fathi.boudra@nokia.com> - 2.8.2
- Use QtGui instead of QtCore
- Remove license header
- Remove %%clean target (useless since MeeGo 1.1)
* Wed Aug 11 2010 Kaitlin Rupert <kaitlin.rupert@intel.com> - 2.8.2
- Replace qt4-devel with pkgconfig(QtCore)
* Mon Jul 19 2010 Fathi Boudra <fathi.boudra@nokia.com> - 2.8.2
- Update to 2.8.2
- Sanitize the spec file
- Use one BuildRequires per line
- Improve cmake-gui summary and description
- Use build-flags.cmake file for cmake initialization
- Pass --system-libs bootstrap option
- Re-enable Qt gui (cmake-gui)
- Drop conditional build parameters (without bootstrap/with gui)
- Drop rpm requirement. CMake doesn't need rpm to run.
- Add procps build requirement/requirement. CMake uses ps binary
- Add libarchive-devel build requirement
- Add add_findlibarchive_cmake_module.patch
  It allows to build with the system's libarchive
- Fix find command in %%install tag
  chmod +x should be applied to shell script files only
* Thu Dec  3 2009 Austin Zhang <austin.zhang@intel.com> 2.8.0
- Update to 2.8.0
* Sun Feb 15 2009 Anas Nashif <anas.nashif@intel.com> 2.6.3
- Disable gui
* Tue Jan 13 2009 Orion Poplawski <orion@cora.nwra.com> - 2.6.3-0.3.rc8
- Update to 2.6.3-RC-8
* Sun Jan  4 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.6.3-0.2.rc5
- macros.cmake: add -DCMAKE_SKIP_RPATH:BOOL=ON
- fix Release tag
* Wed Dec 10 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.3-0.rc5.1
- Update to 2.6.3-RC-5
* Tue Dec  2 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.6.2-3
- Add -DCMAKE_VERBOSE_MAKEFILE=ON to %%%%cmake (#474053)
- preserve timestamp of macros.cmake
- cosmetics
* Tue Oct 21 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-2
- Allow conditional build of gui
* Mon Sep 29 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-1
- Update to 2.6.2
* Mon Sep  8 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-0.rc3.1
- Update to 2.6.2-RC-2
- Drop parens patch fixed upstream
* Tue Sep  2 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-3
- Drop jni patch, applied upstream.
* Tue Aug 26 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.6.1-2
- attempt to patch logic error, crasher
* Tue Aug  5 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-1
- Update to 2.6.1
* Mon Jul 14 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.1-0.rc8.1
- Update to 2.6.1-RC-8
- Drop xmlrpc patch fixed upstream
* Tue May  6 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-1
- Update to 2.6.0
* Mon May  5 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc10.1
- Update to 2.6.0-RC-10
* Thu Apr 24 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc9.1
- Update to 2.6.0-RC-9
* Fri Apr 11 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc8.1
- Update to 2.6.0-RC-8
* Thu Apr  3 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc6.1
- Update to 2.6.0-RC-6
* Fri Mar 28 2008 Orion Poplawski <orion@cora.nwra.com> - 2.6.0-0.rc5.1
- Update to 2.6.0-RC-5
- Add gui sub-package for Qt frontend
* Fri Mar  7 2008 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-3
- Add macro for bootstrapping new release/architecture
- Add %%%%check section
* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.8-2
- Autorebuild for GCC 4.3
* Tue Jan 22 2008 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-1
- Update to 2.4.8
* Wed Jan 16 2008 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-0.rc12
- Update to 2.4.8 RC-12
* Fri Dec 14 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.8-0.rc4
- Update to 2.4.8 RC-4
* Mon Nov 12 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-4
- No longer set CMAKE_SKIP_RPATH
* Tue Aug 28 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-3
- Rebuild for new expat
* Wed Aug 22 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-2
- Rebuild for BuildID
* Mon Jul 23 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-1
- Update to 2.4.7
* Fri Jun 29 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.7-0.rc11
- Update to 2.4.7 RC-11
* Wed Jun 27 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-4
- Update macros.cmake to add CMAKE_INSTALL_LIBDIR, INCLUDE_INSTALL_DIR,
  LIB_INSTALL_DIR, SYSCONF_INSTALL_DIR, and SHARE_INSTALL_PREFIX
* Mon Apr 16 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-3
- Apply patch from upstream CVS to fix .so install permissions (bug #235673)
* Fri Apr  6 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-2
- Add rpm macros
* Thu Jan 11 2007 Orion Poplawski <orion@cora.nwra.com> - 2.4.6-1
- Update to 2.4.6
* Mon Dec 18 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.5-2
- Use system libraries (bootstrap --system-libs)
* Tue Dec  5 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.5-1
- Update to 2.4.5
* Tue Nov 21 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.4-1
- Update to 2.4.4
* Tue Oct 31 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-4
- Add /usr/lib/jvm/java to FindJNI search paths
* Tue Aug 29 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-3
- Rebuild for FC6
* Wed Aug  2 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-2
- vim 7.0 now ships cmake files, so don't ship ours (bug #201018)
- Add patch to Linux.cmake for Fortran soname support for plplot
* Tue Aug  1 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.3-1
- Update to 2.4.3
* Mon Jul 31 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.2-3
- Update for vim 7.0
* Tue Jul 11 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.2-2
- Patch FindRuby and FindSWIG to work on Fedora (bug #198103)
* Fri Jun 30 2006 Orion Poplawski <orion@cora.nwra.com> - 2.4.2-1
- Update to 2.4.2
* Thu Apr  6 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-4
- Update for vim 7.0c
* Tue Mar 28 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-3
- No subpackages, just own the emacs and vim dirs.
* Tue Mar 21 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-2
- Add emacs and vim support
- Include Example in docs
* Wed Mar  8 2006 Orion Poplawski <orion@cora.nwra.com> - 2.2.3-1
- Fedora Extras version
