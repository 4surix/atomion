# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestAddition(unittest.TestCase):

    def test_atome_proton(self):
        a = Atome('C') + Proton(3)
        b = Atome('F')
        self.assertTrue(a == b and a.proton == b.proton == 9)

    def test_atome_neutron(self):
        a = Atome('C') + Neutron(2)
        self.assertTrue(a.neutron == 8)

    def test_atome_electron(self):
        a = Atome('Cl') + Electron(1)
        b = Ion('Cl')
        self.assertTrue(a == b and a.electron == b.electron == 18)

    def test_atome_atome(self):
        self.assertEqual(Atome('O') + Atome('O'), Molecule('O2'))

    def test_ion_ion(self):
        self.assertEqual(
            IonMonoAtomique('O') + IonMonoAtomique('O'),
            IonPolyAtomique('O2')
        )

    def test_molecule_molecule(self):
        self.assertEqual(
            Molecule('CO2') + Molecule('CH4'), 
            Molecule('C2O2H4')
        )

    def test_molecule_atome(self):
        self.assertEqual(
            Molecule('C2H4') + Atome('C'),
            Molecule('C3H4')
        )

    def test_proton_proton(self):
        self.assertEqual(
            Proton(2) + Proton(3),
            Proton(5)
        )

    def test_neutron_neutron(self):
        self.assertEqual(
            Neutron(2) + Neutron(3),
            Neutron(5)
        )

    def test_proton_neutron(self):
        self.assertEqual(
            Proton(2) + Neutron(3),
            Noyau(Proton(2), Neutron(3))
        )

    def test_neutron_proton(self):
        self.assertEqual(
            Neutron(2) + Proton(3),
            Noyau(Proton(3), Neutron(2))
        )

    def test_noyau_electron__atome(self):
        self.assertEqual(
            Noyau(Proton(3), Neutron(4)) + Electron(3),
            Atome(3)
        )

    def test_noyau_electron__ion(self):
        self.assertEqual(
            Noyau(Proton(3), Neutron(4)) + Electron(2),
            Ion(3)
        )

    def test_quark__proton(self):
        self.assertEqual(
            QUp(1) + QUp(2) + QDown(3),
            Proton()
        )

    def test_quark__neutron(self):
        self.assertEqual(
            QUp(1) + QDown(2) + QDown(3),
            Neutron()
        )


if __name__ == '__main__':
    unittest.main()