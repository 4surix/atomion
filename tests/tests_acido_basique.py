# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestAcidoBasique(unittest.TestCase):

    def setUp(self):
        self.reaction = AcidoBasique('{C3H5O2 -}', '{H3O +}')

    def test_don(self):
        self.assertEqual(
            self.reaction.don,
            'H₃O⁺ -> H₂O + H⁺'
        )

    def test_gain(self):
        self.assertEqual(
            self.reaction.gain,
            'C₃H₅O₂⁻ + H⁺ -> C₃H₆O₂'
        )

    def test_equation(self):
        self.assertEqual(
            self.reaction.equation,
            'H₃O⁺ + C₃H₅O₂⁻ -> H₂O + C₃H₆O₂'
        )


if __name__ == '__main__':
    unittest.main()