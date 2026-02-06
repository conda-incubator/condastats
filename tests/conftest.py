"""Pytest fixtures for condastats tests."""

import hashlib
import pickle
from pathlib import Path

import pytest

from condastats import (
    data_source,
    overall,
    pkg_platform,
    pkg_python,
    pkg_version,
)

# Shared disk cache for S3 results across pytest sessions and pixi environments.
# The test data (2019-01, 2019-02) is immutable, so caching is safe.
# Delete tests/.s3_cache/ to force a fresh download.
_CACHE_DIR = Path(__file__).parent / ".s3_cache"
_CACHE_DIR.mkdir(exist_ok=True)


def _cache_key(prefix: str, args: tuple, kwargs: dict) -> str:
    """Create a stable cache key from function arguments."""
    raw = f"{prefix}:{args!r}:{sorted(kwargs.items())!r}"
    return hashlib.sha256(raw.encode()).hexdigest()


def _get_cached(prefix, func, *args, **kwargs):
    """Get result from disk cache, or compute, cache, and return it."""
    key = _cache_key(prefix, args, kwargs)
    cache_path = _CACHE_DIR / f"{key}.pkl"

    if cache_path.exists():
        with open(cache_path, "rb") as f:
            return pickle.load(f)  # noqa: S301

    result = func(*args, **kwargs)

    with open(cache_path, "wb") as f:
        pickle.dump(result, f)

    return result


@pytest.fixture(scope="session")
def get_overall():
    """Factory fixture for overall() results."""

    def _get(package, **kwargs):
        return _get_cached("overall", overall, package, **kwargs)

    return _get


@pytest.fixture(scope="session")
def get_groupby():
    """Factory fixture for groupby function results."""
    funcs = {
        "pkg_platform": pkg_platform,
        "data_source": data_source,
        "pkg_version": pkg_version,
        "pkg_python": pkg_python,
    }

    def _get(func_name, package, **kwargs):
        return _get_cached(func_name, funcs[func_name], package, **kwargs)

    return _get
