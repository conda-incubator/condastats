import subprocess
import sys
from unittest import mock

import pytest

from condastats.cli import overall, pkg_platform, pkg_version, pkg_python, data_source, main


# Tests for overall()

def test_overall_single_package_single_month():
    """Test overall counts for a single package in a single month."""
    result = overall('pandas', month='2019-01')
    assert result.loc['pandas'] == 932443


def test_overall_multiple_packages_single_month():
    """Test overall counts for multiple packages in a single month."""
    result = overall(['pandas', 'dask'], month='2019-01')
    assert result.loc['pandas'] == 932443
    assert result.loc['dask'] == 221200


def test_overall_with_all_filters():
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


def test_overall_with_platform_filter():
    """Test overall counts filtered by platform."""
    result = overall('pandas', month='2019-01', pkg_platform='linux-64')
    assert result.loc['pandas'] > 0


def test_overall_with_data_source_filter():
    """Test overall counts filtered by data source."""
    result = overall('pandas', month='2019-01', data_source='anaconda')
    assert result.loc['pandas'] > 0


def test_overall_date_range():
    """Test overall counts for a date range."""
    result = overall('pandas', start_month='2019-01', end_month='2019-02')
    single_month = overall('pandas', month='2019-01')
    assert result.loc['pandas'] > single_month.loc['pandas']


def test_overall_monthly_aggregation():
    """Test monthly aggregation returns multiple time periods."""
    result = overall('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 2
    assert len(result) >= 2


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


# Tests for complete parameter

def test_overall_complete():
    """Test overall with complete=True returns full DataFrame."""
    result = overall('pandas', month='2019-01', complete=True)
    # Should return a DataFrame, not a Series
    assert hasattr(result, 'columns')
    assert 'pkg_name' in result.columns


# Tests for monthly aggregation in groupby functions

def test_pkg_platform_monthly():
    """Test platform breakdown with monthly aggregation."""
    result = pkg_platform('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 3  # pkg_name, time, pkg_platform


def test_data_source_monthly():
    """Test data source breakdown with monthly aggregation."""
    result = data_source('pandas', start_month='2019-01', end_month='2019-02', monthly=True)
    assert result.index.nlevels == 3


# Tests for CLI

def test_cli_overall():
    """Test CLI overall subcommand."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'overall', 'pandas', '--month', '2019-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'pandas' in result.stdout
    assert '932443' in result.stdout


def test_cli_pkg_platform():
    """Test CLI pkg_platform subcommand."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'pkg_platform', 'pandas', '--month', '2019-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'linux-64' in result.stdout


def test_cli_data_source():
    """Test CLI data_source subcommand."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'data_source', 'pandas', '--month', '2019-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'anaconda' in result.stdout


def test_cli_pkg_version():
    """Test CLI pkg_version subcommand."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'pkg_version', 'pandas', '--month', '2019-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'pandas' in result.stdout


def test_cli_pkg_python():
    """Test CLI pkg_python subcommand."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'pkg_python', 'pandas', '--month', '2019-01'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'pandas' in result.stdout


def test_cli_overall_with_filters():
    """Test CLI overall with filter options."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'overall', 'pandas',
         '--month', '2019-01',
         '--pkg_platform', 'linux-64',
         '--data_source', 'anaconda'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'pandas' in result.stdout


def test_cli_overall_monthly():
    """Test CLI overall with monthly flag."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli', 'overall', 'pandas',
         '--start_month', '2019-01',
         '--end_month', '2019-02',
         '--monthly'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'pandas' in result.stdout


# Tests for main() function directly (for coverage)

def test_main_overall(capsys):
    """Test main() with overall subcommand."""
    with mock.patch('sys.argv', ['condastats', 'overall', 'pandas', '--month', '2019-01']):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out
    assert '932443' in captured.out


def test_main_pkg_platform(capsys):
    """Test main() with pkg_platform subcommand."""
    with mock.patch('sys.argv', ['condastats', 'pkg_platform', 'pandas', '--month', '2019-01']):
        main()
    captured = capsys.readouterr()
    assert 'linux-64' in captured.out


def test_main_data_source(capsys):
    """Test main() with data_source subcommand."""
    with mock.patch('sys.argv', ['condastats', 'data_source', 'pandas', '--month', '2019-01']):
        main()
    captured = capsys.readouterr()
    assert 'anaconda' in captured.out


def test_main_pkg_version(capsys):
    """Test main() with pkg_version subcommand."""
    with mock.patch('sys.argv', ['condastats', 'pkg_version', 'pandas', '--month', '2019-01']):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_pkg_python(capsys):
    """Test main() with pkg_python subcommand."""
    with mock.patch('sys.argv', ['condastats', 'pkg_python', 'pandas', '--month', '2019-01']):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_overall_with_all_options(capsys):
    """Test main() with all filter options."""
    with mock.patch('sys.argv', [
        'condastats', 'overall', 'pandas',
        '--month', '2019-01',
        '--pkg_platform', 'linux-32',
        '--data_source', 'anaconda',
        '--pkg_version', '0.10.0',
        '--pkg_python', '2.6'
    ]):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_overall_complete(capsys):
    """Test main() with complete flag."""
    with mock.patch('sys.argv', ['condastats', 'overall', 'pandas', '--month', '2019-01', '--complete']):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_overall_monthly(capsys):
    """Test main() with monthly flag and date range."""
    with mock.patch('sys.argv', [
        'condastats', 'overall', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ]):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_pkg_platform_monthly(capsys):
    """Test main() pkg_platform with monthly flag."""
    with mock.patch('sys.argv', [
        'condastats', 'pkg_platform', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ]):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_data_source_monthly(capsys):
    """Test main() data_source with monthly flag."""
    with mock.patch('sys.argv', [
        'condastats', 'data_source', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ]):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_pkg_version_monthly(capsys):
    """Test main() pkg_version with monthly flag."""
    with mock.patch('sys.argv', [
        'condastats', 'pkg_version', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ]):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_pkg_python_monthly(capsys):
    """Test main() pkg_python with monthly flag."""
    with mock.patch('sys.argv', [
        'condastats', 'pkg_python', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ]):
        main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out
