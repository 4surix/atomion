# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestFusion(unittest.TestCase):

    def test_noyau_noyau_1(self):
        self.assertEqual(
            Noyau(Proton(1), Neutron(1)) << Noyau(Proton(1), Neutron(1)), 
            [
                Noyau(Proton(2), Neutron(2))
            ]
        )

    def test_noyau_noyau_2(self):
        self.assertEqual(
            Noyau(Proton(1), Neutron(1)) << Noyau(Proton(1), Neutron(2)),
            [
                Noyau(Proton(2), Neutron(2)),
                Neutron(1)
            ]
        )

    def test_noyau_noyau_2(self):
        self.assertEqual(
            Noyau(Proton(2), Neutron(2)) << Noyau(Proton(2), Neutron(1)),
            [
                Noyau(Proton(4), Neutron(3))
            ]
        )


if __name__ == '__main__':
    unittest.main()