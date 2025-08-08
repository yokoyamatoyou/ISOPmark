"""Utilities package.

This module exposes submodules at package import time so that test suites and
other modules can reliably reference paths like ``utils.helpers``.  Without
this, :func:`pkgutil.resolve_name` used by :mod:`unittest.mock` would fail to
locate the ``helpers`` submodule because it isn't automatically added to the
package namespace.
"""

from . import helpers, logger

__all__ = ["helpers", "logger"]
