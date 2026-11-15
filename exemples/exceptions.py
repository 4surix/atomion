# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

if not params.calculatrice:
    from atomion.exception import *


try: molecule = Molecule('C3O')
except Instable:
    molecule = Ion('C3O')

try: carbone = Atome('Carbone')
except ValeurIncorrecte:
    carbone = Atome('C')

try: oxygene = carbone + 2
except Incompatible:
    oxygene = carbone + Proton(2)
