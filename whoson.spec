Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Summary(pl.UTF-8):	Protokołu śledzenia dynamicznie przydzielanych adresów IP
Name:		whoson
Version:	2.04
Release:	1
License:	Public Domain
Group:		Networking
Source0:	http://dl.sourceforge.net/whoson/%{name}-%{version}.tar.gz
# Source0-md5:	e74d3484ebb3f002703f81e9e76d51b0
Source1:	%{name}.init
Source2:	%{name}.conf
URL:		http://whoson.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}

%description
Simple method for Internet server programs to know if a particular
(dynamically allocated) IP address is currently allocated to a known
(trusted) user and, optionally, the identity of the said user.

%description -l pl.UTF-8
Program oraz biblioteka będące implementacją protokołu WHOSON
pozwalającego innym programom na śledzenie dynamicznie przydzielanych
IP używanych przez znanych (zaufanych) użytkowników.

%package server
Summary:	Whoson server binary and scripts
Summary(pl.UTF-8):	Plik binarny i skrypty serwera whoson
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description server
Whoson server binary and scripts.

%description server -l pl.UTF-8
Plik binarny i skrypty serwera whoson.

%package devel
Summary:	Header files and development docomentation for whoson
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja dla dla programistów do whosona
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is whoson development package. It includes files and development
docomentation for whoson.

%description devel -l pl.UTF-8
To jest pakiet dla programistów. Zawiera pliki nagłówkowe i
dokumentację do whosona.

%package static
Summary:	Static whoson library
Summary(pl.UTF-8):	Biblioteka statyczna whosona
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static whoson library.

%description static -l pl.UTF-8
Biblioteka statyczna whosona.

%prep
%setup -q

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
%configure

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/lib/whosond}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/whosond
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}

for i in wso_login wso_logout wso_query wso_version; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man3/$i.3
	echo ".so whoson.3" > $RPM_BUILD_ROOT%{_mandir}/man3/$i.3
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add whosond
%service whosond restart "whosond daemon"

%preun server
if [ "$1" = "0" ]; then
	%service whosond stop
	/sbin/chkconfig --del whosond
fi

%files
%defattr(644,root,root,755)
%doc README whoson.txt
%attr(755,root,root) %{_sbindir}/whoson
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/whoson.conf
%{_mandir}/man[58]/*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/whosond
%attr(754,root,root) /etc/rc.d/init.d/whosond
%dir /var/lib/whosond

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
