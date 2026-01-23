"""Tests for the overall() function."""
import pytest

from condastats.tests.conftest import TEST_PACKAGES_DATA


@pytest.mark.parametrize("fixture_name,package,expected_count", [
    ("pandas_overall", "pandas", TEST_PACKAGES_DATA['pandas']['overall']),
    ("numpy_overall", "numpy", TEST_PACKAGES_DATA['numpy']['overall']),
    ("scipy_overall", "scipy", TEST_PACKAGES_DATA['scipy']['overall']),
    ("requests_overall", "requests", TEST_PACKAGES_DATA['requests']['overall']),
    ("dask_overall", "dask", TEST_PACKAGES_DATA['dask']['overall']),
])
def test_single_package(fixture_name, package, expected_count, request):
    """Test overall counts for individual packages."""
    result = request.getfixturevalue(fixture_name)
    assert result.loc[package] == expected_count


def test_multiple_packages(multi_package_overall):
    """Test overall counts for multiple packages."""
    assert multi_package_overall.loc['pandas'] == TEST_PACKAGES_DATA['pandas']['overall']
    assert multi_package_overall.loc['numpy'] == TEST_PACKAGES_DATA['numpy']['overall']
    assert multi_package_overall.loc['scipy'] == TEST_PACKAGES_DATA['scipy']['overall']


def test_with_filters(pandas_overall_filtered):
    """Test overall counts with filter parameters."""
    assert pandas_overall_filtered.loc['pandas'] == 12


def test_date_range(pandas_overall, pandas_overall_range):
    """Test overall counts for a date range exceeds single month."""
    assert pandas_overall_range.loc['pandas'] > pandas_overall.loc['pandas']


def test_monthly_aggregation(pandas_overall_monthly):
    """Test monthly aggregation returns multiple time periods."""
    assert pandas_overall_monthly.index.nlevels == 2
    assert len(pandas_overall_monthly) >= 2


def test_complete(pandas_overall_complete):
    """Test complete=True returns full DataFrame."""
    assert hasattr(pandas_overall_complete, 'columns')
    assert 'pkg_name' in pandas_overall_complete.columns
