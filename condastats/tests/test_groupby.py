"""Tests for groupby functions: pkg_platform, pkg_version, pkg_python, data_source."""
import pytest

from condastats.cli import pkg_platform, pkg_version, pkg_python, data_source


@pytest.mark.parametrize("func,column,expected_value", [
    (pkg_platform, "pkg_platform", "linux-64"),
    (data_source, "data_source", "anaconda"),
    (pkg_version, "pkg_version", None),  # Just check multiple versions exist
    (pkg_python, "pkg_python", None),  # Just check multiple versions exist
])
def test_single_package(func, column, expected_value):
    """Test groupby breakdown for a single package."""
    result = func('pandas', month='2019-01')
    assert len(result) > 1
    values = result.index.get_level_values(column).unique()
    if expected_value:
        assert expected_value in values
    else:
        assert len(values) > 1


@pytest.mark.parametrize("func", [pkg_platform, data_source, pkg_version, pkg_python])
def test_multiple_packages(func):
    """Test groupby breakdown for multiple packages."""
    result = func(['pandas', 'dask'], month='2019-01')
    packages = result.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


@pytest.mark.parametrize("func", [pkg_platform, data_source])
def test_monthly_aggregation(func):
    """Test groupby with monthly aggregation."""
    result = func('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 3  # pkg_name, time, column
