# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

# Convertire un atome en ion
cuivre = Atome('Cu')
ion_cuivre = Ion(cuivre)

# Convertire un ion en atome
ion_cuivre = Ion('Cu')
cuivre = Atome(ion_cuivre)
