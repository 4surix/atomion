# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import sys
import unittest

from pathlib import Path

# `mk_file_calculatrice` est à la racine du dépôt (ce n'est pas un paquet installé).
sys.path.insert(0, Path(__file__).resolve().parent.parent)

import atomion
import mk_file_calculatrice


def notations(espace):
    """Notations d'objets construits dans un espace de noms donne."""

    objets = [
        espace['Atome']('C'),
        espace['Atome']('H'),
        espace['Atome']('U'),
        espace['Ion']('CO3'),
        espace['Ion']('Cl'),
        espace['Ion']('Na'),
        espace['Ion']('Fe'),
        espace['Molecule']('H2O'),
        espace['Molecule']('CO2'),
        espace['Molecule']('C6H12O6'),
        espace['Proton'](1),
        espace['Neutron'](1),
        espace['Noyau'](espace['Proton'](6), espace['Neutron'](6))
    ]

    lignes = []

    for obj in objets:

        lignes.append(str(obj))
        lignes.append(obj.notation_symbole())

        couche = getattr(obj, 'notation_couche', None)

        if couche is not None:
            lignes.append(couche())

    return lignes


class TestCalculatrice(unittest.TestCase):

    def test_fichier_valide(self):

        texte = mk_file_calculatrice.generate()

        # Plus de marqueurs `CAPTURE` : le fichier est recomposé par AST.
        self.assertNotIn('CAPTURE FICHIER CALC', texte)

        # Aucun `typing` : MicroPython 1.9.4 n'en a pas, et les annotations
        # sont retirées à la génération.
        self.assertNotIn('typing', texte)

        espace = {}
        exec(compile(texte, 'atomion.py', 'exec'), espace)

        for nom in ('Atome', 'Molecule', 'Ion', 'Equation'):
            self.assertIn(nom, espace)

        for nom in ('params', 'mol', 'u', '__version__'):
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

    def test_notations_identiques_au_paquet(self):
        """Le fichier unique doit afficher comme le paquet, au caractère près."""

        espace = {}
        exec(
            compile(mk_file_calculatrice.generate(), 'atomion.py', 'exec'),
            espace
        )

        # Le fichier unique démarre en mode calculatrice (ASCII) : on force le
        #  même profil des deux côtés avant de comparer.
        for parametres in (espace['params'], atomion.params):
            parametres.config(affichage = 'unicode')

        self.assertEqual(notations(espace), notations(vars(atomion)))


if __name__ == '__main__':
    unittest.main()
