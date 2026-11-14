# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import os
import sys
import unittest

# `mk_file_calculatrice` est à la racine du dépôt (ce n'est pas un paquet installé).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mk_file_calculatrice


class TestCalculatrice(unittest.TestCase):

    def test_fichier_valide(self):

        texte = mk_file_calculatrice.generer()

        espace = {}
        exec(compile(texte, 'atomion.py', 'exec'), espace)

        for nom in ('Atome', 'Molecule', 'Ion', 'Equation'):
            self.assertIn(nom, espace)

        self.assertEqual(espace['Atome']('C').symbole, 'C')
        self.assertEqual(
            str(espace['Equation']('H2 + O2 -> H2O').equilibrer()),
            '2 H₂ + O₂ -> 2 H₂O'
        )

        self.assertIn('get_produit', espace)
        self.assertEqual(
            espace['get_produit'](
                espace['Atome']('Fe'), 'oxydoreduction'
            )[0][0],
            'reducteur'
        )


if __name__ == '__main__':
    unittest.main()
