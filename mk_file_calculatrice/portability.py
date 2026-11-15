# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Static AST checks ensuring compatibility with MicroPython 1.9.4."""

from __future__ import annotations

import ast
from typing import Optional

from .config import BundleError

# Built-in exceptions supported by MicroPython 1.9.4.
MICROPYTHON_194_EXCEPTIONS: frozenset[str] = frozenset({
    'BaseException',
    'Exception',
    'ArithmeticError',
    'AssertionError',
    'AttributeError',
    'EOFError',
    'FloatingPointError',
    'GeneratorExit',
    'ImportError',
    'IndentationError',
    'IndexError',
    'KeyError',
    'KeyboardInterrupt',
    'LookupError',
    'MemoryError',
    'NameError',
    'NotImplementedError',
    'OSError',
    'OverflowError',
    'RuntimeError',
    'StopIteration',
    'SyntaxError',
    'SystemError',
    'SystemExit',
    'TypeError',
    'UnicodeError',
    'ValueError',
    'ZeroDivisionError',
})

# Modern or CPython-only exceptions absent from MicroPython 1.9.4.
UNSUPPORTED_EXCEPTIONS: frozenset[str] = frozenset({
    'BaseExceptionGroup',
    'BlockingIOError',
    'BrokenPipeError',
    'BufferError',
    'BytesWarning',
    'ChildProcessError',
    'ConnectionAbortedError',
    'ConnectionError',
    'ConnectionRefusedError',
    'ConnectionResetError',
    'DeprecationWarning',
    'EncodingWarning',
    'EnvironmentError',
    'ExceptionGroup',
    'FileExistsError',
    'FileNotFoundError',
    'FutureWarning',
    'IOError',
    'ImportWarning',
    'InterruptedError',
    'IsADirectoryError',
    'ModuleNotFoundError',
    'NotADirectoryError',
    'PendingDeprecationWarning',
    'PermissionError',
    'ProcessLookupError',
    'RecursionError',
    'ReferenceError',
    'ResourceWarning',
    'RuntimeWarning',
    'StopAsyncIteration',
    'SyntaxWarning',
    'TabError',
    'TimeoutError',
    'UnboundLocalError',
    'UnicodeDecodeError',
    'UnicodeEncodeError',
    'UnicodeTranslateError',
    'UnicodeWarning',
    'UserWarning',
    'Warning',
    'WindowsError',
})


def _base_name(node: ast.expr) -> Optional[str]:
    """Extract the identifier name from a base-class or exception expression."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _inherits_from_exception(
    class_name: str,
    classes: dict[str, ast.ClassDef],
    visiting: Optional[set[str]] = None,
) -> bool:
    """Return `True` if `class_name` transitively inherits from `Exception`."""
    if class_name in (
        'BaseException',
        'GeneratorExit',
        'KeyboardInterrupt',
        'SystemExit',
    ):
        return False

    if class_name in MICROPYTHON_194_EXCEPTIONS:
        return True

    if class_name not in classes:
        return False

    if visiting is None:
        visiting = set()

    if class_name in visiting:
        return False

    visiting.add(class_name)

    for base in classes[class_name].bases:
        base_id = _base_name(base)
        if base_id and _inherits_from_exception(base_id, classes, visiting):
            return True

    return False


def _has_unknown_external_base(
    class_node: ast.ClassDef,
    classes: dict[str, ast.ClassDef],
) -> bool:
    """Return `True` if `class_node` inherits from an external symbol."""
    for base in class_node.bases:
        base_id = _base_name(base)
        if (
            base_id is not None
            and base_id not in classes
            and base_id not in MICROPYTHON_194_EXCEPTIONS
            and base_id not in UNSUPPORTED_EXCEPTIONS
            and base_id != 'object'
        ):
            return True
    return False


def _check_exceptions(
    tree: ast.AST,
    issues: list[tuple[int, str]],
) -> None:
    """Validate exception usage and inheritance rules for MicroPython 1.9.4."""
    classes: dict[str, ast.ClassDef] = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }
    exception_candidates: set[str] = set()

    for node in ast.walk(tree):
        # Reject CPython-specific or post-3.5 built-in exceptions.
        if (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id in UNSUPPORTED_EXCEPTIONS
        ):
            issues.append((
                node.lineno,
                f'exception `{node.id}` is not supported in MicroPython 1.9.4',
            ))

        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == 'builtins'
            and node.attr in UNSUPPORTED_EXCEPTIONS
        ):
            issues.append((
                node.lineno,
                f'exception `builtins.{node.attr}` is not supported in '
                'MicroPython 1.9.4',
            ))

        # Reject bare `except:` and `except BaseException:` clauses.
        elif isinstance(node, ast.ExceptHandler):
            if node.type is None:
                issues.append((
                    node.lineno,
                    'bare `except:` is too broad for MicroPython 1.9.4 '
                    '(use `except Exception:`)',
                ))
            else:
                handlers = (
                    node.type.elts
                    if isinstance(node.type, ast.Tuple)
                    else [node.type]
                )
                for handler in handlers:
                    handler_id = _base_name(handler)
                    if handler_id == 'BaseException':
                        issues.append((
                            node.lineno,
                            '`except BaseException:` is too broad '
                            '(use `except Exception:`)',
                        ))
                    elif handler_id in classes:
                        exception_candidates.add(handler_id)

        elif isinstance(node, ast.Raise) and node.exc is not None:
            raised = (
                node.exc.func
                if isinstance(node.exc, ast.Call)
                else node.exc
            )
            raised_id = _base_name(raised)
            if raised_id in classes:
                exception_candidates.add(raised_id)

        elif isinstance(node, ast.ClassDef):
            if node.name.endswith(('Error', 'Exception')):
                exception_candidates.add(node.name)

            for base in node.bases:
                if _base_name(base) == 'BaseException':
                    issues.append((
                        node.lineno,
                        f'exception `{node.name}` must inherit from '
                        '`Exception`, not `BaseException`',
                    ))

    # Ensure every custom exception class derives from `Exception`.
    for class_name in sorted(exception_candidates):
        class_node = classes[class_name]
        if _inherits_from_exception(class_name, classes):
            continue
        if not _has_unknown_external_base(class_node, classes):
            issues.append((
                class_node.lineno,
                f'exception `{class_name}` must inherit from `Exception`',
            ))


def check_portability(tree: ast.AST, name: str = 'atomion.py') -> None:
    """Reject Python syntax constructs unsupported by MicroPython 1.9.4.

    CPython accepts these constructs silently; catching them at build time
    prevents runtime `SyntaxError` / `TypeError` crashes on calculators.

    Args:
        tree: Parsed AST of a source module or generated bundle.
        name: Display filename used in diagnostic error messages.

    Raises:
        BundleError: If one or more incompatible constructs are detected.
    """
    issues: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            issues.append((node.lineno, 'f-string (MicroPython < 1.17)'))

        elif isinstance(node, ast.Dict) and None in node.keys:
            issues.append((node.lineno, 'dict unpacking `{**x}` (PEP 448)'))

        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            for element in node.elts:
                if isinstance(element, ast.Starred):
                    issues.append((
                        element.lineno,
                        'unpacking `*x` in a literal (PEP 448)',
                    ))

        elif isinstance(node, ast.Call):
            starred_args = sum(
                1 for arg in node.args if isinstance(arg, ast.Starred)
            )
            kw_unpacks = sum(1 for kw in node.keywords if kw.arg is None)
            if starred_args > 1 or kw_unpacks > 1:
                issues.append((
                    node.lineno,
                    'multiple unpackings in call (PEP 448)',
                ))

        elif isinstance(node, ast.NamedExpr):
            issues.append((
                node.lineno,
                'walrus operator `:=` (MicroPython < 1.17)',
            ))

        elif (
            isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
            )
            and node.args.posonlyargs
        ):
            issues.append((
                node.lineno,
                'posonlyargs `def f(a, /):` (PEP 570)',
            ))

        elif hasattr(ast, 'Match') and isinstance(node, ast.Match):
            issues.append((
                node.lineno,
                'structural pattern matching `match`/`case` (PEP 634)',
            ))

        elif (
            isinstance(node, (ast.AsyncFor, ast.AsyncWith))
            or (isinstance(node, ast.comprehension) and node.is_async)
        ):
            issues.append((
                node.lineno,
                'async for/with/comprehension (PEP 525/530)',
            ))

    _check_exceptions(tree, issues)

    if issues:
        details = '\n'.join(
            f'  {name}:{line} : {reason}' for line, reason in issues
        )
        raise BundleError(
            'code incompatible with MicroPython 1.9.4:\n' + details
        )
