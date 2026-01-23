"""Tests for the overall() function."""
import pytest

from condastats.cli import overall


def test_single_package_single_month():
    """Test overall counts for a single package in a single month."""
    result = overall('pandas', month='2019-01')
    assert result.loc['pandas'] == 932443


def test_multiple_packages_single_month():
    """Test overall counts for multiple packages in a single month."""
    result = overall(['pandas', 'dask'], month='2019-01')
    assert result.loc['pandas'] == 932443
    assert result.loc['dask'] == 221200


def test_with_all_filters():
    """Test overall counts with all filter parameters."""
    result = overall(
        'pandas',
        month='2019-01',
        pkg_platform='linux-32',
        data_source='anaconda',
        pkg_version='0.10.0',
        pkg_python=2.6
    )
    assert result.loc['pandas'] == 12


@pytest.mark.parametrize("filter_name,filter_value", [
    ("pkg_platform", "linux-64"),
    ("data_source", "anaconda"),
])
def test_with_single_filter(filter_name, filter_value):
    """Test overall counts with a single filter."""
    result = overall('pandas', month='2019-01', **{filter_name: filter_value})
    assert result.loc['pandas'] > 0


def test_date_range():
    """Test overall counts for a date range."""
    result = overall('pandas', start_month='2019-01', end_month='2019-02')
    single_month = overall('pandas', month='2019-01')
    assert result.loc['pandas'] > single_month.loc['pandas']


def test_monthly_aggregation():
    """Test monthly aggregation returns multiple time periods."""
    result = overall('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 2
    assert len(result) >= 2


def test_complete():
    """Test overall with complete=True returns full DataFrame."""
    result = overall('pandas', month='2019-01', complete=True)
    assert hasattr(result, 'columns')
    assert 'pkg_name' in result.columns
