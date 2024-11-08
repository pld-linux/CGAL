# TODO
# - move qt stuff to subpackages? (include/CGAL/Qt, some cmake files)
# - MPFI (>= 1.5.2, mpfr >= 4.0.0)
# - LEDA, RS, RS3 (rather old, non-free; no longer available?)
#
# Conditional build:
%bcond_with	examples	# demo+examples build

%define	boost_ver	1.48
%define	qt6_ver		6.4
Summary:	Computational Geometry Algorithms Library
Summary(pl.UTF-8):	Computational Geometry Algorithms Library - biblioteka algorytmów geometrii obliczeniowej
Name:		CGAL
Version:	6.0.1
Release:	2
License:	GPL v3+ and LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/CGAL/cgal/releases
Source0:	https://github.com/CGAL/cgal/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	944c789615bff14a56d78b398ec2cc49
Patch0:		%{name}-buildtype.patch
URL:		https://www.cgal.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	Qt6Core-devel >= %{qt6_ver}
BuildRequires:	Qt6Gui-devel >= %{qt6_ver}
BuildRequires:	Qt6OpenGL-devel >= %{qt6_ver}
BuildRequires:	Qt6Svg-devel >= %{qt6_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt6_ver}
BuildRequires:	boost-devel >= %{boost_ver}
BuildRequires:	cmake >= 3.1
BuildRequires:	gmp-devel >= 4.1.4
BuildRequires:	libstdc++-devel
BuildRequires:	mpfr-devel >= 2.2.1
BuildRequires:	qt6-build >= %{qt6_ver}
BuildRequires:	qt6-qmake >= %{qt6_ver}
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	sed >= 4.0
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with examples}
BuildRequires:	blas-devel
BuildRequires:	eigen3 >= 3.1.91
BuildRequires:	gmp-c++-devel >= 4.1.4
BuildRequires:	ipe-devel >= 7
BuildRequires:	lapack-devel
BuildRequires:	tbb
%endif
BuildArch:	noarch
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
Requires:	boost-devel >= %{boost_ver}
Requires:	libstdc++-devel
# for Qt6 component
Requires:	Qt6Core-devel >= %{qt6_ver}
Requires:	Qt6Gui-devel >= %{qt6_ver}
Requires:	Qt6OpenGL-devel >= %{qt6_ver}
Requires:	Qt6Widgets-devel >= %{qt6_ver}
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
Obsoletes:	CGAL < 6.0.1

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
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCGAL_CXX_FLAGS="%{rpmcxxflags} %{rpmcppflags}" \
	-DCGAL_SHARED_LINKER_FLAGS="%{rpmldflags}" \
	-DCGAL_INSTALL_LIB_DIR=%{_datadir} \
	-DCGAL_INSTALL_DOC_DIR= \
%if %{with examples}
	-DWITH_demos=ON \
	-DWITH_examples=ON
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files devel
%defattr(644,root,root,755)
%doc AUTHORS CHANGES.md README.md
%doc LICENSE LICENSE.BSL LICENSE.COMMERCIAL LICENSE.RFL
%attr(755,root,root) %{_bindir}/cgal_create_CMakeLists
%attr(755,root,root) %{_bindir}/cgal_create_cmake_script
%{_includedir}/CGAL
%{_datadir}/cmake/CGAL
%{_mandir}/man1/cgal_create_cmake_script.1*
