Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Summary(pl):	Protoko³u ¶ledzenia dynamicznie przydzielanych adresów IP
Name:		whoson
Version:	2.02a
Release:	2
Group:		Networking
License:	Public domain
Source0:	http://prdownloads.sourceforge.net/whoson/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.conf
Prereq:		rc-scripts
BuildRequires:	autoconf
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_sbindir}
%define		_sysconfigdir	/etc

%description
Simple method for Internet server programs to know if a particular
(dynamically allocated) IP address is currently allocated to a known
(trusted) user and, optionally, the identity of the said user.

%description -l pl
Program oraz biblioteka bêd±ce implementacj± protoko³u WHOSON
pozwalaj±cego innym programom na ¶ledzenie dynamicznie przydzielanych
IP u¿ywanych przez znanych (zaufanych) u¿ytkoników.

%package server
Summary:	Whoson server binary and scripts
Summary(pl):	Plik binarny i skrypty serwera whoson
Group:		Networking/Daemons
Requires:	whoson

%description server
Whoson server binary and scripts.

%description -l pl server
Plik binarny i skrypty serwera whoson.

%package devel
Summary:	Header files and development docomentation for whoson
Summary(pl):	Pliki nag³ówkowe i dokumentacja dla dla programistów do whoson-a
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This is whoson development package. It includes files and development
docomentation for whoson.

%description -l pl devel
To jest pakiet dla programistów. Zawiera pliki nag³ówkowe i
dokumentacja do whoson-a.

%package static
Summary:	Static whoson library
Summary(pl):	Biblioteka statyczna whoson-a
Group:		Development/Libraries
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

for i in wso_login wso_logout wso_query wso_version; do
	rm -f $RPM_BUILD_ROOT%{_mandir}/man3/$i.3
	echo ".so whoson.3" > $RPM_BUILD_ROOT%{_mandir}/man3/$i.3
done

gzip -9nf README whoson.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post server
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
