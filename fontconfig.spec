# TODO:
# - upgrade puts new files into /usr/share/fontconfig/conf.avail/*.conf
# and also removes /etc/fonts/conf.avail/*.conf BUT there is a symlink
# /etc/fonts/conf.avail/ -> /usr/share/fontconfig/conf.avail/ and in the end
# rpm deletes freshly installed /usr/share/fontconfig/conf.avail/*.conf files

# Conditional build
%bcond_without	static_libs	# don't build static library
%bcond_without	doc
#
Summary:	Font configuration and customization tools
Summary(pl.UTF-8):	Narzędzia do konfigurowania fontów
Summary(pt_BR.UTF-8):	Ferramentas para configuração e customização do acesso a fontes
Name:		fontconfig
Version:	2.10.1
Release:	0.1
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	http://fontconfig.org/release/%{name}-%{version}.tar.gz
# Source0-md5:	c94e380eea42f2f23ca9537035ef1899
Source1:	%{name}-lcd-filter.conf
Patch0:		%{name}-blacklist.patch
Patch1:		%{name}-bitstream-cyberbit.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{with doc}
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils >= 0.6.13-3
%endif
BuildRequires:	ed
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 2.1.5
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	freetype >= 2.1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

This package contains tools and documentation.

%description -l pl.UTF-8
Fontconfig jest biblioteką przeznaczoną do lokalizowania fontów w
systemie i wybierania ich w zależności od potrzeb aplikacji.

Paket ten zawiera programy narzędziowe i dokumentację.

%description -l pt_BR.UTF-8
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

Este pacote contém as ferramentas e documentação.

%package libs
Summary:	Font configuration and customization library
Summary(pl.UTF-8):	Biblioteka do konfigurowania fontów
Summary(pt_BR.UTF-8):	Biblioteca para configuração e customização do acesso a fontes
Group:		Libraries
Requires:	freetype >= 2.1.5
Provides:	XFree86-fontconfig
Obsoletes:	XFree86-fontconfig
Conflicts:	fontconfig <= 1:2.2.98-1

%description libs
Fontconfig is designed to locate fonts within the system and select
them according to requirements specified by applications.

%description libs -l pl.UTF-8
Fontconfig jest biblioteką przeznaczoną do lokalizowania fontów w
systemie i wybierania ich w zależności od potrzeb aplikacji.

%description libs -l pt_BR.UTF-8
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

%package devel
Summary:	Font configuration and customization library - development files
Summary(pl.UTF-8):	Biblioteka do konfigurowania fontów - pliki dla programistów
Summary(pt_BR.UTF-8):	Biblioteca para configuração e customização do acesso a fontes - arquivos de desenvolvimento
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

%description devel -l pl.UTF-8
Fontconfig jest biblioteką przeznaczoną do lokalizowania fontów w
systemie i wybierania ich w zależności od potrzeb aplikacji.

Ten pakiet zawiera pliki nagłówkowe potrzebne do kompilowania
programów korzystających z biblioteki fontconfig.

%description devel -l pt_BR.UTF-8
Fontconfig é uma biblioteca para configuração e customização do acesso
a fontes.

Este pacote contém arquivos de desenvolvimento necessários à criação
de extensões baseadas na biblioteca fontconfig.

%package static
Summary:	Static font configuration and customization library
Summary(pl.UTF-8):	Statyczna biblioteka do konfigurowania fontów
Summary(pt_BR.UTF-8):	Biblioteca estática para configuração e customização do acesso a fontes
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	XFree86-fontconfig-static
Obsoletes:	XFree86-fontconfig-static

%description static
This package contains static version of fontconfig library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną wersję biblioteki fontconfig.

%description static -l pt_BR.UTF-8
Este pacote contém a biblioteca estática do fontconfig

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

# don't rebuild docs by default, use prebuild ones
export HASDOCBOOK=no

%configure \
	--%{?with_doc:en}%{!?with_doc:dis}able-docs \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_mandir}/man{1,3,5},/var/cache/fontconfig} \

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	htmldoc_DATA= \
	doc_DATA=

install %{SOURCE1} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/conf.avail/10-lcd-filter.conf

ln -s %{_datadir}/%{name}/conf.avail $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.avail

cp -pf conf.d/README README.confd

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# this needs to be a symlink
if [ -d %{_sysconfdir}/fonts/conf.avail ]; then
	mv -f %{_sysconfdir}/fonts/conf.avail{,.rpmsave}
	install -d %{_datadir}/%{name}/conf.avail
	ln -s %{_datadir}/%{name}/conf.avail %{_sysconfdir}/fonts/conf.avail
fi

%post
umask 022
HOME=/tmp %{_bindir}/fc-cache -f 2>/dev/null || :

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.confd doc/fontconfig-user.html
%dir %{_sysconfdir}/fonts
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/fonts.conf
%{_sysconfdir}/fonts/conf.avail
%dir %{_datadir}/xml/%{name}
%{_datadir}/xml/%{name}/fonts.dtd
%dir %{_datadir}/%{name}/conf.avail
%{_datadir}/%{name}/conf.avail/*.conf
%dir %{_sysconfdir}/fonts/conf.d
%{_sysconfdir}/fonts/conf.d/README
%config(noreplace,missingok) %verify(not link md5 mtime size) %{_sysconfdir}/fonts/conf.d/*.conf
%attr(755,root,root) %{_bindir}/fc-cache
%attr(755,root,root) %{_bindir}/fc-cat
%attr(755,root,root) %{_bindir}/fc-list
%attr(755,root,root) %{_bindir}/fc-match
%attr(755,root,root) %{_bindir}/fc-query
%attr(755,root,root) %{_bindir}/fc-pattern
%attr(755,root,root) %{_bindir}/fc-scan
%if %{with doc}
%{_mandir}/man1/fc-*.1*
%{_mandir}/man5/fonts-conf.5*
%endif
/var/cache/fontconfig

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfontconfig.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfontconfig.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/fontconfig-devel/*.html
%attr(755,root,root) %{_libdir}/libfontconfig.so
%{_libdir}/libfontconfig.la
%{_includedir}/fontconfig
%{_pkgconfigdir}/fontconfig.pc
%if %{with doc}
%{_mandir}/man3/Fc*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfontconfig.a
%endif
