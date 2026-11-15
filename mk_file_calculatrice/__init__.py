# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Generates `atomion.py`, the single-file version for calculators.

This package recomposes the multi-module `atomion` library into a standalone,
minified `atomion.py` script compatible with MicroPython 1.9.4 (commonly
shipped on graphing calculators).

Key transformations performed during bundling:
    - Relative and intra-package imports are stripped, and module-qualified
      references are flattened (e.g., `objets.Atome` -> `Atome`).
    - Type annotations and docstrings are removed to minimize flash/RAM usage
      and satisfy MicroPython 1.9.4 syntax constraints.
    - The periodic table (`elements`) is serialized into a compact,
      single-language delimited string decoded lazily on demand.
    - `is_calculatrice` is forced to `True` in the generated output.

The composition order is declared in `MODULES`; it is not inferred from the
import graph, which contains cycles (`utile` <-> `objets`, resolved at call
time via `objets.X`), but verified by executing the resulting file.

The output is then minified: `python_minifier` is required for this
(`pip install "atomion[calc]"`). The delivered file is thus ~35% lighter,
and it is the one verified, both locally and in CI.

Usage:
    python -m mk_file_calculatrice [--lang fr]
    python mk_file_calculatrice [--lang en]
"""

from __future__ import annotations

from .__main__ import main
from .bundler import build, generate, _verify_no_annotations
from .config import BundleError, DEFAULT_LANG, LANGUAGE, MODULES, PACKAGE
from .elements_packer import available_languages
from .flattener import (
    Flattener,
    check_collisions,
    module_aliases,
    module_body,
    list_modules,
)
from .portability import check_portability

__all__ = [
    'DEFAULT_LANG',
    'LANGUAGE',
    'MODULES',
    'BundleError',
    'available_languages',
    'build',
    'check_portability',
    'generate',
    'list_modules',
    'main',
]
