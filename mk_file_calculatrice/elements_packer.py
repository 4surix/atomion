# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Compact single-language packing for `elements.py`."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any, Optional, Union
from collections.abc import Sequence

from .config import BundleError, DEFAULT_LANG, LANGUAGE, PACKAGE
from .flattener import read_ast

_LAZY_RUNTIME_PATH: Path = Path(__file__).with_name('lazy_runtime.py')
_LAZY_ELEMENTS_RUNTIME: str = _LAZY_RUNTIME_PATH.read_text(encoding='utf-8')


def _escape_field(text: str) -> str:
    """Escape delimiters used in the packed `elements` string."""
    return (
        text.replace('\\', '\\\\')
        .replace('|', '\\p')
        .replace('\n', '\\n')
        .replace(',', '\\c')
    )


def _encode_scalar(value: Any) -> str:
    """Encode a scalar literal value into a compact tagged token."""
    if value is None:
        return 'n'
    if isinstance(value, bool):
        return 'b1' if value else 'b0'
    if isinstance(value, int):
        return f'i{value}'
    if isinstance(value, float):
        return f'f{value!r}'
    if isinstance(value, str):
        return f's{_escape_field(value)}'
    raise BundleError(
        f'unsupported value type in `elements`: {type(value).__name__}'
    )


def _encode_field(value: Any) -> str:
    """Encode a scalar, tuple, or list field value."""
    if isinstance(value, tuple):
        if not value:
            return 't'
        return 't' + ','.join(_encode_scalar(item) for item in value)
    if isinstance(value, list):
        if not value:
            return 'l'
        return 'l' + ','.join(_encode_scalar(item) for item in value)
    return _encode_scalar(value)


def _eval_literal_ast(node: ast.expr) -> Any:
    """Safely evaluate a literal AST node without `eval`."""
    try:
        return ast.literal_eval(node)
    except ValueError as error:
        raise BundleError(
            f'elements.py:{getattr(node, "lineno", 0)}: '
            'non-literal expression in `elements`'
        ) from error


def _parse_elements_records(
    seq_node: ast.expr,
) -> tuple[tuple[str, ...], list[dict[str, Any]], tuple[str, ...]]:
    """Parse `elements` AST into `(ordered_keys, records, languages)`."""
    if not isinstance(seq_node, (ast.List, ast.Tuple)):
        raise BundleError(
            'elements.py: `elements` must be a list or tuple of dicts'
        )

    keys: list[str] = []
    seen_keys: set[str] = set()
    languages: list[str] = []
    seen_langs: set[str] = set()
    records: list[dict[str, Any]] = []

    for item in seq_node.elts:
        if not isinstance(item, ast.Dict):
            raise BundleError(
                f'elements.py:{getattr(item, "lineno", 0)}: '
                'each item in `elements` must be a dict'
            )
        record = _eval_literal_ast(item)
        for key, value in record.items():
            if not isinstance(key, str):
                raise BundleError(
                    f'elements.py:{getattr(item, "lineno", 0)}: '
                    'dict keys in `elements` must be strings'
                )
            if key not in seen_keys:
                seen_keys.add(key)
                keys.append(key)
            if isinstance(value, dict):
                for lang_key in value:
                    if lang_key not in seen_langs:
                        seen_langs.add(lang_key)
                        languages.append(lang_key)
        records.append(record)

    return tuple(keys), records, tuple(languages)


def _resolve_lang(
    lang: Optional[str],
    languages: Sequence[str],
) -> str:
    """Resolve and validate the target language against available locales."""
    chosen = lang or LANGUAGE
    if chosen is None:
        if not languages or DEFAULT_LANG in languages:
            return DEFAULT_LANG
        return languages[0]
    if languages and chosen not in languages:
        raise BundleError(
            f"unknown language {chosen} (available: {', '.join(languages)})"
        )
    return chosen


def _select_record_value(
    record: dict[str, Any],
    key: str,
    lang: str,
) -> Any:
    """Extract a field value for `lang`, unwrapping localized dicts."""
    value = record[key]
    if isinstance(value, dict):
        if lang not in value:
            raise BundleError(
                f'elements.py: missing translation {lang} for key {key}'
            )
        return value[lang]
    return value


def _pack_elements_records(
    seq_node: ast.expr,
    lang: Optional[str] = None,
) -> tuple[tuple[str, ...], str, int]:
    """Pack `elements` records for `lang` into `(keys, packed_str, count)`."""
    keys, records, languages = _parse_elements_records(seq_node)
    chosen_lang = _resolve_lang(lang, languages)

    lines: list[str] = []
    for record in records:
        row = [
            _encode_field(_select_record_value(record, key, chosen_lang))
            if key in record
            else 'u'
            for key in keys
        ]
        lines.append('|'.join(row))

    return keys, '\n'.join(lines), len(records)


def _elements_value_node(node: ast.stmt) -> Optional[ast.expr]:
    """Return the RHS expression if `node` assigns `elements`, else `None`."""
    if (
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == 'elements'
    ):
        return node.value
    if (
        isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == 'elements'
    ):
        return node.value
    return None


def available_languages() -> tuple[str, ...]:
    """Return language codes discovered in `atomion/elements.py`."""
    elements_path = PACKAGE / 'elements.py'
    if not elements_path.is_file():
        return ()

    tree = read_ast(elements_path)
    for node in tree.body:
        value = _elements_value_node(node)
        if value is not None:
            _, _, languages = _parse_elements_records(value)
            return languages
    return ()


class LazyElementsTransformer(ast.NodeTransformer):
    """Replace `elements = [...]` with a packed `_LazyElements` instance."""

    def __init__(self, lang: Optional[str] = None) -> None:
        self.lang = lang
        self.replaced: bool = False

    def _rewrite_value(self, value_node: ast.expr) -> list[ast.stmt]:
        keys, packed, count = _pack_elements_records(value_node, self.lang)
        runtime_nodes = ast.parse(_LAZY_ELEMENTS_RUNTIME).body

        keys_assign = ast.Assign(
            targets=[ast.Name(id='_ELEMENT_KEYS', ctx=ast.Store())],
            value=ast.Tuple(
                elts=[ast.Constant(value=k) for k in keys],
                ctx=ast.Load(),
            ),
        )
        data_assign = ast.Assign(
            targets=[ast.Name(id='_ELEMENTS_DATA', ctx=ast.Store())],
            value=ast.Constant(value=packed),
        )
        elements_assign = ast.Assign(
            targets=[ast.Name(id='elements', ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id='_LazyElements', ctx=ast.Load()),
                args=[
                    ast.Name(id='_ELEMENTS_DATA', ctx=ast.Load()),
                    ast.Constant(value=count),
                ],
                keywords=[],
            ),
        )

        self.replaced = True
        nodes: list[ast.stmt] = [
            *runtime_nodes,
            keys_assign,
            data_assign,
            elements_assign,
        ]
        for node in nodes:
            ast.copy_location(node, value_node)
        return nodes

    def visit_Assign(
        self,
        node: Union[ast.Assign, ast.AnnAssign],
    ) -> Union[ast.stmt, list[ast.stmt]]:
        """Intercept `elements` assignment and inject the lazy runtime."""
        value = _elements_value_node(node)
        if value is not None:
            return self._rewrite_value(value)
        return node

    visit_AnnAssign = visit_Assign
