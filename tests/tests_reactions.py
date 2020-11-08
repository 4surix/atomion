# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestReactionQuantitesReactifs(unittest.TestCase):

    def setUp(self):
        self.reaction = Reaction(
            equation = Equation('Al + O2 -> Al2O3'),
            quantites_reactifs = {Atome('Al'): 1.6, Molecule('O2'): 1.3}
        )

    def test_initial(self):
        self.assertEqual(
            self.reaction.initial(),
            {
                Atome('Al'): 1.6,
                Molecule('O2'): 1.3,
                Molecule('Al2O3'): 0
            }
        )

    def test_intermediaire(self):
        self.assertEqual(
            self.reaction.intermediaire(0.1),
            {
                Atome('Al'): 1.2,
                Molecule('O2'): 1.0,
                Molecule('Al2O3'): 0.2
            }
        )

    def test_final(self):
        self.assertEqual(
            self.reaction.final(),
            {
                Atome('Al'): 0.0,
                Molecule('O2'): 0.1,
                Molecule('Al2O3'): 0.8
            }
        )

    def test_reactifs_limitants(self):
        self.assertEqual(
            self.reaction.reactifs_limitants(),
            [Atome('Al')]
        )


class TestReactionQuantitesProduits(unittest.TestCase):

    def setUp(self):
        self.reaction = Reaction(
            equation = Equation('Al + O2 -> Al2O3'),
            quantites_produits = {Molecule('Al2O3'): 0.7}
        )

    def test_initial(self):
        self.assertEqual(
            self.reaction.initial(),
            {
                Atome('Al'): 1.4,
                Molecule('O2'): 1.05,
                Molecule('Al2O3'): 0
            }
        )

    def test_intermediaire(self):
        self.assertEqual(
            self.reaction.intermediaire(0.1),
            {
                Atome('Al'): 1.0,
                Molecule('O2'): 0.75,
                Molecule('Al2O3'): 0.2
            }
        )

    def test_final(self):
        self.assertEqual(
            self.reaction.final(),
            {
                Atome('Al'): 0,
                Molecule('O2'): 0,
                Molecule('Al2O3'): 0.7
            }
        )

    def test_reactifs_limitants(self):
        self.assertEqual(
            self.reaction.reactifs_limitants(),
            [Atome('Al'), Molecule('O2')]
        )


if __name__ == '__main__':
    unittest.main()