# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *


class TestEquation(unittest.TestCase):

    def test_equilibrage_atome(self):
        self.assertEqual(
            Equation('Cu2S + Cu2O -> Cu + SO2').equilibrer(),
            'Cu₂S + 2 Cu₂O -> 6 Cu + SO₂'
        )

    def test_equilibrage_charge(self):
        self.assertEqual(
            Equation('{Cu 2+} + Al -> Cu + {Al 3+}').equilibrer(),
            '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'
        )


if __name__ == '__main__':
    unittest.main()