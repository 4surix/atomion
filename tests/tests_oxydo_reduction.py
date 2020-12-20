# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestOxydoReduction(unittest.TestCase):

    def setUp(self):
        self.oxydoR = OxydoReduction(Ion('{Cr2O7 2-}'), Atome('Fe'))

    def test_don(self):
        self.assertEqual(
            self.oxydoR.don,
            'Fe -> Fe²⁺ + 2 e⁻'
        )

    def test_gain(self):
        self.assertEqual(
            self.oxydoR.gain,
            'Cr₂O₇²⁻ + 14 H⁺ + 6 e⁻ -> 2 Cr³⁺ + 7 H₂O'
        )

    def test_equation(self):
        self.assertEqual(
            self.oxydoR.equation,
            '3 Fe + Cr₂O₇²⁻ + 14 H⁺ -> 3 Fe²⁺ + 2 Cr³⁺ + 7 H₂O'
        )


if __name__ == '__main__':
    unittest.main()