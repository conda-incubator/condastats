"""Tests for the CLI interface."""
import subprocess
import sys
from unittest import mock

from condastats.cli import main


# Subprocess tests (integration tests)

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


# Direct main() tests (for coverage)

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
