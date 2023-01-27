#
# Conditional build
%bcond_without	static_libs	# don't build static library
%bcond_without	doc		# don't build HTML and man docs
%bcond_without	tests		# don't perform make check

Summary:	Font configuration and customization tools
Summary(pl.UTF-8):	Narzędzia do konfigurowania fontów
Summary(pt_BR.UTF-8):	Ferramentas para configuração e customização do acesso a fontes
Name:		fontconfig
Version:	2.14.2
Release:	1
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	https://www.freedesktop.org/software/fontconfig/release/%{name}-%{version}.tar.xz
# Source0-md5:	95261910ea727b5dd116b06fbfd84b1f
Source1:	%{name}-lcd-filter.conf
Patch0:		%{name}-bitstream-cyberbit.patch
Patch1:		disable-tests.patch
URL:		http://fontconfig.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.11
%{?with_tests:BuildRequires:	bubblewrap}
%if %{with doc}
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils >= 0.6.13-3
%endif
BuildRequires:	ed
BuildRequires:	expat-devel
# pkgconfig(freetype) >= 21.0.15
BuildRequires:	freetype-devel >= 1:2.9
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gperf
%{?with_tests:BuildRequires:	json-c-devel}
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
%{?with_doc:BuildRequires:	python3}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
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
Requires:	freetype >= 1:2.9
Provides:	XFree86-fontconfig
Obsoletes:	XFree86-fontconfig < 4.4
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
Requires:	freetype-devel >= 1:2.9
Requires:	libuuid-devel
Provides:	XFree86-fontconfig-devel
Obsoletes:	XFree86-fontconfig-devel < 4.4

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
Obsoletes:	XFree86-fontconfig-static < 4.4

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

# bwrap: No permissions to creating new namespace, likely because the kernel does not allow non-privileged user namespaces...
sed -i -e 's#BWRAP=.*#BWRAP=#g' test/run-test.sh

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

# don't rebuild docs by default, use prebuild ones
export HASDOCBOOK=no

%configure \
	--enable-docs%{!?with_doc:=no} \
	--disable-silent-rules \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static
%{__make}

%{?with_tests:%{__make} OSTYPE=linux check || (cat test/test-suite.log && /bin/false)}

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

%find_lang %{name}
%find_lang %{name}-conf -a %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# this needs to be a symlink
if [ -d %{_sysconfdir}/fonts/conf.avail ] && [ ! -L %{_sysconfdir}/fonts/conf.avail ]; then
	mv -f %{_sysconfdir}/fonts/conf.avail{,.rpmsave}
	install -d %{_datadir}/%{name}/conf.avail
	ln -s %{_datadir}/%{name}/conf.avail %{_sysconfdir}/fonts/conf.avail
	mv -f %{_sysconfdir}/fonts/conf.avail.rpmsave/*.conf %{_sysconfdir}/fonts/conf.avail/
	rmdir %{_sysconfdir}/fonts/conf.avail.rpmsave 2>/dev/null || :
fi

%post
umask 022
HOME=/tmp %{_bindir}/fc-cache -f 2>/dev/null || :

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README README.confd doc/fontconfig-user.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/fonts/fonts.conf
%{_sysconfdir}/fonts/conf.avail
%{_sysconfdir}/fonts/conf.d/README
%config(noreplace,missingok) %verify(not link md5 mtime size) %{_sysconfdir}/fonts/conf.d/*.conf
%attr(755,root,root) %{_bindir}/fc-cache
%attr(755,root,root) %{_bindir}/fc-cat
%attr(755,root,root) %{_bindir}/fc-conflist
%attr(755,root,root) %{_bindir}/fc-list
%attr(755,root,root) %{_bindir}/fc-match
%attr(755,root,root) %{_bindir}/fc-query
%attr(755,root,root) %{_bindir}/fc-pattern
%attr(755,root,root) %{_bindir}/fc-scan
%attr(755,root,root) %{_bindir}/fc-validate
%dir %{_datadir}/xml/%{name}
%{_datadir}/xml/%{name}/fonts.dtd
%{_datadir}/%{name}/conf.avail/*.conf
%if %{with doc}
%{_mandir}/man1/fc-*.1*
%{_mandir}/man5/fonts-conf.5*
%endif
%dir /var/cache/fontconfig

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
%{_datadir}/gettext/its/fontconfig.its
%{_datadir}/gettext/its/fontconfig.loc
%if %{with doc}
%{_mandir}/man3/Fc*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfontconfig.a
%endif
