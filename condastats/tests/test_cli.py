"""Tests for the CLI interface."""
import sys

import pytest

from condastats.cli import main


# Direct main() tests using monkeypatch (for coverage)

def test_main_overall(monkeypatch, capsys):
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
