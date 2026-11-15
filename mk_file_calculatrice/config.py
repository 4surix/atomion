# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Configuration constants, module ordering, and domain exceptions."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

# Repository root and source package directory.
ROOT: Path = Path(__file__).resolve().parent.parent
PACKAGE: Path = ROOT / 'atomion'

# Default localization settings for calculator builds.
DEFAULT_LANG: str = 'fr'
LANGUAGE: Optional[str] = None

HEADER_TEXT: str = """
# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------
"""

# Explicit topological composition order:
# In a single flattened module, every symbol must be defined before it is
# referenced at module-import time. Every package module must appear here.
MODULES: tuple[str, ...] = (
    '__init__.py',
    'elements.py',
    'exception.py',
    'irregularites.py',
    'affichage.py',
    'objets/__init__.py',
    'utile/utile.py',
    'objets/atome.py',
    'objets/electron.py',
    'objets/ion.py',
    'objets/molecule.py',
    'objets/neutron.py',
    'objets/proton.py',
    'objets/liaison.py',
    'objets/noyau.py',
    'utile/equation.py',
    'objets/quark.py',
    'raccourcis.py',
    'couples.py',
    'utile/oxydo_reduction.py',
    'utile/acido_basique.py',
)

# Modules used solely for static type checking; imports from these modules
# are stripped because MicroPython 1.9.4 provides neither `typing` nor
# `from __future__ import annotations`.
TYPING_MODULES: tuple[str, ...] = ('typing', '__future__')

# Internal helpers that are not part of `__all__` but must retain their
# identifier names after global minification.
INTERNAL_PRESERVED_GLOBALS: tuple[str, ...] = ('get_info',)

# Keyword options forwarded to `python_minifier.minify`.
MINIFICATION_OPTIONS: dict[str, Any] = {
    'filename': None,
    'remove_annotations': True,
    'remove_pass': True,
    'remove_literal_statements': True,
    'combine_imports': True,
    'hoist_literals': False,
    'rename_locals': True,
    'preserve_locals': None,
    'rename_globals': True,
    'preserve_globals': None,
    'remove_object_base': True,
    'convert_posargs_to_args': True,
}


class BundleError(ValueError):
    """Raised when the single-file bundle cannot be validly produced."""
