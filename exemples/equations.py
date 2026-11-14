# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

# Equilibre atomes
equation = Equation('Cu2S + Cu2O -> Cu + SO2')
assert equation.equilibrer() == 'Cu₂S + 2 Cu₂O -> 6 Cu + SO₂'

# Equilibre charges
equation = Equation('{Cu 2+} + Al -> Cu + {Al 3+}')
assert equation.equilibrer() == '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'

# Attributs
assert equation.notation == '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'
assert equation.coefficients == [[3, 2], [3, 2]]
assert equation.spectatrices == []
assert equation.reactifs == [Ion('{Cu 2+}'), Atome('Al')]
assert equation.produits == [Atome('Cu'), Ion('{Al 3+}')]

# Demi-équation
equation = DemiEquation('Cl2', '{Cl -}')
equation.equilibrer()
assert equation == 'Cl₂ + 2 e⁻ -> 2 Cl⁻'
