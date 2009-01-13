%define boost_version 1.32

Summary:	Computational Geometry Algorithms Library
Name:		CGAL
Version:	3.3.1
Release:	0.99
License:	QPL and LGPLv2 and LGPLv2+
Group:		Libraries
URL:		http://www.cgal.org/
Source0:	ftp://ftp.mpi-sb.mpg.de/pub/outgoing/CGAL/%{name}-%{version}.tar.gz
# Source0-md5:	733339b6b05b48d4c7934a6e735b6fc0
Patch1:		%{name}-install_cgal-SUPPORT_REQUIRED.patch
Patch2:		%{name}-build-library.patch
Patch4:		%{name}-install_cgal-no_versions_in_compiler_config.h.patch
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	boost-devel >= %boost_version
BuildRequires:	gmp-devel
BuildRequires:	qt-devel >= 3.0
BuildRequires:	zlib-devel
BuildRequires:	mpfr-devel
BuildRequires:	gmp-c++-devel
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
Requires:	%{_sysconfdir}/profile.d
Requires:	%{name} = %{version}-%{release}
Requires:	blas-devel
Requires:	lapack-devel
Requires:	qt-devel
Requires:	zlib-devel
Requires:	gmp-devel
Requires:	boost-devel >= %{boost_version}
Requires:	mpfr-devel
Requires:	gmp-c++-devel
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
%setup -q
%patch1 -p0 -b .support-required.bak
%patch2 -p1 -b .build-library.bak
%patch4 -p1 -b .no_versions.bak

chmod a-x examples/Nef_3/handling_double_coordinates.cin
# fix end-of-lines of several files
for f in demo/Straight_skeleton_2/data/vertex_event_9.poly \
         demo/Straight_skeleton_2/data/vertex_event_0.poly \
         examples/Surface_mesh_parameterization/data/mask_cone.off \
         examples/Boolean_set_operations_2/test.dxf;
do
  if [ -r $f ]; then
    sed -i.bak 's/\r//' $f;
    touch -r ${f}.bak $f
    rm -f ${f}.bak
  fi
done

%build
export QTDIR=%{_prefix}
./install_cgal -ni g++ --CUSTOM_CXXFLAGS "$RPM_OPT_FLAGS" \
			   --without-autofind \
			   --with-ZLIB \
			   --with-BOOST \
			   --with-BOOST_PROGRAM_OPTIONS \
			   --with-X11 \
			   --with-GMP \
			   --with-GMPXX \
			   --with-MPFR \
			   --with-QT3MT \
			   --with-REFBLASSHARED \
			   --with-DEFAULTLAPACK \
			   --with-OPENGL \
			   --QT_INCL_DIR=%{_includedir}/qt \
			   --QT_LIB_DIR=%{_libdir} \
			   --disable-static


%install
rm -rf $RPM_BUILD_ROOT

case "%{_arch}" in
        *64* | s390 )
           SUFFIX=64 ;;
        * )
           SUFFIX=32 ;;
esac

# Install headers
install -d $RPM_BUILD_ROOT%{_includedir}
cp -a include/* $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT%{_includedir}/CGAL/config/msvc*
mv $RPM_BUILD_ROOT%{_includedir}/CGAL/config/*/CGAL/compiler_config.h $RPM_BUILD_ROOT%{_includedir}/CGAL/compiler_config.h


# remove the arch-specific comment
sed -i -e '/System: / d' $RPM_BUILD_ROOT%{_includedir}/CGAL/compiler_config.h

# use the timestamp of install_cgal
touch -r install_cgal $RPM_BUILD_ROOT%{_includedir}/CGAL/compiler_config.h
rm -rf $RPM_BUILD_ROOT%{_includedir}/CGAL/config

# Install scripts (only those prefixed with "cgal_").
install -d $RPM_BUILD_ROOT%{_bindir}
install -p scripts/cgal_* $RPM_BUILD_ROOT%{_bindir}

# Install libraries
install -d $RPM_BUILD_ROOT%{_libdir}
cp -a lib/*/lib* $RPM_BUILD_ROOT%{_libdir}

# Install makefile:
install -d $RPM_BUILD_ROOT%{_datadir}/CGAL
touch -r make $RPM_BUILD_ROOT%{_datadir}/CGAL
install -p make/makefile_* $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk

# Install demos and examples
install -d $RPM_BUILD_ROOT%{_datadir}/CGAL/
touch -r demo $RPM_BUILD_ROOT%{_datadir}/CGAL/
cp -a demo $RPM_BUILD_ROOT%{_datadir}/CGAL/demo
cp -a examples $RPM_BUILD_ROOT%{_datadir}/CGAL/examples

# Modify makefile
cat > makefile.sed <<'EOF'
s,CGAL_INCL_DIR *=.*,CGAL_INCL_DIR = %{_includedir},;
s,CGAL_LIB_DIR *=.*,CGAL_LIB_DIR = %{_libdir},;
/CUSTOM_CXXFLAGS/ s/-O2 //;
/CUSTOM_CXXFLAGS/ s/-g //;
/CGAL_INCL_DIR/ s,/CGAL/config/.*,,;
s,/$(CGAL_OS_COMPILER),,g;
/-I.*CGAL_INCL_CONF_DIR/ d
EOF

# use -i.bak to generate cgal-${SUFFIX}.mk.bak with right timestamp
# used below to restore the timestamp
sed -i.bak -f makefile.sed $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk

# check if the sed script above has worked:
grep -q %{_builddir} $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk && false
grep -q $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk && false
grep -q CGAL/config $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk && false
grep -q -E 'CUSTOM_CXXFLAGS.*(-O2|-g)' $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk && false

# Remove -L and -R flags from the makefile
cat > makefile-noprefix.sed <<'EOF'
/'-L$(CGAL_LIB_DIR)'/ d;
/-R$(CGAL_LIB_DIR)/ d;
/'-I$(CGAL_INCL_DIR)'/ d;
EOF

sed -i -f makefile-noprefix.sed  $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk

# restore the timestamp and remove the .bak file
touch -r $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk.bak $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk
rm -f $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk.bak

# check that the sed script has worked
grep -q -E -- '-[LI]\$' $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk && false
grep -q -E -- '-R' $RPM_BUILD_ROOT%{_datadir}/CGAL/cgal-${SUFFIX}.mk && false

# Create %{_sysconfdir}/profile.d/ scripts
install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/cgal.sh <<EOF
ARCH=`uname -m`

case \$ARCH in
        x86_64 | ia64 | s390 )
           SUFFIX=64 ;;
        * )
           SUFFIX=32 ;;
esac

if [ -z "\$CGAL_MAKEFILE" ] ; then
  CGAL_MAKEFILE="%{_datadir}/CGAL/cgal-${SUFFIX}.mk"
  export CGAL_MAKEFILE
fi
EOF

cat > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/cgal.csh <<EOF
set ARCH=`uname -m`

switch( \$ARCH )
        case x86_64:
        case ia64:
        case s390:
          set SUFFIX=64;
          breaksw;
        default:
          set SUFFIX=62;
endsw

if ( ! \$?CGAL_MAKEFILE ) then
  setenv CGAL_MAKEFILE "%{_datadir}/CGAL/cgal-${SUFFIX}.mk"
endif
EOF

# use the timestamp of install_cgal
touch -r install_cgal $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/cgal.*sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE LICENSE.FREE_USE LICENSE.LGPL LICENSE.QPL CHANGES
%attr(755,root,root) %{_libdir}/libCGAL*.so.2
%attr(755,root,root) %{_libdir}/libCGAL*.so.2.0.1


%files devel
%defattr(644,root,root,755)
%{_includedir}/CGAL
%{_libdir}/libCGAL*.so
%dir %{_datadir}/CGAL
%{_datadir}/CGAL/cgal*.mk
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/cgal_make_macosx_app
%config(noreplace) /etc/profile.d/cgal.*


%files demos-source
%defattr(644,root,root,755)
%{_datadir}/CGAL/demo
%{_datadir}/CGAL/examples
%exclude %{_datadir}/CGAL/*/*/*.vcproj
%exclude %{_datadir}/CGAL/*/*/skip_vcproj_auto_generation
