Summary:	Font configuration and customization library
Summary(pl):	Biblioteka do konfigurowania fontów
Name:		fontconfig
Version:	2.2.0
Release:	0.5
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	http://fontconfig.org/release/%{name}-%{version}.tar.gz
Patch0:		%{name}-blacklist.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ed
BuildRequires:	expat-devel
BuildRequires:	freetype-devel
BuildRequires:	libtool
Requires(post): /sbin/ldconfig
Provides:	XFree86-fontconfig
Provides:	%{name}-realpkg = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	XFree86-fontconfig

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

%description -l pl
Fontconfig jest biblioteka przeznaczon± do lokalizowania fontów w
systemie i wybierania ich w zale¿no¶ci od potrzeb aplikacji.

%package devel
Summary:	Font configuration and customization library
Summary(pl):	Biblioteka do konfigurowania fontów
Group:		Development/Libraries
Requires:	%{name}-realpkg = %{version}
Requires:	expat-devel
Requires:	freetype-devel
Provides:	%{name}-devel-realpkg = %{version}
Provides:	XFree86-fontconfig-devel
Obsoletes:	XFree86-fontconfig-devel

%description devel
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains the header files needed to develop programs that
use these fontconfig.

%description devel -l pl
Fontconfig jest biblioteka przeznaczon± do lokalizowania fontów w
systemie i wybierania ich w zale¿no¶ci od potrzeb aplikacji.

Ten pakiet zawiera pliki nag³ówkowe potrzebne do kompilowania
programów korzystaj±cych z biblioteki fontconfig.

%package static
Summary:	Static font configuration and customization library
Summary(pl):	Statyczna biblioteka do konfigurowania fontów
Group:		Development/Libraries
Requires:	%{name}-devel-realpkg = %{version}
Provides:	XFree86-fontconfig-static
Obsoletes:	XFree86-fontconfig-static

%description static
This package contains static version of fontconfig library.

%description static -l pl
Ten pakiet zawiera statyczn± wersjê biblioteki fontconfig.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure --disable-docs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install fc-cache/fc-cache.man $RPM_BUILD_ROOT%{_mandir}/man1/fc-cache.1
install fc-list/fc-list.man $RPM_BUILD_ROOT%{_mandir}/man1/fc-list.1

mv -f $RPM_BUILD_ROOT%{_docdir}/%{name} installed-docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
HOME=/root %{_bindir}/fc-cache -f 2> /dev/null

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README
%dir %{_sysconfdir}/fonts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/fonts/fonts.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/fonts/local.conf
%{_sysconfdir}/fonts/fonts.dtd
%attr(755,root,root) %{_bindir}/fc-*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files devel
%defattr(644,root,root,755)
%doc installed-docs/fontconfig-devel/*.html
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/fontconfig
%{_pkgconfigdir}/fontconfig.pc
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
