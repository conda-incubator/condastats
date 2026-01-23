"""Tests for the overall() function."""


def test_single_package(pandas_overall):
    """Test overall counts for a single package."""
    assert pandas_overall.loc['pandas'] == 932443


def test_multiple_packages(multi_package_overall):
    """Test overall counts for multiple packages."""
    assert multi_package_overall.loc['pandas'] == 932443
    assert multi_package_overall.loc['dask'] == 221200


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
