
%define fcname		fcpackage
%define fcversion	2_1

Summary:	Font configuration and customization library
Summary(pl):	Biblioteka do konfigurowania fontów
Name:		fontconfig
Version:	1.0.1
Release:	9
Epoch:		1
License:	MIT
Group:		Libraries
Source0:	http://fontconfig.org/release/%{fcname}.%{fcversion}.tar.gz
Patch0:		%{name}-date.patch
Patch1:		%{name}-blacklist.patch
Patch2:		%{name}-defaultconfig.patch
Patch3:		%{name}-fontdir.patch
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
Provides:	XFree86-fontconfig-devel
Requires:	%{name}-realpkg = %{version}
Requires:	freetype-devel
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

%prep
%setup -q -n %{fcname}.%{fcversion}
%patch0 -p1
cd %{name}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cd %{name}
%{__autoconf}
%configure
%{__make} CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man{1,3}

cd %{name}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install fc-cache/fc-cache.man $RPM_BUILD_ROOT%{_mandir}/man1/fc-cache.1
install fc-list/fc-list.man $RPM_BUILD_ROOT%{_mandir}/man1/fc-list.1
install src/fontconfig.man $RPM_BUILD_ROOT%{_mandir}/man3/fontconfig.3

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
HOME=/root %{_bindir}/fc-cache -f 2> /dev/null

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{name}/{AUTHORS,README}
%dir %{_sysconfdir}/fonts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/fonts/fonts.conf
%{_sysconfdir}/fonts/fonts.dtd
%attr(755,root,root) %{_bindir}/fc-*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man1/*.1*

%files devel
%defattr(644,root,root,755)
%doc %{name}/ChangeLog
%attr(755,root,root) %{_bindir}/fontconfig-config
%{_includedir}/fontconfig
%{_libdir}/lib*.so
%{_pkgconfigdir}/fontconfig.pc
%{_mandir}/man3/*.3*
