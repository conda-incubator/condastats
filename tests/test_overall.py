"""Tests for the overall() function."""

import pandas as pd
import pytest
from constants import (
    TEST_END_MONTH,
    TEST_MONTH,
    TEST_PACKAGES_DATA,
    TEST_START_MONTH,
)


@pytest.mark.parametrize("package", TEST_PACKAGES_DATA.keys())
def test_single_package(get_overall, package):
    """Test overall counts for individual packages."""
    result = get_overall(package, month=TEST_MONTH)
    assert result.loc[package] == TEST_PACKAGES_DATA[package]["overall"]


def test_multiple_packages(get_overall):
    """Test overall counts for multiple packages."""
    result = get_overall(["pandas", "numpy", "scipy"], month=TEST_MONTH)
    assert result.loc["pandas"] == TEST_PACKAGES_DATA["pandas"]["overall"]
    assert result.loc["numpy"] == TEST_PACKAGES_DATA["numpy"]["overall"]
    assert result.loc["scipy"] == TEST_PACKAGES_DATA["scipy"]["overall"]


def test_with_filters(get_overall):
    """Test overall counts with filter parameters."""
    result = get_overall(
        "pandas",
        month=TEST_MONTH,
        pkg_platform="linux-32",
        data_source="anaconda",
        pkg_version="0.10.0",
        pkg_python=2.6,
    )
    assert result.loc["pandas"] == 12


def test_date_range(get_overall):
    """Test overall counts for a date range exceeds single month."""
    single = get_overall("pandas", month=TEST_MONTH)
    range_result = get_overall(
        "pandas", start_month=TEST_START_MONTH, end_month=TEST_END_MONTH
    )
    assert range_result.loc["pandas"] > single.loc["pandas"]


def test_monthly_aggregation(get_overall):
    """Test monthly aggregation returns multiple time periods."""
    result = get_overall(
        "pandas",
        start_month=TEST_START_MONTH,
        end_month=TEST_END_MONTH,
        monthly=True,
    )
    assert result.index.nlevels == 2
    assert len(result) >= 2


def test_complete(get_overall):
    """Test complete=True returns full DataFrame."""
    result = get_overall("pandas", month=TEST_MONTH, complete=True)
    assert isinstance(result, pd.DataFrame)
    assert "pkg_name" in result.columns
    assert "counts" in result.columns
    assert "time" in result.columns


def test_tuple_input(get_overall):
    """Test that tuple input works the same as list input."""
    result = get_overall(("pandas", "numpy"), month=TEST_MONTH)
    assert "pandas" in result.index
    assert "numpy" in result.index
