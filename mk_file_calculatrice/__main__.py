# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Command-line entry point for `python -m mk_file_calculatrice`."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Optional
from collections.abc import Sequence

from .bundler import generate
from .config import DEFAULT_LANG, LANGUAGE, MODULES
from .elements_packer import available_languages


def _parse_cli_lang(argv: Sequence[str]) -> Optional[str]:
    """Extract `--lang` / `-l` from command-line arguments, if provided.

    Args:
        argv: Command-line argument vector (excluding program name).

    Returns:
        The requested language code, or `None` if no flag was passed.

    Raises:
        SystemExit: If `--lang` or `-l` is given without a value.
    """
    for index, arg in enumerate(argv):
        if arg in ('--lang', '-l'):
            if index + 1 >= len(argv):
                raise SystemExit(f'error: {arg} requires a language code')
            return argv[index + 1]
        if arg.startswith('--lang='):
            return arg.split('=', 1)[1]
    return None


def _prompt_language() -> str:
    """Interactively prompt the user for the target language to embed.

    Falls back to `LANGUAGE` or `DEFAULT_LANG` when running in a
    non-interactive environment (e.g., CI pipelines).

    Returns:
        A validated language code available in `elements.py`.
    """
    languages = available_languages()
    if not languages:
        return LANGUAGE or DEFAULT_LANG

    default = DEFAULT_LANG if DEFAULT_LANG in languages else languages[0]
    if LANGUAGE in languages:
        default = LANGUAGE

    if not sys.stdin or not sys.stdin.isatty():
        return default

    choices = ', '.join(languages)
    while True:
        answer = input(
            f'Langues disponibles ({choices}) [{default}] : '
        ).strip()
        chosen = answer or default
        if chosen in languages:
            return chosen
        print(f'Langue invalide {chosen!r}. Choisissez parmi : {choices}.')


def main(argv: Optional[Sequence[str]] = None) -> None:
    """Build, verify, minify, and write `atomion.py` to disk.

    Args:
        argv: Optional argument list; defaults to `sys.argv[1:]`.
    """
    args = sys.argv[1:] if argv is None else argv
    lang = _parse_cli_lang(args)
    if lang is None:
        lang = _prompt_language()

    content = generate(lang=lang)
    output_path = Path('atomion.py')
    output_path.write_text(content, encoding='utf-8')

    print(
        f'{output_path}: {len(MODULES)} modules, '
        f'{output_path.stat().st_size} bytes'
    )


if __name__ == '__main__':
    main()
