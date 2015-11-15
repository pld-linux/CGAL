# TODO
# - force use of qt5, otherwise it may pick qt4! add bcond?
# - check these:
#   blas-devel may be superfluous !
#   gmp-c++-devel may be superfluous !
#   lapack-devel may be superfluous !
# - cleanup?
#   warning: Installed (but unpackaged) file(s) found:
#   /usr/bin/cgal_make_macosx_app
# - move qt stuff to subpackages?

%define boost_version 1.32
Summary:	Computational Geometry Algorithms Library
Name:		CGAL
Version:	4.7
Release:	1
License:	GPLv3+ and LGPLv3+
Group:		Libraries
Source0:	https://github.com/CGAL/releases/archive/%{name}-%{version}.tar.gz
# Source0-md5:	50b29d3f3372cd93aaa31d01f0e45036
URL:		http://www.cgal.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5OpenGL-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	blas-devel
BuildRequires:	boost-devel >= %{boost_version}
BuildRequires:	cmake
BuildRequires:	gmp-c++-devel
BuildRequires:	gmp-devel
BuildRequires:	lapack-devel
BuildRequires:	mpfr-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries for CGAL applications. CGAL is a collaborative effort of
several sites in Europe and Israel. The goal is to make the most
important of the solutions and methods developed in computational
geometry available to users in industry and academia in a C++ library.
The goal is to provide easy access to useful, reliable geometric
algorithms.

%package devel
Summary:	Development files and tools for CGAL applications
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	blas-devel
Requires:	boost-devel >= %{boost_version}
Requires:	gmp-c++-devel
Requires:	gmp-devel
Requires:	lapack-devel
Requires:	mpfr-devel
Requires:	qt-devel
Requires:	zlib-devel

%description devel
The %{name}-devel package provides the headers files and tools you may
need to develop applications using CGAL.

%package demos-source
Summary:	Examples and demos of CGAL algorithms
Group:		Documentation
Requires:	%{name}-devel = %{version}-%{release}

%description demos-source
The %{name}-demos-source package provides the sources of examples and
demos of CGAL algorithms.

%prep
%setup -q -n releases-%{name}-%{version}

%build
install -d build
cd build
# override build type, because:
# PLD is not a valid build type: only Release or Debug is allowed

# XXX: what is ${CHANGE_SOVERSION} here?
%cmake \
	-DCMAKE_BUILD_TYPE=%{!?debug:Release}%{?debug:Debug} \
	-DCGAL_INSTALL_LIB_DIR=%{_lib} \
	-DCGAL_INSTALL_DOC_DIR= ${CHANGE_SOVERSION} \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE LICENSE.FREE_USE LICENSE.LGPL CHANGES
%attr(755,root,root) %{_libdir}/libCGAL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL.so.11
%attr(755,root,root) %{_libdir}/libCGAL_Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_Core.so.11
%attr(755,root,root) %{_libdir}/libCGAL_ImageIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_ImageIO.so.11
%attr(755,root,root) %{_libdir}/libCGAL_Qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_Qt5.so.11

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cgal_create_CMakeLists
%attr(755,root,root) %{_bindir}/cgal_create_cmake_script
%{_includedir}/CGAL
%{_libdir}/CGAL
%attr(755,root,root) %{_libdir}/libCGAL*.so
%{_mandir}/man1/cgal_create_cmake_script.1*
