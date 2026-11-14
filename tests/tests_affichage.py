# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import unittest

from atomion import *
from atomion.utile import params


class TestAffichageUnicode(unittest.TestCase):

    def setUp(self):
        self.calculatrice = params.calculatrice
        params.config(affichage='unicode')

    def tearDown(self):
        params.config(calculatrice=self.calculatrice)

    def test_calculatrice_desactive(self):
        self.assertFalse(params.calculatrice)

    def test_atomes(self):
        self.assertEqual(Atome('C').notation_symbole(), '¹²₆C')
        self.assertEqual(Atome('C').notation_symbole(A=False), '₆C')
        self.assertEqual(Atome('C').notation_symbole(Z=False), '¹²C')
        self.assertEqual(Atome('C').notation_couche(), '(K)² (L)⁴')
        self.assertEqual(Atome('C').notation_configuration(), '1s² 2s² 2p²')
        self.assertIn('Elément: Carbone', str(Atome('C')))
        self.assertIn('Couche électronique', str(Atome('C')))

    def test_ions(self):
        self.assertEqual(Ion('Cl').notation_symbole(), '³⁵₁₇Cl⁻')
        self.assertEqual(Ion('Cl').notation_symbole(A=False), '₁₇Cl⁻')
        self.assertEqual(Ion('Cl').notation_symbole(charge=False), '³⁵₁₇Cl')
        self.assertEqual(Ion('CO3').notation_symbole(), 'CO₃²⁻')

    def test_molecules(self):
        self.assertEqual(Molecule('H2O').notation_symbole(), 'H₂O')
        self.assertIn('Molécule H₂O', str(Molecule('H2O')))

    def test_particules(self):
        self.assertEqual(Proton(3).notation_symbole(), '³₃p⁺')
        self.assertEqual(Proton(3).notation_symbole(A=False), '₃p⁺')
        self.assertEqual(Neutron(6).notation_symbole(), '⁶₀n⁰')
        self.assertEqual(Electron(1).notation_symbole(), 'e⁻')
        self.assertEqual(Electron(9).notation_symbole(), '9e⁻')
        self.assertEqual(
            Noyau(Proton(6), Neutron(6)).notation_symbole(), '¹²₆X'
        )

    def test_equations(self):
        self.assertEqual(str(DemiEquation('Cl2', '{Cl -}')), 'Cl₂ -> Cl⁻')
        self.assertEqual(
            str(Equation('{Cu 2+} + Al -> Cu + {Al 3+}').equilibrer()),
            '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'
        )
        self.assertEqual(
            str(OxydoReduction(Ion('{Cr2O7 2-}'), Atome('Fe')).equation),
            '3 Fe + Cr₂O₇²⁻ + 14 H⁺ -> 3 Fe²⁺ + 2 Cr³⁺ + 7 H₂O'
        )


class TestAffichageAscii(unittest.TestCase):

    def setUp(self):
        self.calculatrice = params.calculatrice
        params.config(affichage='ascii')

    def tearDown(self):
        params.config(calculatrice=self.calculatrice)

    def test_calculatrice_active(self):
        self.assertTrue(params.calculatrice)

    def test_atomes(self):
        self.assertEqual(Atome('C').notation_symbole(), 'C')
        self.assertEqual(Atome('C').notation_symbole(A=False), 'C')
        self.assertEqual(Atome('C').notation_symbole(Z=False), 'C')
        self.assertEqual(Atome('C').notation_couche(), '(K)2 (L)4')
        self.assertEqual(Atome('C').notation_configuration(), '1s2 2s2 2p2')
        self.assertIn('Element: Carbone', str(Atome('C')))
        self.assertNotIn('Elément', str(Atome('C')))
        self.assertIn('Couche electronique', str(Atome('C')))

    def test_ions(self):
        self.assertEqual(Ion('Cl').notation_symbole(), '{Cl 1-}')
        self.assertEqual(Ion('Cl').notation_symbole(A=False), '{Cl 1-}')
        self.assertEqual(Ion('Cl').notation_symbole(charge=False), 'Cl')
        self.assertEqual(Ion('CO3').notation_symbole(), '{CO3 2-}')

    def test_molecules(self):
        self.assertEqual(Molecule('H2O').notation_symbole(), 'H2O')
        self.assertIn('Molecule H2O', str(Molecule('H2O')))

    def test_particules(self):
        self.assertEqual(Proton(3).notation_symbole(), 'p+')
        self.assertEqual(Proton(3).notation_symbole(A=False), 'p+')
        self.assertEqual(Neutron(6).notation_symbole(), 'n')
        self.assertEqual(Electron(1).notation_symbole(), 'e-')
        self.assertEqual(Electron(9).notation_symbole(), '9e-')
        self.assertEqual(Noyau(Proton(6), Neutron(6)).notation_symbole(), 'X')

    def test_equations(self):
        self.assertEqual(str(DemiEquation('Cl2', '{Cl -}')), 'Cl2 -> {Cl 1-}')
        self.assertEqual(
            str(Equation('{Cu 2+} + Al -> Cu + {Al 3+}').equilibrer()),
            '3 {Cu 2+} + 2 Al -> 3 Cu + 2 {Al 3+}'
        )
        self.assertEqual(
            str(OxydoReduction(Ion('{Cr2O7 2-}'), Atome('Fe')).equation),
            '3 Fe + {Cr2O7 2-} + 14 {H 1+} -> 3 {Fe 2+} + 2 {Cr 3+} + 7 H2O'
        )


class TestConfigAffichage(unittest.TestCase):

    def setUp(self):
        self.calculatrice = params.calculatrice

    def tearDown(self):
        params.config(calculatrice=self.calculatrice)

    def test_affichage_inconnu(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: params.config(affichage='couleur')
        )

    def test_calculatrice_bascule_le_profil(self):
        # `calculatrice` doit changer le rendu immediatement,
        #  et pas seulement activer les fonctions de calcul.
        params.config(calculatrice=True)
        self.assertEqual(Atome('C').notation_symbole(), 'C')
        self.assertEqual(Ion('Cl').notation_symbole(), '{Cl 1-}')

        params.config(calculatrice=False)
        self.assertEqual(Atome('C').notation_symbole(), '¹²₆C')
        self.assertEqual(Ion('Cl').notation_symbole(), '³⁵₁₇Cl⁻')

    def test_affichage_et_calculatrice_coherents(self):
        params.config(affichage='ascii')
        self.assertTrue(params.calculatrice)

        params.config(affichage='unicode')
        self.assertFalse(params.calculatrice)


if __name__ == '__main__':
    unittest.main()
