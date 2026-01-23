"""Tests for the CLI interface."""
import subprocess
import sys

import pytest

from condastats.cli import main


# Subprocess tests (integration tests)
# These can't easily use fixtures since they run in separate processes

@pytest.mark.parametrize("subcommand,expected", [
    (["overall", "pandas", "--month", "2019-01"], "932443"),
    (["pkg_platform", "pandas", "--month", "2019-01"], "linux-64"),
    (["data_source", "pandas", "--month", "2019-01"], "anaconda"),
    (["pkg_version", "pandas", "--month", "2019-01"], "pandas"),
    (["pkg_python", "pandas", "--month", "2019-01"], "pandas"),
])
def test_cli_subcommands(subcommand, expected):
    """Test CLI subcommands via subprocess."""
    result = subprocess.run(
        [sys.executable, '-m', 'condastats.cli'] + subcommand,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert expected in result.stdout


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


# Direct main() tests using monkeypatch (for coverage)
# These reuse fixture data where the assertions allow

def test_main_overall(monkeypatch, capsys, pandas_overall):
    """Test main() with overall subcommand."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas', '--month', '2019-01'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out
    assert '932443' in captured.out


@pytest.mark.parametrize("subcommand,expected", [
    ('pkg_platform', 'linux-64'),
    ('data_source', 'anaconda'),
    ('pkg_version', 'pandas'),
    ('pkg_python', 'pandas'),
])
def test_main_groupby_subcommands(monkeypatch, capsys, subcommand, expected):
    """Test main() with groupby subcommands."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', subcommand, 'pandas', '--month', '2019-01'
    ])
    main()
    captured = capsys.readouterr()
    assert expected in captured.out


def test_main_overall_with_all_options(monkeypatch, capsys):
    """Test main() with all filter options."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas',
        '--month', '2019-01',
        '--pkg_platform', 'linux-32',
        '--data_source', 'anaconda',
        '--pkg_version', '0.10.0',
        '--pkg_python', '2.6'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_overall_complete(monkeypatch, capsys):
    """Test main() with complete flag."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas', '--month', '2019-01', '--complete'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


def test_main_overall_monthly(monkeypatch, capsys):
    """Test main() with monthly flag and date range."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', 'overall', 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out


@pytest.mark.parametrize("subcommand", [
    'pkg_platform', 'data_source', 'pkg_version', 'pkg_python'
])
def test_main_subcommands_monthly(monkeypatch, capsys, subcommand):
    """Test main() subcommands with monthly flag."""
    monkeypatch.setattr(sys, 'argv', [
        'condastats', subcommand, 'pandas',
        '--start_month', '2019-01',
        '--end_month', '2019-02',
        '--monthly'
    ])
    main()
    captured = capsys.readouterr()
    assert 'pandas' in captured.out
