# COPR Makefile for automated php-quic builds
# Downloads php-quic from GitHub and builds PHP extension

# COPR provides outdir, set default for local testing
outdir ?= .

# Fetch latest release version from GitHub (strip v prefix)
QUIC_VERSION := $(shell curl -s https://api.github.com/repos/DigitalCyberSoft/php-quic/releases/latest | sed -n 's/.*"tag_name": *"v\?\([^"]*\)".*/\1/p')
QUIC_URL = https://github.com/DigitalCyberSoft/php-quic/archive/refs/tags/v$(QUIC_VERSION).tar.gz

# Default target for COPR
srpm:
	@echo "=== Starting php-quic SRPM build ==="
	@echo "Output directory: $(outdir)"
	@echo "Working directory: $$(pwd)"

	# Download php-quic source
	@echo "=== Downloading php-quic $(QUIC_VERSION) ==="
	curl -L -o php-quic-$(QUIC_VERSION).tar.gz $(QUIC_URL) || exit 1

	# Extract and prepare source
	@echo "=== Preparing source ==="
	tar xzf php-quic-$(QUIC_VERSION).tar.gz || exit 1
	mv php-quic-$(QUIC_VERSION) php-quic-temp
	tar czf php-quic-$(QUIC_VERSION).tar.gz php-quic-temp/ --transform='s/php-quic-temp/php-quic-$(QUIC_VERSION)/' || exit 1
	rm -rf php-quic-temp/

	# Generate spec file
	@echo "=== Generating spec file ==="; \
	( \
	echo '# we dont want -z defs linker flag'; \
	echo '%undefine _strict_symbol_defs_build'; \
	echo ''; \
	echo '%global pecl_name   quic'; \
	echo '%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}'; \
	echo '%global ini_name    40-%{pecl_name}.ini'; \
	echo ''; \
	echo 'Name:           php-%{pecl_name}'; \
	echo 'Version:        $(QUIC_VERSION)'; \
	echo 'Release:        1.php%{php_version}%{?dist}'; \
	echo 'Summary:        QUIC protocol extension for PHP (RFC 9000)'; \
	echo ''; \
	echo 'License:        MIT'; \
	echo 'URL:            https://github.com/DigitalCyberSoft/php-quic'; \
	echo 'Source0:        php-quic-%{version}.tar.gz'; \
	echo ''; \
	echo 'BuildRequires:  gcc'; \
	echo 'BuildRequires:  make'; \
	echo 'BuildRequires:  php-devel >= 8.0'; \
	echo 'BuildRequires:  openssl-devel >= 3.2'; \
	echo ''; \
	echo 'Requires:       php(zend-abi) = %{php_zend_api}'; \
	echo 'Requires:       php(api) = %{php_core_api}'; \
	echo 'Requires:       openssl >= 3.2'; \
	echo ''; \
	echo '%description'; \
	echo 'PHP extension for the QUIC transport protocol as defined in RFC 9000.'; \
	echo 'QUIC is the transport protocol used by HTTP/3.'; \
	echo ''; \
	echo 'Wraps OpenSSL 3.2+ QUIC support to provide client connections,'; \
	echo 'bidirectional and unidirectional streams, TLS configuration,'; \
	echo 'and connection statistics.'; \
	echo ''; \
	echo '%package devel'; \
	echo 'Summary:        Development files for %{name}'; \
	echo 'Requires:       %{name}%{?_isa} = %{version}-%{release}'; \
	echo 'Requires:       php-devel%{?_isa}'; \
	echo ''; \
	echo '%description devel'; \
	echo 'These are the files needed to compile programs using %{name}.'; \
	echo ''; \
	echo '%prep'; \
	echo '%setup -q -n php-quic-%{version}'; \
	echo ''; \
	echo '# Sanity check'; \
	echo 'extver=$$(sed -n '"'"'/#define PHP_QUIC_VERSION/{s/.* "//;s/".*$$//;p}'"'"' php_quic.h)'; \
	echo 'if test "x$${extver}" != "x%{version}"; then'; \
	echo '   : Error: Upstream extension version is $${extver}, expecting %{version}.'; \
	echo '   exit 1'; \
	echo 'fi'; \
	echo ''; \
	echo '%if %{with_zts}'; \
	echo '# Duplicate for ZTS build'; \
	echo 'cp -pr . ../ZTS'; \
	echo '%endif'; \
	echo ''; \
	echo '%build'; \
	echo '# NTS build'; \
	echo '%{_bindir}/phpize'; \
	echo '%configure \'; \
	echo '    --with-php-config=%{_bindir}/php-config \'; \
	echo '    --with-libdir=%{_lib} \'; \
	echo '    --enable-quic'; \
	echo ''; \
	echo 'make %{?_smp_mflags}'; \
	echo ''; \
	echo '%if %{with_zts}'; \
	echo '# ZTS build'; \
	echo 'cd ../ZTS'; \
	echo '%{_bindir}/zts-phpize'; \
	echo '%configure \'; \
	echo '    --with-php-config=%{_bindir}/zts-php-config \'; \
	echo '    --with-libdir=%{_lib} \'; \
	echo '    --enable-quic'; \
	echo ''; \
	echo 'make %{?_smp_mflags}'; \
	echo '%endif'; \
	echo ''; \
	echo '%install'; \
	echo '# Install NTS extension'; \
	echo 'make install INSTALL_ROOT=%{buildroot}'; \
	echo ''; \
	echo '# Install config file'; \
	echo 'install -d %{buildroot}%{php_inidir}'; \
	echo 'cat > %{buildroot}%{php_inidir}/%{ini_name} << EOF'; \
	echo '; Enable quic extension module'; \
	echo 'extension = %{pecl_name}.so'; \
	echo 'EOF'; \
	echo ''; \
	echo '%if %{with_zts}'; \
	echo '# Install ZTS extension'; \
	echo 'cd ../ZTS'; \
	echo 'make install INSTALL_ROOT=%{buildroot}'; \
	echo ''; \
	echo '# Install ZTS config file'; \
	echo 'install -d %{buildroot}%{php_ztsinidir}'; \
	echo 'cp %{buildroot}%{php_inidir}/%{ini_name} \'; \
	echo '   %{buildroot}%{php_ztsinidir}/%{ini_name}'; \
	echo '%else'; \
	echo '# Remove any ZTS files that NTS make install may have created'; \
	echo 'find %{buildroot} -name "%{pecl_name}.so" -not -path "%{buildroot}%{php_extdir}/*" -delete 2>/dev/null || :'; \
	echo '%endif'; \
	echo ''; \
	echo '# Install headers for devel package'; \
	echo 'install -d %{buildroot}%{php_incldir}/ext/%{pecl_name}'; \
	echo 'cp -p php_quic.h %{buildroot}%{php_incldir}/ext/%{pecl_name}/'; \
	echo ''; \
	echo '%check'; \
	echo '# Minimal load test for NTS extension'; \
	echo '%{__php} --no-php-ini \'; \
	echo '    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \'; \
	echo '    --modules | grep "^%{pecl_name}$$"'; \
	echo ''; \
	echo '%if %{with_zts}'; \
	echo '# Minimal load test for ZTS extension'; \
	echo '%{__ztsphp} --no-php-ini \'; \
	echo '    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \'; \
	echo '    --modules | grep "^%{pecl_name}$$"'; \
	echo '%endif'; \
	echo ''; \
	echo '%files'; \
	echo '%license LICENSE'; \
	echo '%config(noreplace) %{php_inidir}/%{ini_name}'; \
	echo '%{php_extdir}/%{pecl_name}.so'; \
	echo ''; \
	echo '%if %{with_zts}'; \
	echo '%config(noreplace) %{php_ztsinidir}/%{ini_name}'; \
	echo '%{php_ztsextdir}/%{pecl_name}.so'; \
	echo '%endif'; \
	echo ''; \
	echo '%files devel'; \
	echo '%{php_incldir}/ext/%{pecl_name}'; \
	echo ''; \
	echo '%changelog'; \
	echo "* $$(date '+%a %b %d %Y') COPR Builder - $(QUIC_VERSION)-1"; \
	echo '- Automated build from GitHub release $(QUIC_VERSION)'; \
	echo '- QUIC transport protocol for HTTP/3 (RFC 9000)'; \
	echo '- Supports both NTS and ZTS builds'; \
	) > php-quic.spec || exit 1

	@echo "Spec file generated"

	# Build SRPM
	@echo "=== Building SRPM ==="
	rpmbuild -bs \
		--define "_sourcedir $$(pwd)" \
		--define "_specdir $$(pwd)" \
		--define "_builddir $$(pwd)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_rpmdir $$(pwd)" \
		php-quic.spec || exit 1

	@echo "=== SRPM build complete ==="
	ls -la $(outdir)/*.src.rpm

clean:
	@rm -f *.tar.gz *.spec *.src.rpm
	@rm -rf php-quic-*/

.PHONY: srpm clean
