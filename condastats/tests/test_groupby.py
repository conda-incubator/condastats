"""Tests for groupby functions: pkg_platform, pkg_version, pkg_python, data_source."""
from condastats.cli import pkg_platform, pkg_version, pkg_python, data_source


# Tests for pkg_platform()

def test_pkg_platform_single_package():
    """Test platform breakdown for a single package."""
    result = pkg_platform('pandas', month='2019-01')
    assert len(result) > 1
    platforms = result.index.get_level_values('pkg_platform').unique()
    assert 'linux-64' in platforms


def test_pkg_platform_multiple_packages():
    """Test platform breakdown for multiple packages."""
    result = pkg_platform(['pandas', 'dask'], month='2019-01')
    packages = result.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


def test_pkg_platform_monthly():
    """Test platform breakdown with monthly aggregation."""
    result = pkg_platform('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 3  # pkg_name, time, pkg_platform


# Tests for data_source()

def test_data_source_single_package():
    """Test data source breakdown for a single package."""
    result = data_source('pandas', month='2019-01')
    sources = result.index.get_level_values('data_source').unique()
    assert 'anaconda' in sources


def test_data_source_multiple_packages():
    """Test data source breakdown for multiple packages."""
    result = data_source(['pandas', 'dask'], month='2019-01')
    packages = result.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


def test_data_source_monthly():
    """Test data source breakdown with monthly aggregation."""
    result = data_source('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 3


# Tests for pkg_version()

def test_pkg_version_single_package():
    """Test version breakdown for a single package."""
    result = pkg_version('pandas', month='2019-01')
    assert len(result) > 1
    versions = result.index.get_level_values('pkg_version').unique()
    assert len(versions) > 1


def test_pkg_version_multiple_packages():
    """Test version breakdown for multiple packages."""
    result = pkg_version(['pandas', 'dask'], month='2019-01')
    packages = result.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


# Tests for pkg_python()

def test_pkg_python_single_package():
    """Test Python version breakdown for a single package."""
    result = pkg_python('pandas', month='2019-01')
    assert len(result) > 1
    python_versions = result.index.get_level_values('pkg_python').unique()
    assert len(python_versions) > 1


def test_pkg_python_multiple_packages():
    """Test Python version breakdown for multiple packages."""
    result = pkg_python(['pandas', 'dask'], month='2019-01')
    packages = result.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages
