# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- MongoDB integration for data persistence
- Beautiful embed messages for notifications
- Pre-commit hooks for code quality
- CI/CD pipeline with GitHub Actions
- Automated dependency updates with Dependabot
- Release automation script
- Comprehensive documentation

### Changed

- Migrated from JSON file storage to MongoDB
- Enhanced message formatting with embeds
- Improved error handling and logging

### Fixed

- SSL certificate issues on macOS
- Token validation and error messages

## [1.0.0] - 2025-01-02

### Added

- Initial release of Spy Bot
- Discord bot for monitoring user presence and voice channels
- Status tracking (online, offline, idle, do not disturb)
- Voice channel time tracking
- Excluded room functionality
- Statistics command (!stats)
- Environment-based configuration
- JSON data persistence
- Beautiful notification messages

### Features

- Real-time status change notifications
- Voice channel entry/exit tracking
- Time calculation for each status and voice channel
- Configurable notification channel
- Configurable excluded voice channels
- User statistics with detailed time breakdown
- Persistent data storage
- Professional embed messages with colors and emojis

[Unreleased]: https://github.com/samuelramos/spy-bot/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/samuelramos/spy-bot/releases/tag/v1.0.0
