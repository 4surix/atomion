# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Generates `atomion.py`, the single-file version for calculators.

The package is recomposed into a single module from its sources:

 - package imports are removed and references are flattened
   (`utile.affichage.x` becomes `affichage.x`, `objets.Atome` becomes `Atome`);
 - type annotations and docstrings are stripped: MicroPython 1.9.4 does not
   evaluate annotations and has no `typing` module;
 - two modules cannot define the same object: explicit error.

The composition order is declared in `MODULES`; it is not inferred from the
import graph, which contains cycles (`utile` <-> `objets`, resolved at call
time via `objets.X`), but verified by executing the resulting file.

The output is then minified: `python_minifier` is required for this
(`pip install "atomion[calc]"`). The delivered file is thus ~35% lighter,
and it is the one verified, both locally and in CI.

Formatting: PEP 8 spacing (two blank lines between definitions).

Usage:
    python mk_file_calculatrice.py
"""

import ast
import importlib
import os
import sys

try:
    import python_minifier
except ImportError:
    raise SystemExit(
        'python_minifier is required to generate the single file:\n'
        '    python -m pip install "atomion[calc]"'
    )


ROOT = os.path.dirname(os.path.abspath(__file__))
PACKAGE = os.path.join(ROOT, 'atomion')


HEADER_TEXT = """
# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------
"""

# Composition order:
#  in a flat module, a name must be defined before it is used.
# `MODULES` must list every module in the package.
MODULES = (
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

# Built-in exceptions supported by MicroPython 1.9.4.
MICROPYTHON_194_EXCEPTIONS = frozenset({
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

# Recent or CPython-only exceptions absent from MicroPython 1.9.4.
UNSUPPORTED_EXCEPTIONS = frozenset({
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


class BundleError(ValueError):
    """The single file cannot be produced."""


class _DynamicAllError(Exception):
    """Raised internally when `__all__` requires runtime evaluation."""


def list_modules():
    """Package modules to compose, in the order of `MODULES`."""
    found = {}

    for folder, subfolders, files in os.walk(PACKAGE):
        subfolders[:] = [
            name for name in subfolders if name != '__pycache__'
        ]

        for filename in files:
            if not filename.endswith('.py'):
                continue

            path = os.path.join(folder, filename)
            relative = os.path.relpath(path, PACKAGE).replace(os.sep, '/')

            found[relative] = path

    # Pure import redirection: nothing to compose.
    found.pop('utile/__init__.py', None)

    missing = [part for part in MODULES if part not in found]

    if missing:
        raise BundleError(
            'modules declared in `MODULES` but missing from package: %s'
            % ', '.join(missing)
        )

    forgotten = sorted(set(found) - set(MODULES))

    if forgotten:
        raise BundleError(
            'package modules missing from `MODULES`: %s'
            % ', '.join(forgotten)
        )

    return tuple((part, found[part]) for part in MODULES)


def _submodule_names():
    """Package submodule and subpackage names absent from the single file.

    These names (derived from `MODULES`, without extension or path)
     refer to modules, not objects: they must not appear in `public_globals`
     or in the `__all__` of the single file.
    """
    names = set()

    for part in MODULES:
        segments = part.split('/')
        names.update(segments[:-1])
        stem = os.path.splitext(segments[-1])[0]

        if stem and stem != '__init__':
            names.add(stem)

    return names


def _base_name(node):
    """Extract the class identifier from a base expression, if any."""
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        return node.attr

    return None


def _inherits_from_exception(class_name, classes, visiting=None):
    """True if `class_name` inherits from `Exception` in MicroPython 1.9.4."""
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


def _has_unknown_external_base(class_node, classes):
    """True if a base class is imported from outside the current AST."""
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


def _check_exceptions(tree, issues):
    """Verify exception portability and inheritance for MicroPython 1.9.4."""
    classes = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    }
    exception_candidates = set()

    for node in ast.walk(tree):
        # Forbid recent/CPython-only exceptions absent from MicroPython 1.9.4.
        if (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id in UNSUPPORTED_EXCEPTIONS
        ):
            issues.append((
                node.lineno,
                'exception `%s` is not supported in MicroPython 1.9.4'
                % node.id,
            ))

        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == 'builtins'
            and node.attr in UNSUPPORTED_EXCEPTIONS
        ):
            issues.append((
                node.lineno,
                'exception `builtins.%s` is not supported in MicroPython '
                '1.9.4' % node.attr,
            ))

        # Avoid overly broad `try ... except` handlers.
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
                base_id = _base_name(base)

                if base_id == 'BaseException':
                    issues.append((
                        node.lineno,
                        'exception `%s` must inherit from `Exception`, '
                        'not `BaseException`' % node.name,
                    ))

    # Ensure custom exceptions inherit from `Exception` (or a valid subclass).
    for class_name in sorted(exception_candidates):
        class_node = classes[class_name]

        if _inherits_from_exception(class_name, classes):
            continue

        # In a single module, an imported base class may live in another
        # module of the package; only reject known non-exception bases here.
        if not _has_unknown_external_base(class_node, classes):
            issues.append((
                class_node.lineno,
                'exception `%s` must inherit from `Exception`' % class_name,
            ))


def check_portability(tree, name='atomion.py'):
    """Fail on constructs absent from MicroPython 1.9.4.

    These constructs raise no error on CPython: without this safeguard,
    they would only be detected when the calculator crashes.
    """
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            issues.append(
                (node.lineno, 'f-string (MicroPython < 1.17)')
            )

        elif isinstance(node, ast.Dict) and None in node.keys:
            issues.append(
                (node.lineno, 'dict unpacking `{**x}` (PEP 448)')
            )

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
            issues.append(
                (node.lineno, 'walrus operator `:=` (MicroPython < 1.17)')
            )

        elif (
            isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
            )
            and node.args.posonlyargs
        ):
            issues.append(
                (node.lineno, 'posonlyargs `def f(a, /):` (PEP 570)')
            )

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
            '  %s:%d : %s' % (name, line, reason)
            for line, reason in issues
        )

        raise BundleError(
            'code incompatible with MicroPython 1.9.4:\n' + details
        )


def _read(path):
    """Syntax tree of a package module."""
    with open(path, encoding='utf-8') as file:
        return ast.parse(file.read(), path)


def _is_docstring(node):
    """True for a docstring expression."""
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _strip_docstring(body):
    """Remove the docstring from a statement body (never empty afterward)."""
    if body and _is_docstring(body[0]):
        del body[0]

    if not body:
        body.append(ast.Pass())


def _strip_annotations(args):
    """Remove type annotations from an argument list."""
    for arg in args.posonlyargs + args.args + args.kwonlyargs + [
        args.vararg, args.kwarg
    ]:
        if arg is not None:
            arg.annotation = None

    return args


class _Flattener(ast.NodeTransformer):
    """Adapt a package module for the single file."""

    def __init__(self, aliases):
        self.aliases = aliases

    def visit_Attribute(self, node):
        """`utile.affichage.embellir` becomes `affichage.embellir`."""
        self.generic_visit(node)

        if (
            isinstance(node.value, ast.Name)
            and node.value.id in self.aliases
        ):
            return ast.copy_location(
                ast.Name(id=node.attr, ctx=node.ctx), node
            )

        return node

    def visit_FunctionDef(self, node):
        """Remove type annotations and the docstring from a function."""
        self.generic_visit(node)

        node.returns = None
        node.args = _strip_annotations(node.args)

        _strip_docstring(node.body)

        return node

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.generic_visit(node)

        _strip_docstring(node.body)

        return node

    def visit_AnnAssign(self, node):
        """`x: int = 1` becomes `x = 1` (and `x: int` disappears)."""
        self.generic_visit(node)

        if node.value is None:
            return None

        return ast.copy_location(
            ast.Assign(targets=[node.target], value=node.value), node
        )


def _is_module(folder, name):
    """True if `folder/name` is a module of the package."""
    return (
        os.path.isfile(os.path.join(folder, name + '.py'))
        or os.path.isfile(os.path.join(folder, name, '__init__.py'))
    )


def _imported_dir(path, node):
    """Package folder targeted by a relative import (`None` if outside)."""
    if node.level == 0:
        return None

    folder = os.path.dirname(os.path.abspath(path))

    for _ in range(node.level - 1):
        folder = os.path.dirname(folder)

        if os.path.commonpath([ROOT, folder]) != ROOT:
            return None

    if node.module:
        folder = os.path.join(folder, *node.module.split('.'))

    return folder


def _module_aliases(tree, path):
    """Names bound to a package module by a relative import.

    `from .. import objets` binds `objets` to the `atomion.objets` module:
    in the single file, `objets.Atome` therefore becomes `Atome`. Conversely,
    `from ..objets import Atome` binds a class: nothing to flatten.
    """
    aliases = set()

    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue

        folder = _imported_dir(path, node)

        if folder is None:
            continue

        aliases.update(
            name.asname or name.name
            for name in node.names
            if name.name != '*' and _is_module(folder, name.name)
        )

    return aliases


def _imports_package(node):
    """True if the import targets a package module (relative or `atomion`)."""
    package_name = os.path.basename(PACKAGE)

    if isinstance(node, ast.ImportFrom):
        return (
            node.level > 0
            or (node.module or '').split('.')[0] == package_name
        )

    return any(name.name.split('.')[0] == package_name for name in node.names)


# Modules used solely for type annotations (stripped from the single file).
TYPING_MODULES = ('typing', '__future__')


def _imports_typing(node):
    """True if the import is only for annotations (removed in single file).

    MicroPython 1.9.4 has neither `typing` nor `from __future__ import
    annotations`: keeping the import would be fatal.
    """
    if isinstance(node, ast.ImportFrom):
        return (node.module or '').split('.')[0] in TYPING_MODULES

    return any(
        name.name.split('.')[0] in TYPING_MODULES for name in node.names
    )


def _filter_stdlib_import(node):
    """Return an import node keeping only non-package, non-typing targets."""
    if isinstance(node, ast.ImportFrom):
        if _imports_package(node) or _imports_typing(node):
            return None
        return node

    package_name = os.path.basename(PACKAGE)
    kept = [
        alias for alias in node.names
        if alias.name.split('.')[0] != package_name
        and alias.name.split('.')[0] not in TYPING_MODULES
    ]

    if not kept:
        return None

    return ast.copy_location(ast.Import(names=kept), node)


def _is_type_checking_guard(node):
    """True for `if TYPE_CHECKING:` or `if typing.TYPE_CHECKING:`."""
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


def _eval_string_sequence(node, path, local_seqs=None):
    """Evaluate a static sequence of export names from `__all__`."""
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        names = []

        for element in node.elts:
            if (
                not isinstance(element, ast.Constant)
                or not isinstance(element.value, str)
            ):
                raise BundleError(
                    '%s:%d: `__all__` must contain only string literals'
                    % (path, getattr(node, 'lineno', 0))
                )

            names.append(element.value)

        return names

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        return (
            _eval_string_sequence(node.left, path, local_seqs)
            + _eval_string_sequence(node.right, path, local_seqs)
        )

    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in ('list', 'tuple', 'set')
        and len(node.args) == 1
        and not node.keywords
    ):
        return _eval_string_sequence(node.args[0], path, local_seqs)

    if (
        local_seqs
        and isinstance(node, ast.Name)
        and node.id in local_seqs
    ):
        return list(local_seqs[node.id])

    raise _DynamicAllError()


def _targets_dunder_all(node):
    """Return `(is_all, is_augmented)` for a top-level assignment node."""
    if isinstance(node, ast.Assign):
        targets = node.targets
        is_aug = False
    elif isinstance(node, ast.AnnAssign) and node.value is not None:
        targets = [node.target]
        is_aug = False
    elif isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Add):
        targets = [node.target]
        is_aug = True
    else:
        return False, False

    is_all = any(
        isinstance(target, ast.Name) and target.id == '__all__'
        for target in targets
    )

    return is_all, is_aug


def _dunder_all_method_call(node):
    """Return `('append' | 'extend', arg)` for `__all__.append/extend(...)`."""
    if (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and isinstance(node.value.func.value, ast.Name)
        and node.value.func.value.id == '__all__'
        and node.value.func.attr in ('append', 'extend')
        and len(node.value.args) == 1
        and not node.value.keywords
    ):
        return node.value.func.attr, node.value.args[0]

    return None


def _is_dunder_all_statement(node):
    """True if a top-level statement defines or mutates `__all__`."""
    return (
        _targets_dunder_all(node)[0]
        or _dunder_all_method_call(node) is not None
    )


def _load_runtime_all(path):
    """Import a package module to evaluate a dynamically computed `__all__`."""
    rel_path = os.path.relpath(os.path.abspath(path), ROOT)
    module_name = os.path.splitext(rel_path)[0].replace(os.sep, '.')

    if module_name.endswith('.__init__'):
        module_name = module_name[:-len('.__init__')]

    added_root = ROOT not in sys.path

    if added_root:
        sys.path.insert(0, ROOT)

    try:
        module = importlib.import_module(module_name)
    except Exception as error:
        raise BundleError(
            '%s: unable to evaluate `__all__` (%s: %s)'
            % (path, type(error).__name__, error)
        )
    finally:
        if added_root and ROOT in sys.path:
            sys.path.remove(ROOT)

    raw_all = getattr(module, '__all__', None)

    if raw_all is None:
        return []

    if not isinstance(raw_all, (list, tuple)) or not all(
        isinstance(item, str) for item in raw_all
    ):
        raise BundleError(
            '%s: `__all__` must evaluate to a list or tuple of strings' % path
        )

    return list(raw_all)


def _extract_all(tree, path):
    """Extract public symbol names declared in `__all__` of a module."""
    exported = []
    local_seqs = {}

    try:
        for node in tree.body:
            is_all, is_aug = _targets_dunder_all(node)

            if is_all:
                names = _eval_string_sequence(node.value, path, local_seqs)

                if is_aug:
                    exported.extend(names)
                else:
                    exported = names

                continue

            call_info = _dunder_all_method_call(node)

            if call_info is not None:
                method, arg = call_info

                if method == 'append':
                    if (
                        not isinstance(arg, ast.Constant)
                        or not isinstance(arg.value, str)
                    ):
                        raise _DynamicAllError()

                    exported.append(arg.value)
                else:
                    exported.extend(
                        _eval_string_sequence(arg, path, local_seqs)
                    )

                continue

            # Track simple top-level string sequences referenced by `__all__`.
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
            ):
                try:
                    local_seqs[node.targets[0].id] = _eval_string_sequence(
                        node.value, path, local_seqs
                    )
                except (BundleError, _DynamicAllError):
                    local_seqs.pop(node.targets[0].id, None)

        # Handle dynamic mutations inside loops/ifs by falling back to runtime.
        for node in tree.body:
            if _is_dunder_all_statement(node):
                continue

            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id == '__all__':
                    raise _DynamicAllError()

    except _DynamicAllError:
        return _load_runtime_all(path)

    return exported


def _module_body(tree, path):
    """Statements of a module retained in the single file.

    Returns `(statements, imports)`; `imports` collects external imports
    (standard library), placed at the top of the single file.
    """
    body = []
    imports = []

    for node in tree.body:
        if _is_type_checking_guard(node):
            body.extend(node.orelse)
            continue

        if _is_dunder_all_statement(node):
            continue

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            filtered = _filter_stdlib_import(node)
            if filtered is not None:
                imports.append(filtered)    # standard library

            continue

        if not _is_docstring(node):
            body.append(node)

    return body, imports


def _targets(node):
    """Names bound by a top-level statement."""
    if isinstance(node, ast.Assign):
        targets = node.targets

    elif isinstance(node, (ast.AnnAssign, ast.For, ast.AsyncFor)):
        targets = [node.target]

    elif isinstance(node, (ast.With, ast.AsyncWith)):
        targets = [
            item.optional_vars for item in node.items
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


def _is_object(node):
    """True for a class or function definition."""
    return isinstance(
        node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    )


def _bound_names(body):
    """Names bound by a list of statements: `name` -> statement."""
    names = {}

    for node in body:
        if _is_object(node):
            names[node.name] = node
            continue

        for name in _targets(node):
            names[name] = node

    return names


def _check_collisions(chunks):
    """Reject two modules defining the same object.

    Simple assignments are excluded: they accumulate in composition order
    (the last one wins), just as in package mode.
    """
    seen = {}

    for part, body in chunks:
        for name, node in _bound_names(body).items():
            if not _is_object(node):
                continue

            if name in seen:
                raise BundleError(
                    'modules `%s` and `%s` both define `%s`'
                    % (seen[name], part, name)
                )

            seen[name] = part


def _deduplicate_imports(imports):
    """External imports, deduplicated and placed at the top of the file."""
    forms = {}

    for node in imports:
        forms.setdefault(ast.unparse(node), node)

    return list(forms.values())


def _verify(text, public_globals=None):
    """Verify the single file: syntax, portability, execution."""
    try:
        tree = ast.parse(text, 'atomion.py')
    except SyntaxError as error:
        raise BundleError(
            'generated single file is invalid: %s' % error
        )

    check_portability(tree)

    _verify_no_annotations(tree)

    namespace = {}
    try:
        exec(compile(tree, 'atomion.py', 'exec'), namespace)
    except Exception as error:
        raise BundleError(
            'generated single file fails to execute '
            '(fix order in `MODULES`?): %s: %s'
            % (type(error).__name__, error)
        )

    if public_globals:
        missing = [name for name in public_globals if name not in namespace]
        if missing:
            raise BundleError(
                'symbols listed in `__all__` but undefined after execution: %s'
                % ', '.join(missing)
            )


def _verify_no_annotations(tree):
    """Fail if any annotation remains (none can be evaluated in 1.9.4)."""
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
                'remaining annotation in single file (line %s)'
                % getattr(node, 'lineno', '?')
            )


def _discover_public_globals():
    """Collect public symbols automatically from `__all__` across `MODULES`."""
    if not os.path.isdir(PACKAGE):
        return []

    try:
        modules = list_modules()
        seen = set()
        public_globals = []

        for _, path in modules:
            for name in _extract_all(_read(path), path):
                if name not in seen:
                    seen.add(name)
                    public_globals.append(name)

        submodule_names = _submodule_names()
        return [name for name in public_globals if name not in submodule_names]
    except BundleError:
        return []


def _build_bundle():
    """Return `(unminified_text, public_globals)` for the single file."""
    chunks = []
    imports = []
    seen_exports = set()
    public_globals = []

    for part, path in list_modules():
        tree = _read(path)
        check_portability(tree, path)

        for name in _extract_all(tree, path):
            if name not in seen_exports:
                seen_exports.add(name)
                public_globals.append(name)

        body, header = _module_body(tree, path)
        imports.extend(header)

        body = _Flattener(
            _module_aliases(tree, path)
        ).visit(ast.Module(body=body, type_ignores=[])).body

        chunks.append((part, body))

    # Submodule names (exception, atom, molecule, ...)
    #  do not exist as such in the single file: 
    #  exclude them from public_globals and the final __all__.
    submodule_names = _submodule_names()
    public_globals = [
        name for name in public_globals if name not in submodule_names
    ]

    _check_collisions(chunks)

    statements = _deduplicate_imports(imports)

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

    text = HEADER_TEXT + '\n' + ast.unparse(
        ast.fix_missing_locations(
            ast.Module(body=statements, type_ignores=[])
        )
    ).strip() + '\n'

    _verify(text, public_globals)

    return text, public_globals


def build():
    """Content of the single file, before minification.

    The resulting text is usable as-is on MicroPython 1.9.4: it is checked
    by `_verify` (syntax, portability, execution).
    """
    text, _ = _build_bundle()
    return text


# Minification options: public API names extracted from `__all__` are
# automatically preserved from global renaming.
MINIFICATION_OPTIONS = {
    'filename': None,
    'remove_annotations': True,
    'remove_pass': True,
    'remove_literal_statements': True,
    'combine_imports': True,
    'hoist_literals': False,
    'rename_locals': True,
    'preserve_locals': None,
    'rename_globals': True,
    'preserve_globals': _discover_public_globals(),
    'remove_object_base': True,
    'convert_posargs_to_args': True,
}


def _minify(text, preserve_globals=None):
    """Reduce the size of the single file."""
    options = dict(MINIFICATION_OPTIONS)

    if preserve_globals is not None:
        options['preserve_globals'] = preserve_globals

    return python_minifier.minify(text, **options)


_CACHE = {}


def generate(force=False):
    """Content of `atomion.py`: `build()` minified and verified.

    The result is cached, as minifying a ~95 KB file is expensive;
    `force=True` recomputes it (determinism check).
    """
    if force or not _CACHE:
        unminified, public_globals = _build_bundle()
        MINIFICATION_OPTIONS['preserve_globals'] = public_globals
        text = _minify(unminified, preserve_globals=public_globals)

        # The delivered file is verified after minification.
        _verify(text, public_globals)

        _CACHE['text'] = text

    return _CACHE['text']


def main():
    """Write the single file (`atomion.py`)."""
    with open('atomion.py', 'w', encoding='utf-8') as file:
        file.write(generate())

    print(
        'atomion.py: %d modules, %d bytes'
        % (len(MODULES), os.path.getsize('atomion.py'))
    )


if __name__ == '__main__':
    main()