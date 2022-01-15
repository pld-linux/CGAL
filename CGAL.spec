# TODO
# - optflags
# - move qt stuff to subpackages?
#
# Conditional build:
%bcond_with	examples	# demo+examples build
%bcond_with	qt3		# CGAL_Qt3 library

%define	boost_ver	1.48
%define	qt5_ver		5.3
Summary:	Computational Geometry Algorithms Library
Summary(pl.UTF-8):	Computational Geometry Algorithms Library - biblioteka algorytmów geometrii obliczeniowej
Name:		CGAL
Version:	4.7
Release:	9
License:	GPL v3+ and LGPL v3+
Group:		Libraries
Source0:	https://github.com/CGAL/releases/archive/%{name}-%{version}.tar.gz
# Source0-md5:	50b29d3f3372cd93aaa31d01f0e45036
Patch0:		%{name}-buildtype.patch
URL:		http://www.cgal.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	Qt5Core-devel >= %{qt5_ver}
BuildRequires:	Qt5Gui-devel >= %{qt5_ver}
BuildRequires:	Qt5OpenGL-devel >= %{qt5_ver}
BuildRequires:	Qt5Svg-devel >= %{qt5_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt5_ver}
BuildRequires:	boost-devel >= %{boost_ver}
BuildRequires:	cmake >= 2.8.11
BuildRequires:	gmp-devel >= 4.1.4
BuildRequires:	libstdc++-devel
BuildRequires:	mpfr-devel >= 2.2.1
BuildRequires:	qt5-build >= %{qt5_ver}
BuildRequires:	qt5-qmake >= %{qt5_ver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
%if %{with qt3}
BuildRequires:	qt-devel >= 3
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
%endif
%if %{with examples}
BuildRequires:	blas-devel
BuildRequires:	eigen3 >= 3.1.91
BuildRequires:	gmp-c++-devel >= 4.1.4
BuildRequires:	lapack-devel
BuildRequires:	tbb
#TODO: mpfi QGLViewer ipelib 
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries for CGAL applications. CGAL is a collaborative effort of
several sites in Europe and Israel. The goal is to make the most
important of the solutions and methods developed in computational
geometry available to users in industry and academia in a C++ library.
The goal is to provide easy access to useful, reliable geometric
algorithms.

%description -l pl.UTF-8
Biblioteka dla aplikacji CGAL (Computational Geometry Algorithms
Library). CGAL to wspólny projekt kilku placówek w Europie i Izraelu.
Celem jest udostępnienie najważniejszych rozwiązań i metod powstałych
w geometrii obliczeniowej dla użytkowników przemysłowych i naukowych w
postaci biblioteki C++. Ma ona za zadanie zapewniać łatwy dostęp do
przydatnych, wiarygodnych algorytmów geometrycznych.

%package devel
Summary:	Development files and tools for CGAL applications
Summary(pl.UTF-8):	Pliki i narzędzia programistyczne dla aplikacji CGAL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= %{boost_ver}
Requires:	libstdc++-devel
# for Qt5 component
Requires:	Qt5Core-devel >= %{qt5_ver}
Requires:	Qt5Gui-devel >= %{qt5_ver}
Requires:	Qt5OpenGL-devel >= %{qt5_ver}
Requires:	Qt5Widgets-devel >= %{qt5_ver}
# for Qt3 component
%if %{with qt3}
Requires:	qt-devel >= 3
%endif
# CGAL header interfaces for (using their headers) - use Suggests?
Requires:	gmp-c++-devel >= 4.1.4
Requires:	gmp-devel >= 4.1.4
Requires:	mpfr-devel >= 2.2.1
#Suggests: eigen3 >= 3.1 gsl-devel tbb-devel vtk-devel
#Suggests(TODO): <rs_exports.h> <rs3_fncts.h> <taucs.h> <OpenMesh/Core/Mesh/PolyMesh_ArrayKernelT.hh> <NTL/ZZX.h> <mpfi.h> <LEDA/*.h> <ipelib.h>
Requires:	zlib-devel
# CGAL header interfaces for (without using their headers) - use Suggests?
Requires:	blas-devel
Requires:	lapack-devel

%description devel
This package provides the header files and tools you may need to
develop applications using CGAL.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe i narzędzia potrzebne do tworzenia
aplikacji wykorzystujących CGAL.

%package demos-source
Summary:	Examples and demos of CGAL algorithms
Summary(pl.UTF-8):	Przykłady i programy demonstracyjne do algorytmów CGAL
Group:		Documentation
Requires:	%{name}-devel = %{version}-%{release}

%description demos-source
This package provides the sources of examples and demos of CGAL
algorithms.

%description demos-source -l pl.UTF-8
Ten pakiet zawiera kod źrodłowy programów przykładowych i
demonstracyjnych do algorytmów CGAL.

%prep
%setup -q -n releases-%{name}-%{version}
%patch0 -p1

%build
install -d build
cd build
# override build type, because:
# PLD is not a valid build type: only Release or Debug is allowed
%cmake .. \
	-DCGAL_CXX_FLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	-DCGAL_SHARED_LINKER_FLAGS="%{rpmldflags}" \
	-DCGAL_INSTALL_LIB_DIR=%{_lib} \
	-DCGAL_INSTALL_DOC_DIR= \
	%{?with_qt3:-DWITH_CGAL_Qt3=ON} \
%if %{with examples}
	-DWITH_demos=ON \
	-DWITH_examples=ON
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# useless in binary package
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{cgal_create_CMakeLists,cgal_create_cmake_script,cgal_make_macosx_app}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES LICENSE LICENSE.BSL LICENSE.FREE_USE LICENSE.LGPL
%attr(755,root,root) %{_libdir}/libCGAL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL.so.11
%attr(755,root,root) %{_libdir}/libCGAL_Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_Core.so.11
%attr(755,root,root) %{_libdir}/libCGAL_ImageIO.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_ImageIO.so.11
%if %{with qt3}
%attr(755,root,root) %{_libdir}/libCGAL_Qt3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_Qt3.so.11
%endif
%attr(755,root,root) %{_libdir}/libCGAL_Qt5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCGAL_Qt5.so.11

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libCGAL.so
%attr(755,root,root) %{_libdir}/libCGAL_Core.so
%attr(755,root,root) %{_libdir}/libCGAL_ImageIO.so
%if %{with qt3}
%attr(755,root,root) %{_libdir}/libCGAL_Qt3.so
%endif
%attr(755,root,root) %{_libdir}/libCGAL_Qt5.so
%{_includedir}/CGAL
%{_libdir}/CGAL
%{_mandir}/man1/cgal_create_cmake_script.1*
