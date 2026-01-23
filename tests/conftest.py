"""Pytest fixtures for condastats tests."""
import pytest

from condastats.cli import (
    overall,
    pkg_platform,
    pkg_version,
    pkg_python,
    data_source,
)

from constants import TEST_MONTH, TEST_START_MONTH, TEST_END_MONTH


# Cache for session-scoped data to avoid repeated S3 calls
_cache = {}


def _get_cached(key, func, *args, **kwargs):
    """Get cached result or compute and cache it."""
    if key not in _cache:
        _cache[key] = func(*args, **kwargs)
    return _cache[key]


@pytest.fixture(scope="session")
def get_overall():
    """Factory fixture for overall() results."""
    def _get(package, **kwargs):
        key = f"overall:{package}:{kwargs}"
        return _get_cached(key, overall, package, **kwargs)
    return _get


@pytest.fixture(scope="session")
def get_groupby():
    """Factory fixture for groupby function results."""
    funcs = {
        'pkg_platform': pkg_platform,
        'data_source': data_source,
        'pkg_version': pkg_version,
        'pkg_python': pkg_python,
    }
    def _get(func_name, package, **kwargs):
        key = f"{func_name}:{package}:{kwargs}"
        return _get_cached(key, funcs[func_name], package, **kwargs)
    return _get
