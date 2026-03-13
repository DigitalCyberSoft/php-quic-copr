# PHP-QUIC COPR Build Repository

Automated COPR build configuration for [php-quic](https://github.com/DigitalCyberSoft/php-quic) - PHP extension for the QUIC transport protocol (RFC 9000).

## Overview

This repository contains the COPR build configuration to automatically build RPM packages for the PHP QUIC extension from GitHub releases.

## Features

- **Automated Builds**: Builds directly from php-quic GitHub releases
- **PHP Version Support**: Builds for the system PHP version (8.0+)
- **NTS and ZTS Support**: Builds both non-thread-safe and thread-safe variants
- **Load Test**: Validates extension loads correctly during build

## COPR Repository

The built packages are available in COPR at:
```
https://copr.fedorainfracloud.org/coprs/reversejames/php-quic/
```

### Installation

```bash
# Enable the COPR repository
sudo dnf copr enable reversejames/php-quic

# Install php-quic
sudo dnf install php-quic

# For development headers
sudo dnf install php-quic-devel

# Restart PHP-FPM if using it
sudo systemctl restart php-fpm
```

## Configuration

The extension is configured via `/etc/php.d/40-quic.ini`:
```ini
; Enable quic extension module
extension = quic.so
```

## Verification

```bash
php -m | grep quic
php -i | grep quic
```

## Build Process

1. Downloads the php-quic source from GitHub release tag
2. Validates version against `php_quic.h`
3. Generates RPM spec file dynamically
4. Builds SRPM for COPR

## Local Testing

```bash
cd .copr
make srpm
```

## Dependencies

- **Build**: gcc, make, php-devel (>= 8.0), openssl-devel (>= 3.2)
- **Runtime**: php, openssl (>= 3.2)

## Extension Features

- QUIC client connections (RFC 9000)
- Bidirectional and unidirectional streams
- TLS 1.3 configuration (ALPN, ciphersuites, peer verification)
- Connection statistics and error handling
- Stream lifecycle management (conclude, reset)

## License

The build configuration is provided as-is. php-quic is licensed under the MIT License.

## Upstream

- php-quic GitHub: https://github.com/DigitalCyberSoft/php-quic
- RFC 9000 (QUIC): https://www.rfc-editor.org/rfc/rfc9000
- OpenSSL QUIC: https://www.openssl.org/docs/man3.2/man7/openssl-quic.html
