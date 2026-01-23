"""Tests for groupby functions: pkg_platform, pkg_version, pkg_python, data_source."""
import pytest


def test_pkg_platform_single_package(pandas_pkg_platform):
    """Test platform breakdown for a single package."""
    assert len(pandas_pkg_platform) > 1
    platforms = pandas_pkg_platform.index.get_level_values('pkg_platform').unique()
    assert 'linux-64' in platforms


def test_pkg_platform_multiple_packages(multi_package_pkg_platform):
    """Test platform breakdown for multiple packages."""
    packages = multi_package_pkg_platform.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


def test_pkg_platform_monthly(pandas_pkg_platform_monthly):
    """Test platform breakdown with monthly aggregation."""
    assert pandas_pkg_platform_monthly.index.nlevels == 3


def test_data_source_single_package(pandas_data_source):
    """Test data source breakdown for a single package."""
    sources = pandas_data_source.index.get_level_values('data_source').unique()
    assert 'anaconda' in sources


def test_data_source_multiple_packages(multi_package_data_source):
    """Test data source breakdown for multiple packages."""
    packages = multi_package_data_source.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


def test_data_source_monthly(pandas_data_source_monthly):
    """Test data source breakdown with monthly aggregation."""
    assert pandas_data_source_monthly.index.nlevels == 3


def test_pkg_version_single_package(pandas_pkg_version):
    """Test version breakdown for a single package."""
    assert len(pandas_pkg_version) > 1
    versions = pandas_pkg_version.index.get_level_values('pkg_version').unique()
    assert len(versions) > 1


def test_pkg_version_multiple_packages(multi_package_pkg_version):
    """Test version breakdown for multiple packages."""
    packages = multi_package_pkg_version.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages


def test_pkg_python_single_package(pandas_pkg_python):
    """Test Python version breakdown for a single package."""
    assert len(pandas_pkg_python) > 1
    python_versions = pandas_pkg_python.index.get_level_values('pkg_python').unique()
    assert len(python_versions) > 1


def test_pkg_python_multiple_packages(multi_package_pkg_python):
    """Test Python version breakdown for multiple packages."""
    packages = multi_package_pkg_python.index.get_level_values('pkg_name').unique()
    assert 'pandas' in packages
    assert 'dask' in packages
