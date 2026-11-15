# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Tests de `mk_file_calculatrice`, le bundleur du fichier unique.

Le fichier unique lui-meme est teste par `tests_calculatrice` ; ici, on
verifie ce que le bundleur retire des modules du paquet, comment il aplatit
les references et ce qu'il refuse.
"""

import ast
import sys
import unittest

from pathlib import Path

# `mk_file_calculatrice` est à la racine du dépôt (ce n'est pas un paquet installé).
sys.path.insert(0, Path(__file__).resolve().parent.parent)

import mk_file_calculatrice


class TestExtraction(unittest.TestCase):
    """Instructions conservées dans le fichier unique."""

    def analyser(self, source):

        return mk_file_calculatrice._module_body(
            ast.parse(source), 'module.py'
        )

    def test_imports_du_paquet_retires(self):

        corps, imports = self.analyser('from .. import utile\nx = 1\n')

        self.assertEqual(imports, [])
        self.assertEqual(len(corps), 1)

    def test_imports_de_typage_retires(self):

        corps, imports = self.analyser('from typing import Union\nx = 1\n')

        self.assertEqual(imports, [])
        self.assertEqual(len(corps), 1)

    def test_import_future_retire(self):

        corps, imports = self.analyser(
            'from __future__ import annotations\nx = 1\n'
        )

        self.assertEqual(imports, [])
        self.assertEqual(len(corps), 1)

    def test_imports_stdlib_conserves(self):

        corps, imports = self.analyser('import os\n')

        self.assertEqual(corps, [])
        self.assertEqual(len(imports), 1)

    def test_docstring_de_module_retiree(self):

        corps, _ = self.analyser('"""Documentation."""\nx = 1\n')

        self.assertEqual(len(corps), 1)
        self.assertEqual(corps[0].targets[0].id, 'x')


class TestAplatissement(unittest.TestCase):
    """Références aux modules du paquet et annotations."""

    def aplatir(self, source, alias=('utile', 'objets')):

        return ast.unparse(
            mk_file_calculatrice._Flattener(set(alias)).visit(
                ast.parse(source)
            )
        )

    def test_reference_a_un_module_aplatie(self):

        self.assertEqual(
            self.aplatir('x = utile.affichage'), 'x = affichage'
        )

    def test_reference_imbriquee_aplatie(self):

        self.assertEqual(
            self.aplatir('x = utile.affichage.profil'),
            'x = affichage.profil'
        )

    def test_reference_hors_paquet_intacte(self):

        self.assertEqual(
            self.aplatir('x = params.calculatrice'),
            'x = params.calculatrice'
        )

    def test_annotations_retirees(self):

        self.assertEqual(
            self.aplatir('def f(x: int) -> str:\n    return x'),
            'def f(x):\n    return x'
        )

    def test_variable_annotee_conservee(self):

        self.assertEqual(self.aplatir('x: int = 1'), 'x = 1')

    def test_annotation_seule_disparait(self):

        self.assertEqual(self.aplatir('x: int'), '')

    def test_docstring_de_fonction_retiree(self):

        self.assertEqual(
            self.aplatir('def f():\n    """Documentation."""\n    return 1'),
            'def f():\n    return 1'
        )


class TestAlias(unittest.TestCase):
    """Détection des noms liés à un module du paquet."""

    def test_module_lie_par_import_relatif(self):

        chemin = Path(
            mk_file_calculatrice.PACKAGE, 'objets', 'atome.py'
        )
        arbre = ast.parse(
            'from .. import objets, utile\n'
            'from ..objets import Atome, Ion\n'
        )

        self.assertEqual(
            mk_file_calculatrice._module_aliases(arbre, chemin),
            {'objets', 'utile'}
        )

    def test_classe_liee_par_import_non_aplatie(self):

        chemin = Path(
            mk_file_calculatrice.PACKAGE, 'objets', 'atome.py'
        )
        arbre = ast.parse('from ..objets import Atome\n')

        self.assertEqual(
            mk_file_calculatrice._module_aliases(arbre, chemin), set()
        )


class TestAssemblage(unittest.TestCase):
    """Collisions et déclarations anticipées."""

    def test_deux_objets_homonymes_refuses(self):

        morceaux = [
            ('a.py', ast.parse('class Doublon: pass').body),
            ('b.py', ast.parse('class Doublon: pass').body)
        ]

        with self.assertRaises(mk_file_calculatrice.BundleError):
            mk_file_calculatrice._check_collisions(morceaux)

    def test_affectations_homonymes_tolerees(self):

        morceaux = [
            ('a.py', ast.parse('__all__ = [1]').body),
            ('b.py', ast.parse('__all__ = [2]').body)
        ]

        mk_file_calculatrice._check_collisions(morceaux)

    def test_modules_du_paquet_tous_declares(self):

        declared = [partie for partie, _ in mk_file_calculatrice.list_modules()]

        self.assertEqual(declared, list(mk_file_calculatrice.MODULES))


class TestPortabilite(unittest.TestCase):
    """Garde-fou MicroPython 1.9.4."""

    def test_fstring_refusee(self):

        with self.assertRaises(mk_file_calculatrice.BundleError):
            mk_file_calculatrice.check_portability(
                ast.parse("x = f'{y}'"), 'test.py'
            )

    def test_code_portable_accepte(self):

        mk_file_calculatrice.check_portability(
            ast.parse('x = [1, 2]\n'), 'test.py'
        )


class TestFichierUnique(unittest.TestCase):
    """Le fichier unique produit par le bundleur.

    `construire()` donne le texte avant minification : c'est là que se
    vérifient les retraits faits par le bundleur (docstrings, annotations,
    `typing`, `__future__`). `generer()` donne l'artefact livré, minifié.
    """

    texte = None
    non_minifie = None

    @classmethod
    def setUpClass(cls):

        cls.texte = mk_file_calculatrice.generate()
        cls.non_minifie = mk_file_calculatrice.build()

    def test_aucun_marqueur(self):

        self.assertNotIn('CAPTURE FICHIER CALC', self.non_minifie)

    def test_aucun_import_de_typage(self):

        for texte in (self.non_minifie, self.texte):
            self.assertNotIn('typing', texte)

    def test_aucun_import_future(self):

        for texte in (self.non_minifie, self.texte):
            self.assertNotIn('__future__', texte)

    def test_aucune_annotation(self):

        for texte in (self.non_minifie, self.texte):
            mk_file_calculatrice._verify_no_annotations(ast.parse(texte))

    def test_aucune_docstring(self):

        arbre = ast.parse(self.non_minifie)

        for noeud in ast.walk(arbre):
            if isinstance(
                noeud,
                (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                self.assertIsNone(ast.get_docstring(noeud))

    def test_version_presente(self):

        self.assertIn('__version__', self.texte)

    def test_aucun_maj_type(self):

        self.assertNotIn('MAJ_TYPE', self.non_minifie)

    def test_fichier_livre_minifie(self):

        self.assertLess(len(self.texte), len(self.non_minifie))

    def test_generation_deterministe(self):

        self.assertEqual(
            self.texte, mk_file_calculatrice.generate(force = True)
        )


if __name__ == '__main__':
    unittest.main()

