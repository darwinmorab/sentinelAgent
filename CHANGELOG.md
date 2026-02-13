# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-13

### Added
- Initial release of SentinelAgent for POS monitoring
- System resource monitoring (CPU, memory, disk)
- POS endpoint health checking
- Configurable alert thresholds
- Support for JSON and YAML configuration files
- Metrics collection and retention system
- Comprehensive logging with multiple levels
- Command-line interface with continuous and single-run modes
- Unit tests with 15 test cases
- Example scripts and usage documentation
- Spanish documentation (README.md)
- Quick start guide (QUICKSTART.md)
- Example configuration files

### Features
- Real-time system metrics collection
- HTTP/HTTPS endpoint health checks
- Alert system based on configurable thresholds
- Metrics history with configurable retention
- Support for custom metrics recording
- Comprehensive error handling and logging
- Cross-platform support (Linux, macOS, Windows)

### Dependencies
- psutil >= 5.9.0 (system metrics)
- requests >= 2.28.0 (HTTP health checks)
- PyYAML >= 6.0 (YAML configuration support)

### Security
- No known vulnerabilities in dependencies
- CodeQL security scanning: 0 alerts
- No hardcoded credentials or secrets
