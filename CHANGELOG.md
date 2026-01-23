# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-01-23

### Breaking Changes

- Drop Python 3.8 and 3.9 support; now requires Python 3.10 or 3.11
- Pin dependency versions for compatibility with legacy S3 parquet files:
  - `numpy>=1.16.5,<2.0.0`
  - `pandas>=1.5.0,<2.0.0`
  - `dask[dataframe]>=2023.1.0,<2024.3.0`
  - `pyarrow>=10.0.0,<15.0.0`

### Added

- Type hints for all public functions in `cli.py`
- Comprehensive test suite with 31 tests covering all CLI functions
- Test coverage for multiple packages (pandas, numpy, scipy, requests, dask)
- Dependabot configuration for automated dependency updates
- `observed=True` parameter to groupby calls (fixes pandas FutureWarning)

### Changed

- Migrate from `setup.py`/`versioneer` to `pyproject.toml`/`setuptools_scm`
- Move tests from `condastats/tests/` to top-level `tests/` directory
- Update project URLs to conda-incubator organization
- Update ReadTheDocs configuration to use Python 3.11
- Use SPDX license expression (BSD-3-Clause)
- Simplify test fixtures using factory pattern with caching

### Removed

- Travis CI configuration (now using GitHub Actions exclusively)
- Local conda recipe (conda-forge feedstock is authoritative)
- `requirements.txt` (dependencies defined in pyproject.toml)
- `setup.py`, `setup.cfg`, `versioneer.py`, `MANIFEST.in`

### Fixed

- Fix pandas 2.x incompatibility with legacy S3 parquet files (#17, #19, #24)
- Fix ValueError when reading parquet files (#19)
- Update GitHub Actions to latest versions
- Fix PyPI publish workflow to use supported Python version

## [0.2.1] - Previous release

See [GitHub releases](https://github.com/conda-incubator/condastats/releases) for earlier changelog.
