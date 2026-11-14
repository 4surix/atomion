# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

if not params.calculatrice:
    from atomion.raccourcis import *


assert C + Proton(3) == F

assert O + O == O2

if params.calculatrice:
	# Utilisez `mul` sur calculatrice :
    assert mul(O, 2) == O2
else:
	# Sur Python normal :
    assert O * 2 == O2

assert CO2 + CH4 == C2O2H4

assert C2H4 + C == C3H4

assert C2H4 - C == CH4


e # 1 électron
n # 1 neutron
p # 1 proton


u # Unité de masse atomique unifiée
mol # Une mole


Me # Masse d'un électron
Mp # Masse d'un proton
# 'Mn' est le raccourci du Manganèse, pas la masse du neutron,
#   à réféchir comment rendre disponible la masse du neutron.
