Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Summary(pl):	Protoko³u ¶ledzenia dynamicznie przydzielanych adresów IP
Name:		whoson
Version:	2.00
Release:	1
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
Copyright:	Public domain
Source0:	ftp://ftp.average.org/pub/whoson/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-config.patch
Patch1:		%{name}-autoconf.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Prereq:		rc-scripts
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

%package devel
Summary:	Header files and development docomentation for whoson
Summary(pl):	Pliki nag³ówkowe i dokumentacja dla dla programistów do whoson-a
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
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
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description devel
Static whoson library.

%description -l pl static
Biblioteka statyczna whoson-a.
%prep
%setup  -q
%patch0 -p1
# %patch1 -p1

%build
libtoolize -c -f
autoheader
aclocal
autoconf
automake -a -c
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/whoson.{s,d}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -m 644 whoson.conf $RPM_BUILD_ROOT/etc/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/whosond

gzip -9nf README whoson.txt

%post
/sbin/ldconfig
/sbin/chkconfig --add whosond
if [ -f /var/lock/subsys/whosond ]; then
	/etc/rc.d/init.d/whosond restart >&2
else
	echo "Run \"/etc/rc.d/init.d/whosond start\" to start whosond daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del whosond
	if [ -f /var/lock/subsys/whosond ]; then
		/etc/rc.d/init.d/whosond stop >&2
	fi
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(754,root,root) /etc/rc.d/init.d/whosond
%config %verify(not size mtime md5) %{_sysconfigdir}/whoson.conf
%{_mandir}/man[58]/*
%dir /var/run/whoson.s
%dir /var/run/whoson.d

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
