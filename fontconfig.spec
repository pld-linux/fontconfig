
%define         _snap           040304

Summary:	Font configuration and customization library
Summary(pl):	Biblioteka do konfigurowania fontów
Summary(pt_BR):	Fontconfig é uma biblioteca para configuração e customização do acesso a fontes
Name:		fontconfig
Version:	2.2.92.%{_snap}
Release:	1
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	http://ep09.pld-linux.org/~adgor/pld/%{name}-%{_snap}.tar.bz2
# Source0-md5:	3ca9eac63d4076d1062e59f40ff3ac21
#Source0:	http://pdx.freedesktop.org/~fontconfig/release/%{name}-%{version}.tar.gz
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-utils >= 0.6.13-3
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	ed
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 2.1.4
BuildRequires:	libtool
BuildRequires:	lynx
Requires(post):	/sbin/ldconfig
Requires:	freetype >= 2.1.4
Provides:	%{name}-realpkg = %{epoch}:%{version}-%{release}
Provides:	XFree86-fontconfig
Obsoletes:	XFree86-fontconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

%description -l pl
Fontconfig jest biblioteka przeznaczon± do lokalizowania fontów w
systemie i wybierania ich w zale¿no¶ci od potrzeb aplikacji.

%description -l pt_BR
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

%package devel
Summary:	Font configuration and customization library
Summary(pl):	Biblioteka do konfigurowania fontów
Summary(pt_BR):	Fontconfig é uma biblioteca para configuração e customização do acesso a fontes
Group:		Development/Libraries
Requires:	%{name}-realpkg = %{epoch}:%{version}
Requires:	expat-devel
Requires:	freetype-devel >= 2.1.4
Provides:	%{name}-devel-realpkg = %{epoch}:%{version}-%{release}
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

%description devel -l pt_BR
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

%package static
Summary:	Static font configuration and customization library
Summary(pl):	Statyczna biblioteka do konfigurowania fontów
Group:		Development/Libraries
Requires:	%{name}-devel-realpkg = %{epoch}:%{version}
Provides:	XFree86-fontconfig-static
Obsoletes:	XFree86-fontconfig-static

%description static
This package contains static version of fontconfig library.

%description static -l pl
Ten pakiet zawiera statyczn± wersjê biblioteki fontconfig.

%prep
%setup -q -n %{name}-%{_snap}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,3,5}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man3
install doc/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

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
%attr(755,root,root) %{_bindir}/fc-cache
%attr(755,root,root) %{_bindir}/fc-list
%attr(755,root,root) %{_bindir}/fc-match
%attr(755,root,root) %{_libdir}/libfontconfig.so.*.*.*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files devel
%defattr(644,root,root,755)
%doc doc/{fontconfig-devel/*.html,fontconfig-{user,devel}.txt,fontconfig-user.html}
%{_libdir}/libfontconfig.la
%{_libdir}/libfontconfig.so
%{_includedir}/fontconfig
%{_pkgconfigdir}/fontconfig.pc
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libfontconfig.a
