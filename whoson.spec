Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Summary(pl):	Protoko³u ¶ledzenia dynamicznie przydzielanych adresów IP
Name:		whoson
Version:	1.08
Release:	1
Group:		Networking
Group(pl):	Sieci
Copyright:	Public domain
Source:		ftp://ftp.average.org/pub/whoson/%{name}-%{version}.tar.gz
Patch0:		whoson-config.patch
Patch1:		whoson-autoconf.patch
BuildRoot:	/tmp/%{name}-%{version}-root

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
%setup  -q
%patch0 -p1
%patch1 -p1

%build
LDFLAGS="-s"; export LDFLAGS
%configure \
	--with-config="/etc/whoson.conf"
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make install install-man DESTDIR=$RPM_BUILD_ROOT

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
	touch /var/lock/subsys/whosond
	;;
  stop)
	show "Stopping whosond services: "
	killproc whosond
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
	/etc/rc.d/init.d/whosond stop 2> /dev/null
	/etc/rc.d/init.d/whosond start 2> /dev/null
else
	echo "Run \"/etc/rc.d/init.d/whosond start\" to start whosond daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del whosond
	/etc/rc.d/init.d/whosond stop 2> /dev/null
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/whosond
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
