# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

reaction = Reaction(
    equation = Equation('Al + O2 -> Al2O3'),
    quantites_reactifs = {Atome('Al'): 1.6, Molecule('O2'): 1.3}
)
assert reaction.initial() == {
    Atome('Al'): 1.6,
    Molecule('O2'): 1.3,
    Molecule('Al2O3'): 0
}
assert reaction.intermediaire(0.1) == {
    Atome('Al'): 1.2,
    Molecule('O2'): 1.0,
    Molecule('Al2O3'): 0.2
}
assert reaction.final() == {
    Atome('Al'): 0.0,
    Molecule('O2'): 0.1,
    Molecule('Al2O3'): 0.8
}
assert reaction.reactifs_limitants() == [Atome('Al')]

reaction = Reaction(
    equation = Equation('Al + O2 -> Al2O3'),
    quantites_produits = {Molecule('Al2O3'): 0.7}
)
assert reaction.initial() == {
    Atome('Al'): 1.4,
    Molecule('O2'): 1.05,
    Molecule('Al2O3'): 0
}
assert reaction.intermediaire(0.1) == {
    Atome('Al'): 1.0,
    Molecule('O2'): 0.75,
    Molecule('Al2O3'): 0.2
}
assert reaction.final() == {
    Atome('Al'): 0,
    Molecule('O2'): 0,
    Molecule('Al2O3'): 0.7
}
assert reaction.reactifs_limitants() == [Atome('Al'), Molecule('O2')]
