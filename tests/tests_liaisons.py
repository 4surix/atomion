# -*- coding: utf-8 -*-
# Python 3.6.2
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