"""Tests for groupby functions: pkg_platform, pkg_version, pkg_python, data_source."""

import pytest
from constants import TEST_END_MONTH, TEST_MONTH, TEST_START_MONTH


@pytest.mark.parametrize(
    "func_name,column,expected_value",
    [
        ("pkg_platform", "pkg_platform", "linux-64"),
        ("data_source", "data_source", "anaconda"),
        ("pkg_version", "pkg_version", None),
        ("pkg_python", "pkg_python", None),
    ],
)
@pytest.mark.parametrize("package", ["pandas", "numpy"])
def test_single_package(get_groupby, func_name, column, expected_value, package):
    """Test groupby breakdown for individual packages."""
    result = get_groupby(func_name, package, month=TEST_MONTH)
    assert len(result) > 1
    values = result.index.get_level_values(column).unique()
    if expected_value:
        assert expected_value in values
    else:
        assert len(values) > 1


@pytest.mark.parametrize(
    "func_name", ["pkg_platform", "data_source", "pkg_version", "pkg_python"]
)
def test_multiple_packages(get_groupby, func_name):
    """Test groupby breakdown for multiple packages."""
    result = get_groupby(func_name, ["pandas", "numpy"], month=TEST_MONTH)
    packages = result.index.get_level_values("pkg_name").unique()
    assert "pandas" in packages
    assert "numpy" in packages


@pytest.mark.parametrize("func_name", ["pkg_platform", "data_source"])
def test_monthly_aggregation(get_groupby, func_name):
    """Test groupby with monthly aggregation."""
    result = get_groupby(
        func_name,
        "pandas",
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True,
    )
    assert result.index.nlevels == 3
