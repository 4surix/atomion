# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Bundle orchestration, post-build verification, and minification."""

from __future__ import annotations

import ast
from typing import Any, Optional
from collections.abc import Sequence

try:
    import python_minifier
except ImportError:
    raise SystemExit(
        'python_minifier is required to generate the single file:\n'
        '    python -m pip install "atomion[calc]"'
    ) from None

from .config import (
    BundleError,
    DEFAULT_LANG,
    HEADER_TEXT,
    INTERNAL_PRESERVED_GLOBALS,
    LANGUAGE,
    MINIFICATION_OPTIONS,
)
from .elements_packer import LazyElementsTransformer
from .flattener import (
    Flattener,
    ImportNode,
    check_collisions,
    deduplicate_imports,
    discover_public_globals,
    extract_all,
    list_modules,
    module_aliases,
    module_body,
    read_ast,
    submodule_names,
)
from .portability import check_portability

# Per-language in-memory cache to avoid redundant minification passes.
_CACHE: dict[str, str] = {}


def _verify_no_annotations(tree: ast.AST) -> None:
    """Ensure no type annotations survived AST flattening."""
    for node in ast.walk(tree):
        remaining = (
            isinstance(node, (ast.AnnAssign, ast.arg))
            and node.annotation is not None
        ) or (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.returns is not None
        )
        if remaining:
            raise BundleError(
                'remaining annotation in single file '
                f'(line {getattr(node, "lineno", "?")})'
            )


def _verify(
    text: str,
    public_globals: Optional[Sequence[str]] = None,
) -> None:
    """Validate syntax, MicroPython portability, and runtime execution."""
    try:
        tree = ast.parse(text, 'atomion.py')
    except SyntaxError as error:
        raise BundleError(
            f'generated single file is invalid: {error}'
        ) from error

    check_portability(tree)
    _verify_no_annotations(tree)

    namespace: dict[str, Any] = {}
    try:
        exec(compile(tree, 'atomion.py', 'exec'), namespace)
    except Exception as error:
        raise BundleError(
            'generated single file fails to execute '
            f'(fix order in `MODULES`?): {type(error).__name__}: {error}'
        ) from error

    if public_globals:
        missing = [name for name in public_globals if name not in namespace]
        if missing:
            raise BundleError(
                'symbols listed in `__all__` but undefined after execution: '
                f"{', '.join(missing)}"
            )


def _build_bundle(lang: Optional[str] = None) -> tuple[str, list[str]]:
    """Compose all package modules into an unminified single-file string."""
    chunks: list[tuple[str, list[ast.stmt]]] = []
    imports: list[ImportNode] = []
    seen_exports: set[str] = set()
    public_globals: list[str] = []

    for part, path in list_modules():
        tree = read_ast(path)
        check_portability(tree, str(path))

        for name in extract_all(path):
            if name not in seen_exports:
                seen_exports.add(name)
                public_globals.append(name)

        aliases = module_aliases(tree, path)
        body, header = module_body(tree)
        imports.extend(header)

        mod_ast = ast.Module(body=body, type_ignores=[])
        if part == 'elements.py':
            transformer = LazyElementsTransformer(lang=lang)
            mod_ast = transformer.visit(mod_ast)
            if not transformer.replaced:
                raise BundleError(
                    'elements.py: `elements` assignment not found'
                )

        flattened_body = Flattener(aliases).visit(mod_ast).body
        chunks.append((part, flattened_body))

    excluded_submodules = submodule_names()
    public_globals = [
        name for name in public_globals if name not in excluded_submodules
    ]

    check_collisions(chunks)

    statements: list[ast.stmt] = list(deduplicate_imports(imports))
    for _, body in chunks:
        statements.extend(body)

    if public_globals:
        statements.append(
            ast.Assign(
                targets=[ast.Name(id='__all__', ctx=ast.Store())],
                value=ast.List(
                    elts=[ast.Constant(value=name) for name in public_globals],
                    ctx=ast.Load(),
                ),
            )
        )

    unparsed = ast.unparse(
        ast.fix_missing_locations(
            ast.Module(body=statements, type_ignores=[])
        )
    ).strip()
    text = f'{HEADER_TEXT}\n{unparsed}\n'

    _verify(text, public_globals)
    return text, public_globals


def build(lang: Optional[str] = None) -> str:
    """Return the unminified single-file source for MicroPython 1.9.4."""
    text, _ = _build_bundle(lang=lang)
    return text


def _minify(
    text: str,
    preserve_globals: Optional[Sequence[str]] = None,
) -> str:
    """Minify `text` while preserving public API and required globals."""
    options = dict(MINIFICATION_OPTIONS)
    base_globals = (
        discover_public_globals()
        if preserve_globals is None
        else preserve_globals
    )
    options['preserve_globals'] = list(
        dict.fromkeys([*base_globals, *INTERNAL_PRESERVED_GLOBALS])
    )
    return python_minifier.minify(text, **options)


def generate(force: bool = False, lang: Optional[str] = None) -> str:
    """Return the verified and minified `atomion.py` source code.

    Results are cached per language because minifying a ~95 KB module is
    computationally expensive. Pass `force=True` to bypass the cache.
    """
    cache_key = lang or LANGUAGE or DEFAULT_LANG

    if force or cache_key not in _CACHE:
        unminified, public_globals = _build_bundle(lang=cache_key)
        text = _minify(unminified, preserve_globals=public_globals)

        # Re-verify after minification to catch minifier-induced regressions.
        _verify(text, public_globals)
        _CACHE[cache_key] = text

    return _CACHE[cache_key]
