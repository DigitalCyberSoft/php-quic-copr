# we dont want -z defs linker flag
%undefine _strict_symbol_defs_build

%global pecl_name   quic
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
%global ini_name    40-%{pecl_name}.ini

# Latest release version - update this to build a new version
%global upstream_version 1.0.0

Name:           php-%{pecl_name}
Version:        %{upstream_version}
Release:        1%{?dist}
Summary:        QUIC protocol extension for PHP (RFC 9000)

License:        MIT
URL:            https://github.com/DigitalCyberSoft/php-quic
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/php-quic-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  php-devel >= 8.0
BuildRequires:  openssl-devel >= 3.2

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       openssl >= 3.2

%description
PHP extension for the QUIC transport protocol as defined in RFC 9000.
QUIC is the transport protocol used by HTTP/3.

Wraps OpenSSL 3.2+ QUIC support to provide client connections,
bidirectional and unidirectional streams, TLS configuration,
and connection statistics.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       php-devel%{?_isa}

%description devel
These are the files needed to compile programs using %{name}.

%prep
%setup -q -n php-quic-%{version}

# Sanity check
extver=$(sed -n '/#define PHP_QUIC_VERSION/{s/.* "//;s/".*$//;p}' php_quic.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

%if %{with_zts}
# Duplicate for ZTS build
cp -pr . ../ZTS
%endif

%build
# NTS build
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --with-libdir=%{_lib} \
    --enable-quic

make %{?_smp_mflags}

%if %{with_zts}
# ZTS build
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    --with-libdir=%{_lib} \
    --enable-quic

make %{?_smp_mflags}
%endif

%install
# Install NTS extension
make install INSTALL_ROOT=%{buildroot}

# Install config file
install -d %{buildroot}%{php_inidir}
cat > %{buildroot}%{php_inidir}/%{ini_name} << EOF
; Enable quic extension module
extension = %{pecl_name}.so
EOF

%if %{with_zts}
# Install ZTS extension
cd ../ZTS
make install INSTALL_ROOT=%{buildroot}

# Install ZTS config file
install -d %{buildroot}%{php_ztsinidir}
cp %{buildroot}%{php_inidir}/%{ini_name} \
   %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Install headers for devel package
install -d %{buildroot}%{php_incldir}/ext/%{pecl_name}
cp -p php_quic.h %{buildroot}%{php_incldir}/ext/%{pecl_name}/

%check
# Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep "^%{pecl_name}$"

%if %{with_zts}
# Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep "^%{pecl_name}$"
%endif

%files
%license LICENSE
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif

%files devel
%{php_incldir}/ext/%{pecl_name}

%changelog
* Fri Mar 13 2026 James Campbell - 1.0.0-1
- Initial package
- QUIC transport protocol for HTTP/3 (RFC 9000)
- Requires OpenSSL 3.2+ with QUIC support
- Supports both NTS and ZTS builds
