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


class TestException(unittest.TestCase):

    def test_molecule_instable(self):
        self.assertRaises(
            exception.Instable,
            lambda: Molecule('LiC')
        )

    def test_proton_instable(self):
        self.assertRaises(
            exception.Instable,
            lambda: QUp('R') + QUp('V') + QDown('V')
        )

    def test_neutron_instable(self):
        self.assertRaises(
            exception.Instable,
            lambda: QUp('R') + QDown('V') + QDown('V')
        )

    def test_atome_valeurIncorrecte(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Atome('Carbone')
        )

    def test_molecule_valeurIncorrecte_nombre(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Molecule('C')
        )

    def test_molecule_valeurIncorrecte_gazNoble(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Molecule('HeNTaI')
        )

    def test_atome_incompatible(self):
        self.assertRaises(
            exception.Incompatible,
            lambda: Atome('C') + 2
        )


if __name__ == '__main__':
    unittest.main()
