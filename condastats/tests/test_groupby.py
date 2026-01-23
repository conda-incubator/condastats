"""Tests for groupby functions: pkg_platform, pkg_version, pkg_python, data_source."""
import pytest


@pytest.mark.parametrize("fixture_name,column,expected_value", [
    ("pandas_pkg_platform", "pkg_platform", "linux-64"),
    ("pandas_data_source", "data_source", "anaconda"),
    ("pandas_pkg_version", "pkg_version", None),
    ("pandas_pkg_python", "pkg_python", None),
])
def test_single_package(fixture_name, column, expected_value, request):
    """Test groupby breakdown for a single package."""
    result = request.getfixturevalue(fixture_name)
    assert len(result) > 1
    values = result.index.get_level_values(column).unique()
    if expected_value:
        assert expected_value in values
    else:
        assert len(values) > 1


@pytest.mark.parametrize("fixture_name", [
    "multi_package_pkg_platform",
    "multi_package_data_source",
    "multi_package_pkg_version",
    "multi_package_pkg_python",
])
def test_multiple_packages(fixture_name, request):
    """Test groupby breakdown for multiple packages."""
    result = request.getfixturevalue(fixture_name)
    packages = result.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


@pytest.mark.parametrize("fixture_name", [
    "pandas_pkg_platform_monthly",
    "pandas_data_source_monthly",
])
def test_monthly_aggregation(fixture_name, request):
    """Test groupby with monthly aggregation."""
    result = request.getfixturevalue(fixture_name)
    assert result.index.nlevels == 3
