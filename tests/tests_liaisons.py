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


class TestLiaison(unittest.TestCase):

    def setUp(self):
        self.liaison = Liaison(Atome('C'), Atome('N'))

    def test_pole_moin(self):
        self.assertEqual(
            self.liaison.pole_moins,
            Atome('N')
        )

    def test_pole_plus(self):
        self.assertEqual(
            self.liaison.pole_plus,
            Atome('C')
        )

    def test_polarisee(self):
        self.assertEqual(
            self.liaison.polarisee,
            True
        )


if __name__ == '__main__':
    unittest.main()
