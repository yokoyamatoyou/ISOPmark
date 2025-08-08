"""Minimal stub of the :mod:`streamlit` package for testing purposes.

Only the small subset of functions used in the tests are implemented.  The
functions simply accept any arguments and return ``None``.
"""

from typing import Any


def title(*args: Any, **kwargs: Any) -> None:  # pragma: no cover - trivial
    """Stub for :func:`streamlit.title`."""


def write(*args: Any, **kwargs: Any) -> None:  # pragma: no cover - trivial
    """Stub for :func:`streamlit.write`."""

