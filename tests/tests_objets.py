# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestObjet(unittest.TestCase):

    def test_ionmonoatomique(self):
        self.assertEqual(
            Ion('O'),
            IonMonoAtomique('O')
        )

    def test_ionpolyatomique(self):
        self.assertEqual(
            Ion('O2'),
            IonPolyAtomique('O2')
        )

    def test_stable(self):
        for symbole in [
            'O3',
            'CH4',
            'C6H12O6',
            'O2',
            'CO2',
            'NH3',
            'C60',
            'C2H6',
            'CH4',
            'C2H4',
            'C3H4',
            'C2H2',
            'C6H6',
            'C2H5Br',
            'C2H5OH',
            'C6H6O',
            'C2H4O2',
            'C2H4O',
            'C3H6O',
            'H2O',
            'SO3',
            'C4H10O',
            'NH3',
            'C2H5CHO',
            'C2H3OH',
            'CH3CHO',
            'C2O2H4'
        ]:
            Molecule(symbole)

    def test_str(self):
        str(Quark(+ 2/3, 'R'))
        str(Proton())
        str(Neutron())
        str(Electron())
        str(Noyau(Proton(6), Neutron(6)))
        str(Atome('C'))
        str(Molecule('O2'))
        str(Ion('K'))
        str(Ion('CO2'))

    def test_repr(self):
        repr(Quark(+ 2/3, 'R'))
        repr(Proton())
        repr(Neutron())
        repr(Electron())
        repr(Noyau(Proton(6), Neutron(6)))
        repr(Atome('C'))
        repr(Molecule('O2'))
        repr(Ion('K'))
        repr(Ion('CO2'))


if __name__ == '__main__':
    unittest.main()