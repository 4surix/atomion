# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""AST flattening, import filtering, and module discovery utilities."""

from __future__ import annotations

import ast
import importlib
import os
from pathlib import Path
import sys
from typing import Optional, Union
from collections.abc import Iterable, Sequence

from .config import BundleError, MODULES, PACKAGE, ROOT, TYPING_MODULES

ImportNode = Union[ast.Import, ast.ImportFrom]
FunctionNode = Union[ast.FunctionDef, ast.AsyncFunctionDef]


def list_modules() -> tuple[tuple[str, Path], ...]:
    """Return `(relative_posix_path, absolute_path)` in `MODULES` order.

    Raises:
        BundleError: If `MODULES` is out of sync with files on disk.
    """
    found: dict[str, Path] = {
        path.relative_to(PACKAGE).as_posix(): path
        for path in PACKAGE.rglob('*.py')
        if '__pycache__' not in path.parts
    }
    # Pure re-export package initializer; nothing to bundle.
    found.pop('utile/__init__.py', None)

    missing = [part for part in MODULES if part not in found]
    if missing:
        raise BundleError(
            'modules declared in `MODULES` but missing from package: '
            f"{', '.join(missing)}"
        )

    forgotten = sorted(set(found) - set(MODULES))
    if forgotten:
        raise BundleError(
            'package modules missing from `MODULES`: '
            f"{', '.join(forgotten)}"
        )

    return tuple((part, found[part]) for part in MODULES)


def read_ast(path: Path) -> ast.Module:
    """Parse a UTF-8 Python source file into an AST module."""
    return ast.parse(path.read_text(encoding='utf-8'), str(path))


def submodule_names() -> set[str]:
    """Return submodule and subpackage identifiers absent from the flat file.

    In package mode, `__all__` may export submodule names such as `objets` or
    `exception`. Because those modules do not exist as separate namespaces in
    the flattened file, they must be excluded from the final `__all__`.
    """
    names: set[str] = set()
    for part in MODULES:
        segments = part.split('/')
        names.update(segments[:-1])
        stem = Path(segments[-1]).stem
        if stem and stem != '__init__':
            names.add(stem)
    return names


def _is_docstring(node: ast.stmt) -> bool:
    """Return `True` if `node` is a standalone string literal expression."""
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _strip_docstring(body: list[ast.stmt]) -> None:
    """Remove a leading docstring from `body`, inserting `pass` if empty."""
    if body and _is_docstring(body[0]):
        del body[0]
    if not body:
        body.append(ast.Pass())


def _strip_annotations(args: ast.arguments) -> ast.arguments:
    """Remove parameter type annotations in place."""
    all_args = (
        args.posonlyargs
        + args.args
        + args.kwonlyargs
        + [args.vararg, args.kwarg]
    )
    for arg in all_args:
        if arg is not None:
            arg.annotation = None
    return args


class Flattener(ast.NodeTransformer):
    """Rewrite a module AST for inclusion in the standalone calculator file."""

    def __init__(self, aliases: set[str]) -> None:
        self.aliases = aliases

    def visit_Attribute(self, node: ast.Attribute) -> ast.expr:
        """Flatten `module_alias.symbol` references into `symbol`."""
        self.generic_visit(node)
        if (
            isinstance(node.value, ast.Name)
            and node.value.id in self.aliases
        ):
            return ast.copy_location(
                ast.Name(id=node.attr, ctx=node.ctx), node
            )
        return node

    def visit_FunctionDef(self, node: FunctionNode) -> FunctionNode:
        """Strip return annotations, parameter annotations, and docstrings."""
        self.generic_visit(node)
        node.returns = None
        node.args = _strip_annotations(node.args)
        _strip_docstring(node.body)
        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Strip class docstrings and ensure the class body remains valid."""
        self.generic_visit(node)
        _strip_docstring(node.body)
        return node

    @staticmethod
    def _override_calculator_flag(
        target: ast.expr,
        value: ast.expr,
    ) -> ast.expr:
        """Force `is_calculatrice = True` in the bundled output."""
        if isinstance(target, ast.Name) and target.id == 'is_calculatrice':
            return ast.copy_location(ast.Constant(value=True), value)
        return value

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        """Apply calculator flag overrides to simple assignments."""
        self.generic_visit(node)
        if len(node.targets) == 1:
            node.value = self._override_calculator_flag(
                node.targets[0], node.value
            )
        return node

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Optional[ast.Assign]:
        """Convert `x: T = val` into `x = val` and drop bare `x: T`."""
        self.generic_visit(node)
        if node.value is None:
            return None
        value = self._override_calculator_flag(node.target, node.value)
        return ast.copy_location(
            ast.Assign(targets=[node.target], value=value), node
        )


def _is_module(folder: Path, name: str) -> bool:
    """Return `True` if `folder/name` resolves to a Python module/package."""
    return (
        (folder / f'{name}.py').is_file()
        or (folder / name / '__init__.py').is_file()
    )


def _imported_dir(path: Path, node: ast.ImportFrom) -> Optional[Path]:
    """Resolve the package directory targeted by an `ImportFrom` node."""
    package_name = PACKAGE.name

    if node.level == 0:
        parts = (node.module or '').split('.')
        if parts[0] != package_name:
            return None
        folder = Path(PACKAGE, *parts[1:])
        return (
            folder
            if Path(os.path.commonpath([PACKAGE, folder])) == PACKAGE
            else None
        )

    folder = path.resolve().parent
    for _ in range(node.level - 1):
        folder = folder.parent
        if Path(os.path.commonpath([ROOT, folder])) != ROOT:
            return None

    if node.module:
        folder = Path(folder, *node.module.split('.'))

    return folder


def module_aliases(tree: ast.AST, path: Path) -> set[str]:
    """Collect local identifiers bound to submodules of `atomion`.

    For example, `from .. import objets` or `import atomion.affichage as aff`
    binds `objets` / `aff` to a submodule; attribute accesses on those names
    must be flattened in the single file.
    """
    aliases: set[str] = set()
    package_name = PACKAGE.name

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            folder = _imported_dir(path, node)
            if folder is None:
                continue
            aliases.update(
                alias.asname or alias.name
                for alias in node.names
                if alias.name != '*' and _is_module(folder, alias.name)
            )
        elif isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split('.')
                if parts[0] == package_name and len(parts) > 1:
                    aliases.add(alias.asname or parts[-1])

    return aliases


def _imports_package(node: ImportNode) -> bool:
    """Return `True` if `node` imports from `atomion` or via relative path."""
    package_name = PACKAGE.name
    if isinstance(node, ast.ImportFrom):
        return (
            node.level > 0
            or (node.module or '').split('.')[0] == package_name
        )
    return any(alias.name.split('.')[0] == package_name for alias in node.names)


def _imports_typing(node: ImportNode) -> bool:
    """Return `True` if `node` imports from `typing` or `__future__`."""
    if isinstance(node, ast.ImportFrom):
        return (node.module or '').split('.')[0] in TYPING_MODULES
    return any(
        alias.name.split('.')[0] in TYPING_MODULES for alias in node.names
    )


def _filter_stdlib_import(node: ImportNode) -> Optional[ImportNode]:
    """Keep only standard-library / third-party targets from an import."""
    if isinstance(node, ast.ImportFrom):
        if _imports_package(node) or _imports_typing(node):
            return None
        return node

    package_name = PACKAGE.name
    kept = [
        alias
        for alias in node.names
        if alias.name.split('.')[0] != package_name
        and alias.name.split('.')[0] not in TYPING_MODULES
    ]
    if not kept:
        return None
    return ast.copy_location(ast.Import(names=kept), node)


def _is_type_checking_guard(node: ast.stmt) -> bool:
    """Return `True` for `if TYPE_CHECKING:` or `if typing.TYPE_CHECKING:`."""
    if not isinstance(node, ast.If):
        return False
    test = node.test
    if isinstance(test, ast.Name) and test.id == 'TYPE_CHECKING':
        return True
    return (
        isinstance(test, ast.Attribute)
        and isinstance(test.value, ast.Name)
        and test.value.id == 'typing'
        and test.attr == 'TYPE_CHECKING'
    )


def _is_dunder_all(node: ast.stmt) -> bool:
    """Return `True` if a top-level statement defines or mutates `__all__`."""
    if isinstance(node, ast.Assign):
        return any(
            isinstance(t, ast.Name) and t.id == '__all__'
            for t in node.targets
        )
    if isinstance(node, (ast.AnnAssign, ast.AugAssign)):
        return isinstance(node.target, ast.Name) and node.target.id == '__all__'
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and isinstance(node.value.func.value, ast.Name)
        and node.value.func.value.id == '__all__'
    )


def extract_all(path: Path) -> list[str]:
    """Import a package module and return its declared `__all__` symbols."""
    rel_path = path.resolve().relative_to(ROOT)
    module_name = rel_path.with_suffix('').as_posix().replace('/', '.')
    if module_name.endswith('.__init__'):
        module_name = module_name[: -len('.__init__')]

    root_str = str(ROOT)
    added = root_str not in sys.path
    if added:
        sys.path.insert(0, root_str)
    try:
        module = importlib.import_module(module_name)
    except Exception as error:
        raise BundleError(
            f'{path}: unable to import module ({error})'
        ) from error
    finally:
        if added and root_str in sys.path:
            sys.path.remove(root_str)

    raw_all = getattr(module, '__all__', None)
    if raw_all is None:
        return []
    if not isinstance(raw_all, (list, tuple)) or not all(
        isinstance(item, str) for item in raw_all
    ):
        raise BundleError(
            f'{path}: `__all__` must be a list or tuple of strings'
        )
    return list(raw_all)


def discover_public_globals() -> list[str]:
    """Collect all public API names across `MODULES` (excluding submodules)."""
    if not PACKAGE.is_dir():
        return []

    try:
        seen: set[str] = set()
        public_globals: list[str] = []
        for _, path in list_modules():
            for name in extract_all(path):
                if name not in seen:
                    seen.add(name)
                    public_globals.append(name)

        excluded = submodule_names()
        return [name for name in public_globals if name not in excluded]
    except BundleError:
        return []


class _BodyImportStripper(ast.NodeTransformer):
    """Strip intra-package and typing imports nested inside blocks."""

    def generic_visit(self, node: ast.AST) -> ast.AST:
        super().generic_visit(node)
        stmts = getattr(node, 'body', None)
        if isinstance(stmts, list) and not stmts:
            stmts.append(ast.Pass())
        return node

    def visit_Import(self, node: ast.Import) -> Optional[ImportNode]:
        return _filter_stdlib_import(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Optional[ImportNode]:
        return _filter_stdlib_import(node)


def module_body(
    tree: ast.Module,
    name: str = 'atomion.py',
) -> tuple[list[ast.stmt], list[ImportNode]]:
    """Split a module into `(retained_statements, hoisted_stdlib_imports)`."""
    body: list[ast.stmt] = []
    imports: list[ImportNode] = []

    for node in tree.body:
        if _is_type_checking_guard(node):
            assert isinstance(node, ast.If)
            body.extend(node.orelse)
            continue

        if _is_dunder_all(node):
            continue

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            filtered = _filter_stdlib_import(node)
            if filtered is not None:
                imports.append(filtered)
            continue

        if not _is_docstring(node):
            cleaned = _BodyImportStripper().visit(node)
            if cleaned is not None:
                body.append(cleaned)

    return body, imports


def _targets(node: ast.stmt) -> list[str]:
    """Return variable names bound by a top-level statement."""
    if isinstance(node, ast.Assign):
        targets: list[ast.expr] = list(node.targets)
    elif isinstance(node, (ast.AnnAssign, ast.For, ast.AsyncFor)):
        targets = [node.target]
    elif isinstance(node, (ast.With, ast.AsyncWith)):
        targets = [
            item.optional_vars
            for item in node.items
            if item.optional_vars is not None
        ]
    else:
        targets = []

    return [
        child.id
        for target in targets
        for child in ast.walk(target)
        if isinstance(child, ast.Name)
    ]


def _is_object(node: ast.stmt) -> bool:
    """Return `True` for function or class definitions."""
    return isinstance(
        node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    )


def _bound_names(body: Sequence[ast.stmt]) -> dict[str, ast.stmt]:
    """Map top-level bound identifiers to their defining AST statement."""
    names: dict[str, ast.stmt] = {}
    for node in body:
        if _is_object(node):
            assert isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            )
            names[node.name] = node
            continue
        for name in _targets(node):
            names[name] = node
    return names


def check_collisions(chunks: Sequence[tuple[str, list[ast.stmt]]]) -> None:
    """Ensure no two modules define a function or class with the same name."""
    seen: dict[str, str] = {}
    for part, body in chunks:
        for name, node in _bound_names(body).items():
            if not _is_object(node):
                continue
            if name in seen:
                raise BundleError(
                    f'modules `{seen[name]}` and `{part}` both define `{name}`'
                )
            seen[name] = part


def deduplicate_imports(imports: Iterable[ImportNode]) -> list[ImportNode]:
    """Deduplicate hoisted external imports while preserving order."""
    forms: dict[str, ImportNode] = {}
    for node in imports:
        forms.setdefault(ast.unparse(node), node)
    return list(forms.values())
