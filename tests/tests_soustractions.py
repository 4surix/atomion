# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestSubstraction(unittest.TestCase):

    def test_atome_proton(self):
        a = Atome('C') - Proton(3)
        b = Atome('Li')
        self.assertTrue(a == b and a.proton == b.proton == 3)

    def test_atome_neutron(self):
        a = Atome('C') - Neutron(2)
        self.assertTrue(a.neutron == 4)

    def test_atome_electron(self):
        a = Atome('Al') - Electron(3)
        b = Ion('Al')
        self.assertTrue(a == b and a.electron == b.electron == 10)

    def test_molecule_molecule(self):
        self.assertEqual(
            Molecule('C3H4') - Molecule('C2'), 
            Molecule('CH4')
        )

    def test_molecule_atome(self):
        self.assertEqual(Molecule('C2H4') - Atome('C'), Molecule('CH4'))


if __name__ == '__main__':
    unittest.main()