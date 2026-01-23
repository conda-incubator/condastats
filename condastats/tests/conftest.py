"""Pytest configuration and shared fixtures.

Session-scoped fixtures fetch data once and reuse across all tests,
reducing test runtime by avoiding repeated S3 queries.
"""
import pytest

from condastats.cli import (
    overall,
    pkg_platform,
    pkg_version,
    pkg_python,
    data_source,
)


# Common test parameters
TEST_PACKAGE = 'pandas'
TEST_PACKAGES = ['pandas', 'dask']
TEST_MONTH = '2019-01'
TEST_START_MONTH = '2019-01'
TEST_END_MONTH = '2019-02'


# Session-scoped fixtures for overall() tests

@pytest.fixture(scope="session")
def pandas_overall():
    """Overall stats for pandas in test month."""
    return overall(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_complete():
    """Complete DataFrame for pandas in test month."""
    return overall(TEST_PACKAGE, month=TEST_MONTH, complete=True)


@pytest.fixture(scope="session")
def multi_package_overall():
    """Overall stats for multiple packages in test month."""
    return overall(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_filtered():
    """Overall stats for pandas with all filters applied."""
    return overall(
        TEST_PACKAGE,
        month=TEST_MONTH,
        pkg_platform='linux-32',
        data_source='anaconda',
        pkg_version='0.10.0',
        pkg_python=2.6
    )


@pytest.fixture(scope="session")
def pandas_overall_range():
    """Overall stats for pandas across date range."""
    return overall(TEST_PACKAGE, start_month=TEST_START_MONTH, end_month=TEST_END_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_monthly():
    """Monthly overall stats for pandas across date range."""
    return overall(
        TEST_PACKAGE,
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


# Session-scoped fixtures for groupby tests

@pytest.fixture(scope="session")
def pandas_pkg_platform():
    """Platform breakdown for pandas in test month."""
    return pkg_platform(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_platform():
    """Platform breakdown for multiple packages in test month."""
    return pkg_platform(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_pkg_platform_monthly():
    """Monthly platform breakdown for pandas across date range."""
    return pkg_platform(
        TEST_PACKAGE,
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


@pytest.fixture(scope="session")
def pandas_data_source():
    """Data source breakdown for pandas in test month."""
    return data_source(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_data_source():
    """Data source breakdown for multiple packages in test month."""
    return data_source(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_data_source_monthly():
    """Monthly data source breakdown for pandas across date range."""
    return data_source(
        TEST_PACKAGE,
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


@pytest.fixture(scope="session")
def pandas_pkg_version():
    """Version breakdown for pandas in test month."""
    return pkg_version(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_version():
    """Version breakdown for multiple packages in test month."""
    return pkg_version(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_pkg_python():
    """Python version breakdown for pandas in test month."""
    return pkg_python(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_python():
    """Python version breakdown for multiple packages in test month."""
    return pkg_python(TEST_PACKAGES, month=TEST_MONTH)
