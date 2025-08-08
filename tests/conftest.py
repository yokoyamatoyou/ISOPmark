"""Test configuration file ensuring project root is importable.

Pytest automatically discovers this module.  We append the repository root to
``sys.path`` so that top-level packages such as ``document_processor`` and
``services`` can be imported without installing the project as a package.
"""

import os
import sys


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:  # pragma: no cover - environment setup
    sys.path.insert(0, ROOT_DIR)

