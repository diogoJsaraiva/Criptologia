"""Test package configuration.

Adds the project root to ``sys.path`` so tests can import the ``core``
modules when ``pytest`` is executed from different working directories.
"""

from __future__ import annotations

import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)