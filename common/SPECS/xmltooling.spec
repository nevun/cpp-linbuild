%define compname xmltooling
%define libname lib%{compname}11
%define develname lib%{compname}-devel
%define schemaname %{compname}-schemas

Name: %{libname}
Version: 3.3.0
Release: 1%{?dist}
Summary: OpenSAML XML Processing library
Group: Development/Libraries/C and C++
Vendor: Shibboleth Consortium
License: Apache-2.0
URL: http://www.opensaml.org/
Source0: https://shibboleth.net/downloads/c++-opensaml/3.3.0/%{compname}-%{version}.tar.bz2
Provides: %{compname} = %{version}-%{release}
Obsoletes: %{compname} < %{version}-%{release}
BuildRequires: libxerces-c-devel >= 3.2
BuildRequires: libxml-security-c-devel >= 2.0.0
%{?_with_log4cpp:BuildRequires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:BuildRequires: liblog4shib-devel >= 1.0.4}
BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: boost-devel >= 1.32.0
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
BuildRequires: libcurl-openssl-devel >= 7.21.7
Requires: libcurl-openssl >= 7.21.7
%else
BuildRequires: curl-devel >= 7.10.6
%endif
%{!?_without_doxygen:BuildRequires: doxygen}
%if "%{_vendor}" == "redhat"
BuildRequires: redhat-rpm-config
%endif

%if 0%{?rhel} == 8
BuildRequires: gdb
%endif

%if "%{_vendor}" == "suse"
%define pkgdocdir %{_docdir}/%{compname}
%else
%define pkgdocdir %{_docdir}/%{compname}-%{version}
%endif

# Prevent the RHEL/etc 6+ package from requiring a vanilla libcurl.
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
%filter_from_requires /libcurl\.so\..*/d
%filter_setup
%endif

%description
The XMLTooling library contains generic XML parsing and processing
classes based on the Xerces-C DOM. It adds more powerful facilities
for declaring element- and type-specific API and implementation
classes to add value around the DOM, as well as signing and encryption
support.

The main package contains just the shared library.

%package -n %{develname}
Summary: XMLTooling development Headers
Group: Development/Libraries/C and C++
Requires: %{libname} = %{version}-%{release}
Provides: %{compname}-devel = %{version}-%{release}
Obsoletes: %{compname}-devel < %{version}-%{release}
Requires: libxerces-c-devel >= 3.2
Requires: libxml-security-c-devel >= 2.0.0
%{?_with_log4cpp:Requires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:Requires: liblog4shib-devel >= 1.0.4}
Requires: openssl-devel
Requires: boost-devel >= 1.32.0
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
Requires: libcurl-openssl-devel >= 7.21.7
%else
Requires: curl-devel >= 7.10.6
%endif

%description -n %{develname}
The XMLTooling library contains generic XML parsing and processing
classes based on the Xerces-C DOM. It adds more powerful facilities
for declaring element- and type-specific API and implementation
classes to add value around the DOM, as well as signing and encryption
support.

This package includes files needed for development with XMLTooling.

%package -n %{schemaname}
Summary: XMLTooling schemas and catalog
Group: Development/Libraries/C and C++

%description -n %{schemaname}
The XMLTooling library contains generic XML parsing and processing
classes based on the Xerces-C DOM. It adds more powerful facilities
for declaring element- and type-specific API and implementation
classes to add value around the DOM, as well as signing and encryption
support.

This package includes XML schemas and related files.

%prep
%setup -q -n %{compname}-%{version}

%build
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} == 1 || 0%{?amzn} == 2
%configure %{?xmltooling_options} %{!?_without_xmlsec: --with-xmlsec} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig CXXFLAGS="-std=c++11"
%else
%configure %{?xmltooling_options} %{!?_without_xmlsec: --with-xmlsec}
%endif
%{__make}

%install
%make_install pkgdocdir=%{pkgdocdir}
# Don't package unit tester if present.
%{__rm} -f $RPM_BUILD_ROOT/%{_bindir}/xmltoolingtest

%check
%{__make} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%exclude %{_libdir}/*.la

%files -n %{schemaname}
%defattr(-,root,root,-)
%dir %{_datadir}/xml/xmltooling
%{_datadir}/xml/xmltooling/*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/xmltooling.pc
%{_libdir}/pkgconfig/xmltooling-lite.pc
%doc %{pkgdocdir}

%changelog
* Wed Oct 16 2024 Scott Cantor <cantor.2@osu.edu> - 3.3.0-1
- Bump version and libname
- Add conditional C++11 CXXFLAGS for older Linux

* Sat Jun 17 2023 John W. O'Brien <john@saltant.com> - 3.2.4-2
- Normalize SPEC file whitespace
- Delete obsolete BuildRoot macro
- Limit macro specifications to one per line for diff-ability
- Ensure Source is valid and fetchable
- Adopt %make_install
- Parameterize (sub-)package names
- Replace empty main package with lib sub-package
- Append %dist to Release

* Wed Nov 2 2022 Scott Cantor <cantor.2@osu.edu> - 3.2.2-1
- Version bump

* Wed Dec 2 2020 Scott Cantor <cantor.2@osu.edu> - 3.2.0-1
- Version bump

* Mon Feb 3 2020 Scott Cantor <cantor.2@osu.edu> - 3.1.0-1
- Version and lib bump

* Mon Sep 30 2019 Scott Cantor <cantor.2@osu.edu> - 3.0.4-1
- CentOS 8 cleanup

* Tue Nov 21 2017 Scott Cantor <cantor.2@osu.edu> - 3.0.0-1
- Update soname
- Require Xerces 3.2 as shipped by me on all platforms
- Exclude libtool archives

* Fri Jun 24 2016 Scott Cantor <cantor.2@osu.edu> - 1.6.0-1
- Fix some lint issues
- Update soname in package name

* Thu Feb 26 2015 Scott Cantor <cantor.2@osu.edu> - 1.5.4-1
- Require Xerces 3.1 even on older platforms
- Add Amazon platform checks
- Switch to bz2 source to avoid future SuSE issues

* Tue May 13 2014 Ian Young <ian@iay.org.uk> - 1.5.3-1.2
- Update package dependencies for RHEL/CentOS 7

* Wed Dec 14 2011 Scott Cantor  <cantor.2@osu.edu>  - 1.5-1
- Update lib package number.
- Add boost-devel dependency.

* Sun Jun 26 2011  Scott Cantor  <cantor.2@osu.edu>  - 1.4.2-1
- Override curl build for RHEL6.

* Tue Oct 26 2010  Scott Cantor  <cantor.2@osu.edu>  - 1.4-1
- Update version
- Add pkg-config support.
- Sync package names for side by side install.
- Adjust Xerces dependency name and Group setting
- Split out schemas into separate subpackage

* Mon Aug 31 2009  Scott Cantor  <cantor.2@osu.edu>  - 1.3-1
- Bump soname for SUSE packaging.

* Thu Aug 6 2009  Scott Cantor  <cantor.2@osu.edu>  - 1.2.1-1
- SuSE conventions
- Stop packaging unit tester

* Wed Dec 3 2008  Scott Cantor  <cantor.2@osu.edu>  - 1.2-1
- Bumping for minor update.
- Fixing SuSE Xerces dependency name.

* Tue Jul 1 2008  Scott Cantor  <cantor.2@osu.edu>  - 1.1-1
- Bumping for minor update.

* Mon Mar 17 2008  Scott Cantor  <cantor.2@osu.edu>  - 1.0-6
- Official release.

* Fri Jan 18 2008  Scott Cantor  <cantor.2@osu.edu>  - 1.0-5
- Release candidate 1.

* Thu Nov 08 2007  Scott Cantor  <cantor.2@osu.edu>  - 1.0-4
- Second public beta.

* Thu Aug 16 2007  Scott Cantor  <cantor.2@osu.edu>  - 1.0-3
- First public beta.

* Fri Jul 13 2007  Scott Cantor  <cantor.2@osu.edu>  - 1.0-2
- Second alpha.

* Wed Apr 12 2006  Scott Cantor  <cantor.2@osu.edu>  - 1.0-1
- First SPEC file based on various versions in existence.
