# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestMultiplication(unittest.TestCase):

    def test_atome_int(self):
        self.assertEqual(Atome('O') * 2, Molecule('O2'))


if __name__ == '__main__':
    unittest.main()