#
# Conditional build
%bcond_with	bytecode	# use bytecode hinting instead of autohinting by default
#
Summary:	Font configuration and customization tools
Summary(pl):	Narzêdzia do konfigurowania fontów
Summary(pt_BR):	Ferramentas para configuração e customização do acesso a fontes
Name:		fontconfig
Version:	2.3.93
Release:	1
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	http://fontconfig.org/release/%{name}-%{version}.tar.gz
# Source0-md5:	0d80f23213a9ca0ea60dc4879efffec3
Patch0:		%{name}-blacklist.patch
Patch1:		%{name}-autohint.patch
Patch2:		%{name}-lunak_fccfg.c.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	docbook-utils >= 0.6.13-3
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	ed
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 2.1.5
BuildRequires:	libtool
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	freetype >= 2.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains tools and documentation.

%description -l pl
Fontconfig jest bibliotek± przeznaczon± do lokalizowania fontów w
systemie i wybierania ich w zale¿no¶ci od potrzeb aplikacji.

Paket ten zawiera programy narzêdziowe i dokumentacjê.

%description -l pt_BR
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

Este pacote contém as ferramentas e documentação.

%package libs
Summary:	Font configuration and customization library
Summary(pl):	Biblioteka do konfigurowania fontów
Summary(pt_BR):	Biblioteca para configuração e customização do acesso a fontes
Group:		Development/Libraries
Requires:	freetype >= 2.1.5
Provides:	XFree86-fontconfig
Conflicts:	fontconfig <= 1:2.2.98-1
Obsoletes:	XFree86-fontconfig

%description libs
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

%description libs -l pl
Fontconfig jest bibliotek± przeznaczon± do lokalizowania fontów w
systemie i wybierania ich w zale¿no¶ci od potrzeb aplikacji.

%description libs -l pt_BR
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

%package devel
Summary:	Font configuration and customization library - development files
Summary(pl):	Biblioteka do konfigurowania fontów - pliki dla programistów
Summary(pt_BR):	Biblioteca para configuração e customização do acesso a fontes - arquivos de desenvolvimento
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	expat-devel
Requires:	freetype-devel >= 2.1.5
Provides:	XFree86-fontconfig-devel
Obsoletes:	XFree86-fontconfig-devel

%description devel
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains the header files needed to develop programs that
use these fontconfig.

%description devel -l pl
Fontconfig jest bibliotek± przeznaczon± do lokalizowania fontów w
systemie i wybierania ich w zale¿no¶ci od potrzeb aplikacji.

Ten pakiet zawiera pliki nag³ówkowe potrzebne do kompilowania
programów korzystaj±cych z biblioteki fontconfig.

%description devel -l pt_BR
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

Este pacote contém arquivos de desenvolvimento necessários à criação
de extensões baseadas na biblioteca fontconfig.

%package static
Summary:	Static font configuration and customization library
Summary(pl):	Statyczna biblioteka do konfigurowania fontów
Summary(pt_BR):	Biblioteca estática para configuração e customização do acesso a fontes
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	XFree86-fontconfig-static
Obsoletes:	XFree86-fontconfig-static

%description static
This package contains static version of fontconfig library.

%description static -l pl
Ten pakiet zawiera statyczn± wersjê biblioteki fontconfig.

%description static -l pt_BR
Este pacote contém a biblioteca estática do fontconfig

%prep
%setup -q
%patch0 -p1
%if %{with bytecode}
%patch1 -p1
%endif
%patch2 -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-docs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,3,5}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install doc/*.3 $RPM_BUILD_ROOT%{_mandir}/man3
install doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

cp -f conf.d/README README.confd

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
HOME=/tmp %{_bindir}/fc-cache -f 2>/dev/null

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.confd
%attr(755,root,root) %{_bindir}/fc-*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files libs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/fonts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/fonts.conf
%{_sysconfdir}/fonts/fonts.dtd
%dir %{_sysconfdir}/fonts/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/conf.d/*.conf
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc doc/fontconfig-devel/*.html
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/fontconfig
%{_pkgconfigdir}/fontconfig.pc
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
