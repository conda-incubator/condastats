"""Tests for the overall() function."""
import pytest

from condastats.cli import overall


def test_single_package_single_month(pandas_overall):
    """Test overall counts for a single package in a single month."""
    assert pandas_overall.loc['pandas'] == 932443


def test_multiple_packages_single_month(multi_package_overall):
    """Test overall counts for multiple packages in a single month."""
    assert multi_package_overall.loc['pandas'] == 932443
    assert multi_package_overall.loc['dask'] == 221200


def test_with_all_filters(pandas_overall_filtered):
    """Test overall counts with all filter parameters."""
    assert pandas_overall_filtered.loc['pandas'] == 12


@pytest.mark.parametrize("filter_name,filter_value", [
    ("pkg_platform", "linux-64"),
    ("data_source", "anaconda"),
])
def test_with_single_filter(pandas_overall, filter_name, filter_value):
    """Test overall counts with a single filter return subset of total."""
    filtered = overall('pandas', month='2019-01', **{filter_name: filter_value})
    # Filtered result should be less than total
    assert 0 < filtered.loc['pandas'] < pandas_overall.loc['pandas']


def test_date_range(pandas_overall, pandas_overall_range):
    """Test overall counts for a date range."""
    assert pandas_overall_range.loc['pandas'] > pandas_overall.loc['pandas']


def test_monthly_aggregation(pandas_overall_monthly):
    """Test monthly aggregation returns multiple time periods."""
    assert pandas_overall_monthly.index.nlevels == 2
    assert len(pandas_overall_monthly) >= 2


def test_complete(pandas_overall_complete):
    """Test overall with complete=True returns full DataFrame."""
    assert hasattr(pandas_overall_complete, 'columns')
    assert 'pkg_name' in pandas_overall_complete.columns
