# Changelog

All notable changes to `ai-stability` are documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]

### Changed

- Advanced the development version on `main` to `0.1.3` after the `0.1.2` release.

### Infrastructure

- Automated tag-driven PyPI publishing with GitHub Actions and Trusted Publishing.
- Automated matching GitHub release creation after successful package publish.
- Updated workflow actions to current release lines and cleaned package metadata warnings.

## [0.1.2] - 2026-04-06

### Added

- Automated PyPI release via GitHub Actions on version tags.

### Fixed

- Cleaned packaging metadata to use SPDX-style license configuration.

## [0.1.1] - 2026-04-06

### Added

- Trusted Publishing workflow for PyPI releases.
- Improved release documentation and repository metadata.

### Changed

- Added `pipx` as the recommended install path for end users.

## [0.1.0] - 2026-04-06

### Added

- Initial public release of `ai-stability`.
- CLI-first repeated prompt execution against OpenAI models.
- Pairwise similarity scoring and aggregate stability score.
- Inline diffing of output variation.
- Local JSON artifact saving for replay and debugging.
- Test coverage for scoring and end-to-end orchestration.
