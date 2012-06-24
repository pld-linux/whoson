Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Summary(pl):	Protoko�u �ledzenia dynamicznie przydzielanych adres�w IP
Name:		whoson
Version:	2.02a
Release:	1
Group:		Networking
Group(de):	Netzwerkwesen
Group(es):	Red
Group(pl):	Sieciowe
Group(pt_BR):	Rede
License:	Public domain
Source0:	http://prdownloads.sourceforge.net/whoson/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.conf
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_sysconfigdir	/etc

%description
Simple method for Internet server programs to know if a particular
(dynamically allocated) IP address is currently allocated to a known
(trusted) user and, optionally, the identity of the said user.

%description -l pl
Program oraz biblioteka b�d�ce implementacj� protoko�u WHOSON
pozwalaj�cego innym programom na �ledzenie dynamicznie przydzielanych
IP u�ywanych przez znanych (zaufanych) u�ytkonik�w.

%package server
Summary:	Whoson server binary and scripts
Summary(pl):	Plik binarny i skrypty serwera whoson
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	whoson

%description server
Whoson server binary and scripts

%description -l pl server
Plik binarny i skrypty serwera whoson

%package devel
Summary:	Header files and development docomentation for whoson
Summary(pl):	Pliki nag��wkowe i dokumentacja dla dla programist�w do whoson-a
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	%{name} = %{version}

%description devel
This is whoson development package. It includes files and development
docomentation for whoson.

%description -l pl devel
To jest pakiet dla programist�w. Zawiera pliki nag��wkowe i
dokumentacja do whoson-a.

%package static
Summary:	Static whoson library
Summary(pl):	Biblioteka statyczna whoson-a
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	%{name}-devel = %{version}

%description static
Static whoson library.

%description -l pl static
Biblioteka statyczna whoson-a.

%prep
%setup  -q

%build
autoconf
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/lib/whosond}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/whosond
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/

gzip -9nf README whoson.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post server
/sbin/ldconfig
/sbin/chkconfig --add whosond
if [ -f /var/lock/subsys/whosond ]; then
	/etc/rc.d/init.d/whosond restart >&2
else
	echo "Run \"/etc/rc.d/init.d/whosond start\" to start whosond daemon."
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/whosond ]; then
		/etc/rc.d/init.d/whosond stop >&2
	fi
	/sbin/chkconfig --del whosond
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/whoson
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%config %verify(not size mtime md5) %{_sysconfigdir}/whoson.conf
%{_mandir}/man[58]/*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/whosond
%attr(754,root,root) /etc/rc.d/init.d/whosond
%dir /var/lib/whosond
%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
