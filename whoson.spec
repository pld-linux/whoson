Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Summary(pl):	Protoko³u ¶ledzenia dynamicznie przydzielanych adresów IP
Name:		whoson
Version:	1.07
Release:	1
Group:		Networking
Group(pl):	Sieci
Copyright:	Public domain
Source:		ftp://ftp.average.org/pub/whoson/%{name}-%{version}.tar.gz
Patch0:		whoson-config.patch
BuildRoot:	/tmp/buildroot-%{name}-%{version}

%description
Simple method for Internet server programs to know if a particular
(dynamically allocated) IP address is currently allocated to a known
(trusted) user and, optionally, the identity of the said user.

%description -l pl
Program oraz biblioteka bêd±ce implementacj± protoko³u WHOSON pozwalaj±cego
innym programom na ¶ledzenie dynamicznie przydzielanych IP u¿ywanych
przez znanych (zaufanych) u¿ytkoników.

%package devel
Summary:	Static library and header file for whoson
Summary(pl):	Plik nag³ówkowy i biblioteka statyczna dla whoson-a
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
This is whoson development package.
It includes static library and header file.

%description -l pl devel
To jest pakiet dla developerów.
Zawiera plik nag³ówkowy i bibliotekê statyczn± whoson-a.

%prep
%setup -q
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" \
./configure %{_target} \
	--prefix=%{_prefix} \
	--with-config=/etc/whoson.conf
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,3,8},%{_includedir},%_{libdir}}

make install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	config=$RPM_BUILD_ROOT/etc/whoson.conf

make prefix=$RPM_BUILD_ROOT/usr install-man

strip $RPM_BUILD_ROOT%{_sbindir}/*

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{3,5,8}/* README whoson.txt

cat  << EOF > $RPM_BUILD_ROOT/etc/rc.d/init.d/whosond
#!/bin/bash
#
# whosond       Start/Stop whosond server
#
# chkconfig: 345 40 65
# description:  whosond - implementation of WHOSON protocol
#

# Source function library.
. /etc/rc.d/init.d/functions

# Get config.
. /etc/sysconfig/network

# Check that networking is up.
if [ \${NETWORKING} = "no" ]
then
	exit 0
fi

[ -f %{_sbindir}/whosond ] || exit 0

# See how we were called.
case "\$1" in
  start)
	show "Starting whosond: "
	daemon whosond
	echo
	touch /var/lock/subsys/whosond
	;;
  stop)
	show "Stopping whosond services: "
	killproc whosond
	echo
	rm -f /var/lock/subsys/whosond
	;;
  status)
	status whosond
	;;
  restart|reload)
	\$0 stop
	\$0 start
	;;
  *)
	echo "Usage:\$0 {start|stop|status|restart|reload}"
	exit 1
esac

exit 0
EOF

%post
/sbin/chkconfig --add whosond
if test -r /var/run/whosond.pid; then
	/etc/rc.d/init.d/whosond stop >&2
	/etc/rc.d/init.d/whosond start >&2
else
	echo "Run \"/etc/rc.d/init.d/whosond start\" to start whosond daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del whosond
	/etc/rc.d/init.d/whosond stop >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.bz2 whoson.txt.bz2

%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) %config /etc/rc.d/init.d/whosond
%attr(640,root,root) %config %verify(not size mtime md5) /etc/whoson.conf
%{_mandir}/man[58]/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/*
%{_includedir}/*

%changelog
* Fri May 21 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.07-1]
- now package is FHS 2.0 compliant,
- gzipping %doc instaead bzippng2,
- standarized %post/%preun (restart service on upgrade, stop service on
  removing package).

* Tue Jan 19 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [1.06-1d]
- inital rpm release
