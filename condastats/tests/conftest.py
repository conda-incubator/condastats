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

TEST_MONTH = '2019-01'
TEST_START_MONTH = '2019-01'
TEST_END_MONTH = '2019-02'

# Test packages with known download counts for 2019-01
TEST_PACKAGES_DATA = {
    'pandas': {'overall': 932443, 'platform': 'linux-64', 'source': 'anaconda'},
    'numpy': {'overall': 2301341, 'platform': 'linux-64', 'source': 'anaconda'},
    'scipy': {'overall': 1065864, 'platform': 'linux-64', 'source': 'anaconda'},
    'requests': {'overall': 889856, 'platform': 'linux-64', 'source': 'anaconda'},
    'dask': {'overall': 221200, 'platform': 'linux-64', 'source': 'anaconda'},
}


# Overall fixtures - individual packages

@pytest.fixture(scope="session")
def pandas_overall():
    return overall('pandas', month=TEST_MONTH)


@pytest.fixture(scope="session")
def numpy_overall():
    return overall('numpy', month=TEST_MONTH)


@pytest.fixture(scope="session")
def scipy_overall():
    return overall('scipy', month=TEST_MONTH)


@pytest.fixture(scope="session")
def requests_overall():
    return overall('requests', month=TEST_MONTH)


@pytest.fixture(scope="session")
def dask_overall():
    return overall('dask', month=TEST_MONTH)


# Overall fixtures - special cases

@pytest.fixture(scope="session")
def pandas_overall_complete():
    return overall('pandas', month=TEST_MONTH, complete=True)


@pytest.fixture(scope="session")
def multi_package_overall():
    return overall(['pandas', 'numpy', 'scipy'], month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_filtered():
    return overall(
        'pandas',
        month=TEST_MONTH,
        pkg_platform='linux-32',
        data_source='anaconda',
        pkg_version='0.10.0',
        pkg_python=2.6
    )


@pytest.fixture(scope="session")
def pandas_overall_range():
    return overall('pandas', start_month=TEST_START_MONTH, end_month=TEST_END_MONTH)


@pytest.fixture(scope="session")
def pandas_overall_monthly():
    return overall(
        'pandas',
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


# Groupby fixtures - pandas

@pytest.fixture(scope="session")
def pandas_pkg_platform():
    return pkg_platform('pandas', month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_data_source():
    return data_source('pandas', month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_pkg_version():
    return pkg_version('pandas', month=TEST_MONTH)


@pytest.fixture(scope="session")
def pandas_pkg_python():
    return pkg_python('pandas', month=TEST_MONTH)


# Groupby fixtures - numpy

@pytest.fixture(scope="session")
def numpy_pkg_platform():
    return pkg_platform('numpy', month=TEST_MONTH)


@pytest.fixture(scope="session")
def numpy_data_source():
    return data_source('numpy', month=TEST_MONTH)


@pytest.fixture(scope="session")
def numpy_pkg_version():
    return pkg_version('numpy', month=TEST_MONTH)


@pytest.fixture(scope="session")
def numpy_pkg_python():
    return pkg_python('numpy', month=TEST_MONTH)


# Groupby fixtures - multiple packages

@pytest.fixture(scope="session")
def multi_package_pkg_platform():
    return pkg_platform(['pandas', 'numpy'], month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_data_source():
    return data_source(['pandas', 'numpy'], month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_version():
    return pkg_version(['pandas', 'numpy'], month=TEST_MONTH)


@pytest.fixture(scope="session")
def multi_package_pkg_python():
    return pkg_python(['pandas', 'numpy'], month=TEST_MONTH)


# Groupby fixtures - monthly

@pytest.fixture(scope="session")
def pandas_pkg_platform_monthly():
    return pkg_platform(
        'pandas',
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )


@pytest.fixture(scope="session")
def pandas_data_source_monthly():
    return data_source(
        'pandas',
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True
    )
