"""Pytest fixtures for condastats tests.

Session-scoped fixtures fetch data once and reuse across all tests.
"""
import pytest

from condastats.cli import (
    overall,
    pkg_platform,
    pkg_version,
    pkg_python,
    data_source,
)

TEST_PACKAGE = 'pandas'
TEST_PACKAGES = ['pandas', 'dask']
TEST_MONTH = '2019-01'
TEST_START_MONTH = '2019-01'
TEST_END_MONTH = '2019-02'


# Overall fixtures

@pytest.fixture(scope="session")
def pandas_overall():
    return overall(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_complete():
    return overall(TEST_PACKAGE, month=TEST_MONTH, complete=True)


@pytest.fixture(scope="session")
def multi_package_overall():
    return overall(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_filtered():
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
    return overall(TEST_PACKAGE, start_month=TEST_START_MONTH, end_month=TEST_END_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_monthly():
    return overall(
        TEST_PACKAGE,
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


# Groupby fixtures - single package

@pytest.fixture(scope="session")
def pandas_pkg_platform():
    return pkg_platform(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_data_source():
    return data_source(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_pkg_version():
    return pkg_version(TEST_PACKAGE, month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_pkg_python():
    return pkg_python(TEST_PACKAGE, month=TEST_MONTH)


# Groupby fixtures - multiple packages

@pytest.fixture(scope="session")
def multi_package_pkg_platform():
    return pkg_platform(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_data_source():
    return data_source(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_version():
    return pkg_version(TEST_PACKAGES, month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_python():
    return pkg_python(TEST_PACKAGES, month=TEST_MONTH)


# Groupby fixtures - monthly

@pytest.fixture(scope="session")
def pandas_pkg_platform_monthly():
    return pkg_platform(
        TEST_PACKAGE,
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


@pytest.fixture(scope="session")
def pandas_data_source_monthly():
    return data_source(
        TEST_PACKAGE,
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )
