# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import unittest

from atomion import *
from atomion.elements import elements


class TestElements(unittest.TestCase):

    def test_nombre_elements(self):
        # Le tableau périodique s'arrête à 118 éléments (Oganesson).
        self.assertEqual(len(elements), 118)

    def test_proton_max(self):
        self.assertEqual(Atome(118).symbole, 'Og')

    def test_proton_trop_grand(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Atome(119)
        )

    def test_symbole_inconnu(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Atome('Uue')
        )


if __name__ == '__main__':
    unittest.main()
