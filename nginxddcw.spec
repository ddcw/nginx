Name:		nginx
Version:	1.9.9
Release:	1%{?dist}
Summary:	nginx1.9.9 by ddcw

Group:		Applications/System
License:	ddcw
URL:		https://github.com/ddcw/nginx
Source0:	%{name}-%{version}.tar.gz

#BuildRequires:	make
#Requires:	make zlib zlib-devel gcc-c++ libtool  openssl openssl-devel pcre
Requires:	zlib zlib-devel openssl openssl-devel pcre

%define		_prefix		/u01/nginx


%description
this is for install nginx in oel74


%prep
%setup -q


%build
./configure --prefix=%{_prefix} --with-pcre --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-http_realip_module 
make 


%install
make install DESTDIR=%{buildroot}
#make install

%post
export os_v="6"
systemctl -h >/dev/null 2>&1 && export os_v="7"

sed -i 's/ 80\;/ 8888\;/' %{_prefix}/conf/nginx.conf
cat << EOF > %{_prefix}/html/index.html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx by DDCW!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>
<h1>Successful</h1>

<p>
you can visit https://github.com/ddcw/nginx to known more
<a href="https://github.com/ddcw/nginx">https://github.com/ddcw/nginx</a>.</p>

</body>
</html>
EOF

if  [ "${os_v}" -eq "7" ] 
then
cat << EOF > /usr/lib/systemd/system/nginxDDCW.service
[Unit]
Description=nginx by ddcw
After=network.target

[Service]
Type=forking
PIDFile=%{_prefix}/logs/nginx.pid
ExecStart=%{_prefix}/sbin/nginx
ExecReload=%{_prefix}/sbin/nginx -s reload
ExecStop=%{_prefix}/sbin/nginx -s stop
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
chmod 754 /usr/lib/systemd/system/nginxDDCW.service
systemctl daemon-reload
systemctl enable nginxDDCW
systemctl restart nginxDDCW
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m systemctl start nginxDDCW   \033[0m to start nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m systemctl stop nginxDDCW    \033[0m to stop nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m systemctl restart nginxDDCW \033[0m to restart nginx status"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m systemctl reload nginxDDCW  \033[0m to reload nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m systemctl status nginxDDCW  \033[0m to known nginx status"
fi
if [ "${os_v}" -eq "6" ]
then
cat << EOF > /etc/rc.d/init.d/nginxDDCW
#chkconfig: 2345 80 05   
#description: nginx 1.9.9 by ddcw
case \$1 in
start)
	%{_prefix}/sbin/nginx
    ;;
stop)
        %{_prefix}/sbin/nginx -s stop
    ;;
restart)
	service nginxDDCW stop
	service nginxDDCW start
    ;;
reload)
	%{_prefix}/sbin/nginx -s reload
    ;;
status)
	ps -ef |grep nginx | grep -v grep | grep -v status |  grep --color nginx
    ;;
*)
    ;;
esac
EOF
chmod +x /etc/rc.d/init.d/nginxDDCW
service nginxDDCW restart 2>/dev/null
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m service nginxDDCW start  \033[0m to start nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m service nginxDDCW stop   \033[0m to stop nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m service nginxDDCW restart\033[0m to restart nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m service nginxDDCW reolad \033[0m to reload nginx"
echo -e "[\033[32;40mINFO\033[0m `date +%Y%m%d-%H:%M:%S`] you can run \033[32;40m service nginxDDCW status \033[0m to known nginx status"

fi

%files
%doc
%{_prefix}

%postun
#systemctl -h >/dev/null 2>&1 && cat %{_prefix}/logs/nginx.pid | xargs -t -i kill -9 \{\} >/dev/null 2>&1 || ps -ef | grep nginx | grep -v  grep| awk '{print $2}' | xargs -t -i kill -9 {}
cat %{_prefix}/logs/nginx.pid | xargs -t -i kill -9 \{\} >/dev/null 2>&1 
#systemctl -h >/dev/null 2>&1 || ps -ef | grep nginx | grep -v  grep| awk '{print $2}' | xargs -t -i kill -9 {}
rm -rf %{_prefix} 2>/dev/null


%changelog
#write at 20200427 by ddcw first
