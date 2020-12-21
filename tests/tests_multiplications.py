# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestMultiplication(unittest.TestCase):

    def test_atome_int(self):
        self.assertEqual(2 * Atome('O') * 2, Molecule('O4'))

    def test_neutron_int(self):
        self.assertEqual(2 * Neutron() * 2, Neutron(4))

    def test_proton_int(self):
        self.assertEqual(2 * Proton() * 2, Proton(4))

    def test_electron_int(self):
        self.assertEqual(2 * Electron() * 2, Electron(4))


if __name__ == '__main__':
    unittest.main()