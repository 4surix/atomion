# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import unittest

from atomion import *


class TestAttributsAtome(unittest.TestCase):

    def setUp(self):
        self.hydrogene = Atome('H')

    def test_nom(self):
        self.assertEqual(self.hydrogene.nom, 'Hydrogène')

    def test_symbole(self):
        self.assertEqual(self.hydrogene.symbole, 'H')

    def test_categorie(self):
        self.assertEqual(
            self.hydrogene.categorie, 'diatomique non-metal'
        )

    def test_particules(self):
        self.assertEqual(
            (
                self.hydrogene.proton,
                self.hydrogene.neutron,
                self.hydrogene.nucleon,
                self.hydrogene.electron
            ),
            (1, 0, 1, 1)
        )

    def test_masse(self):
        self.assertAlmostEqual(
            self.hydrogene.masse, 1.6735599*(10**-27), delta=1e-32
        )
        self.assertEqual(self.hydrogene.masse_atomique_relative, 1.008)

    def test_couches(self):
        self.assertEqual(self.hydrogene.configuration, [1])
        self.assertEqual(self.hydrogene.couches, [1])


class TestAttributsIonMonoAtomique(unittest.TestCase):

    def setUp(self):
        self.chlorure = Ion('Cl')

    def test_nom(self):
        self.assertEqual(self.chlorure.nom, 'Chlore')

    def test_categorie(self):
        self.assertEqual(
            self.chlorure.categorie, 'diatomique non-metal'
        )

    def test_particules(self):
        self.assertEqual(
            (
                self.chlorure.proton,
                self.chlorure.neutron,
                self.chlorure.nucleon,
                self.chlorure.electron
            ),
            (17, 18, 35, 18)
        )

    def test_masse(self):
        self.assertAlmostEqual(
            self.chlorure.masse, 5.86001692*(10**-26), delta=1e-31
        )
        self.assertEqual(self.chlorure.masse_atomique_relative, 35.45)

    def test_couches(self):
        self.assertEqual(self.chlorure.configuration, [2, 2, 6, 2, 6])
        self.assertEqual(self.chlorure.couches, [2, 8, 8])

    def test_charge(self):
        self.assertEqual(self.chlorure.diff, 1)
        self.assertEqual(self.chlorure.charge, '-')


class TestAttributsMolecule(unittest.TestCase):

    def setUp(self):
        self.dioxyde_carbone = Molecule('CO2')

    def test_atomes(self):
        self.assertEqual(
            self.dioxyde_carbone.atomes,
            [Atome('C'), Atome('O'), Atome('O')]
        )

    def test_particules(self):
        self.assertEqual(
            (
                self.dioxyde_carbone.proton,
                self.dioxyde_carbone.neutron,
                self.dioxyde_carbone.nucleon,
                self.dioxyde_carbone.electron
            ),
            (22, 22, 44, 22)
        )

    def test_masse(self):
        self.assertAlmostEqual(
            self.dioxyde_carbone.masse, 7.36667778*(10**-26), delta=1e-31
        )
        self.assertEqual(
            self.dioxyde_carbone.masse_moleculaire_relative, 44.009
        )


class TestAttributsIonPolyAtomique(unittest.TestCase):

    def setUp(self):
        self.dioxyde_carbone = Ion('CO2')

    def test_ions(self):
        self.assertEqual(
            self.dioxyde_carbone.ions,
            [Ion('C'), Ion('O'), Ion('O')]
        )

    def test_particules(self):
        self.assertEqual(
            (
                self.dioxyde_carbone.proton,
                self.dioxyde_carbone.neutron,
                self.dioxyde_carbone.nucleon,
                self.dioxyde_carbone.electron
            ),
            (22, 22, 44, 22)
        )

    def test_masse(self):
        self.assertAlmostEqual(
            self.dioxyde_carbone.masse, 7.36667778*(10**-26), delta=1e-31
        )
        self.assertEqual(
            self.dioxyde_carbone.masse_moleculaire_relative, 44.009
        )


if __name__ == '__main__':
    unittest.main()
