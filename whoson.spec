Summary:	Protocol for Keeping Track of Dynamically Allocated IP
Name:		whoson
Version:	1.06
Release:	1d
Source:		ftp://ftp.average.org/pub/whoson/%{name}-%{version}.tar.gz
Patch0:		%{name}.config.diff
Copyright:	Public domain
Group:		Networking
Group(pl):	Sieci	
BuildRoot:	/tmp/buildroot-%{name}-%{version}
Summary(pl):	Protoko³u ¶ledzenia dynamicznie przydzielanych adresów IP

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
CFLAGS=$RPM_OPT_FLAGS \
    ./configure %{_target} \
	--prefix=/usr \
	--with-config=/etc/whoson.conf
make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT/usr/{sbin,man/man{5,3,8},include,lib}

make \
    prefix=$RPM_BUILD_ROOT/usr \
    config=$RPM_BUILD_ROOT/etc/whoson.conf \
    install

make prefix=$RPM_BUILD_ROOT/usr install-man

strip       $RPM_BUILD_ROOT/usr/sbin/*
bzip2 -9    $RPM_BUILD_ROOT%{_mandir}/man{3,5,8}/* README whoson.txt

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

[ -f /usr/sbin/whosond ] || exit 0

# See how we were called.
case "\$1" in
  start)
	echo -n "Starting whosond: "
	daemon whosond
	echo
	touch /var/lock/subsys/whosond
	;;
  stop)
	echo -n "Stopping whosond services: "
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

%preun
if [ $1 = 0]; then
    /sbin/chkconfig --del whosond
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.bz2 whoson.txt.bz2

%attr(755,root,root) /usr/sbin/*
%attr(700,root,root) %config /etc/rc.d/init.d/whosond
%attr(640,root,root) %config %verify(not size mtime md5) /etc/whoson.conf
%attr(644,root, man) %{_mandir}/man[58]/*

%files devel
%attr(644,root,root) /usr/lib/*
%attr(644,root,root) /usr/include/*

%changelog
* Tue Jan 19 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
[1.06-1d]
- inital rpm release
