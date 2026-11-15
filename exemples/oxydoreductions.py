# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

oxydoR = OxydoReduction(
    Ion('{Cr2O7 2-}'),
    Atome('Fe')
)
assert oxydoR.don == 'Fe -> Fe²⁺ + 2 e⁻'
assert oxydoR.gain == 'Cr₂O₇²⁻ + 14 H⁺ + 6 e⁻ -> 2 Cr³⁺ + 7 H₂O'
assert oxydoR.equation == '3 Fe + Cr₂O₇²⁻ + 14 H⁺ -> 3 Fe²⁺ + 2 Cr³⁺ + 7 H₂O'
