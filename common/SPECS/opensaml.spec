%define compname opensaml
%define libname libsaml13
%define develname libsaml-devel
%define schemaname %{compname}-schemas
%define utilname %{compname}-bin

Name: %{libname}
Version: 3.3.0
Release: 1%{?dist}
Summary: OpenSAML SAML library
Group: Development/Libraries/C and C++
Vendor: Shibboleth Consortium
License: Apache-2.0
URL: http://www.opensaml.org/
Source0: https://shibboleth.net/downloads/c++-%{compname}/%{version}/%{compname}-%{version}.tar.bz2
Provides: %{compname} = %{version}-%{release}
Obsoletes: %{compname} < %{version}-%{release}
BuildRequires: libxerces-c-devel >= 3.2
BuildRequires: libxml-security-c-devel >= 2.0.0
BuildRequires: libxmltooling-devel >= 3.3.0
%{?_with_log4cpp:BuildRequires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:BuildRequires: liblog4shib-devel >= 1.0.4}
BuildRequires: gcc-c++
BuildRequires: pkgconfig
BuildRequires: boost-devel >= 1.32.0
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

%description
OpenSAML is an open source implementation of the OASIS Security Assertion
Markup Language Specification. It contains a set of open source C++ classes
that support the SAML 1.0, 1.1, and 2.0 specifications.

The main package contains just the shared library.

%package -n %{utilname}
Summary: Utilities for OpenSAML library
Group: Development/Libraries/C and C++

%description -n %{utilname}
OpenSAML is an open source implementation of the OASIS Security Assertion
Markup Language Specification. It contains a set of open source C++ classes
that support the SAML 1.0, 1.1, and 2.0 specifications.

This package contains the utility programs.

%package -n %{develname}
Summary: OpenSAML development Headers
Group: Development/Libraries/C and C++
Requires: %{libname} = %{version}-%{release}
Provides: %{compname}-devel = %{version}-%{release}
Obsoletes: %{compname}-devel < %{version}-%{release}
Requires: libxerces-c-devel >= 3.2
Requires: libxml-security-c-devel >= 2.0.0
Requires: libxmltooling-devel >= 3.3.0
%{?_with_log4cpp:Requires: liblog4cpp-devel >= 1.0}
%{!?_with_log4cpp:Requires: liblog4shib-devel >= 1.0.4}

%description -n %{develname}
OpenSAML is an open source implementation of the OASIS Security Assertion
Markup Language Specification. It contains a set of open source C++ classes
that support the SAML 1.0, 1.1, and 2.0 specifications.

This package includes files needed for development with OpenSAML.

%package -n %{schemaname}
Summary: OpenSAML schemas and catalog
Group: Development/Libraries/C and C++

%description -n %{schemaname}
OpenSAML is an open source implementation of the OASIS Security Assertion
Markup Language Specification. It contains a set of open source C++ classes
that support the SAML 1.0, 1.1, and 2.0 specifications.

This package includes XML schemas and related files.

%prep
%setup -q -n %{compname}-%{version}

%build
%if 0%{?rhel} == 6 || 0%{?rhel} == 7 || 0%{?amzn} >= 1
%configure %{?saml_options} PKG_CONFIG_PATH=/opt/shibboleth/%{_lib}/pkgconfig
%else
%configure %{?saml_options}
%endif
%{__make}

%install
%make_install pkgdocdir=%{pkgdocdir}
# Don't package unit tester if present.
%{__rm} -f $RPM_BUILD_ROOT/%{_bindir}/samltest

%check
%{__make} check

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && %{__rm} -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{utilname}
%defattr(-,root,root,-)
%{_bindir}/samlsign

%files
%defattr(-,root,root,-)
%{_libdir}/libsaml.so.*
%exclude %{_libdir}/libsaml.la

%files -n %{schemaname}
%defattr(-,root,root,-)
%dir %{_datadir}/xml/opensaml
%{_datadir}/xml/opensaml/*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/opensaml.pc
%doc %{pkgdocdir}

%changelog
* Wed Oct 16 2024 Scott Cantor <cantor.2@osu.edu> - 3.3.0-1
- Bump version and xmltooling dependency

* Sat Jun 17 2023 John W. O'Brien <john@saltant.com> - 3.2.1-2
- Normalize SPEC file whitespace
- Delete obsolete BuildRoot macro
- Limit macro specifications to one per line for diff-ability
- Ensure Source is valid and fetchable
- Adopt %make_install
- Parameterize (sub-)package names
- Replace empty main package with lib sub-package
- Append %dist to Release

* Wed Dec 2 2020 Scott Cantor <cantor.2@osu.edu> - 3.2.0-1
- Version and lib bump

* Mon Feb 3 2020 Scott Cantor <cantor.2@osu.edu> - 3.1.0-1
- Version and lib bump
- Remove Solaris conditionals

* Mon Sep 30 2019 Scott Cantor <cantor.2@osu.edu> - 3.0.1-1
- CentOS 8 cleanup

* Tue Nov 21 2017 Scott Cantor <cantor.2@osu.edu> - 3.0.0-1
- Update soname
- Update dependency reqs
- Require Xerces 3.2 as shipped by me on all platforms

* Fri Jun 24 2016 Scott Cantor <cantor.2@osu.edu> - 2.6.0-1
- Fix some nits
- Update soname in package names

* Mon Mar 9 2015 Scott Cantor <cantor.2@osu.edu> - 2.5.4-1
- Require Xerces 3.1 even on older platforms
- Switch to bz2 source to avoid future SuSE issues

* Tue May 13 2014 Ian Young <ian@iay.org.uk> - 2.5.3-1.2
- Update package dependencies for RHEL/CentOS 7
- Fixed bogus dates in changelog

* Wed Dec 14 2011 Scott Cantor  <cantor.2@osu.edu>  - 2.5-1
- Update lib package number.
- Add boost-devel dependency.

* Tue Oct 26 2010  Scott Cantor  <cantor.2@osu.edu>  - 2.4-1
- Update version
- Add pkg-config support.
- Sync package names for side by side install.
- Adjust Xerces dependency name and Group setting
- Split out schemas into separate subpackage

* Mon Aug 31 2009   Scott Cantor  <cantor.2@osu.edu>  - 2.3-1
- Bump soname for SUSE packaging.

* Sat Aug 8 2009  Scott Cantor  <cantor.2@osu.edu>  - 2.2.1-1
- SuSE conventions
- Stop packaging unit tester

* Wed Dec 3 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.2-1
- Bumping for minor update.
- Fixing SUSE Xerces dependency name.

* Tue Jul 1 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.1-1
- Bumping for minor update.

* Mon Mar 17 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.0-6
- Official release.

* Fri Jan 18 2008  Scott Cantor  <cantor.2@osu.edu>  - 2.0-5
- Release candidate 1.

* Thu Nov 08 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-4
- Second public beta.

* Thu Aug 16 2007 Scott Cantor  <cantor.2@osu.edu>  - 2.0-3
- First public beta.

* Fri Jul 13 2007  Scott Cantor  <cantor.2@osu.edu>  - 2.0-2
- Second alpha.

* Mon Apr 16 2007  Scott Cantor  <cantor.2@osu.edu>  - 2.0-1
- First SPEC file for 2.0.
