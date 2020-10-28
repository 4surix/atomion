# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

Neutron = Proton = Electron                \
= Atome = Molecule                         \
= Ion = IonMonoAtomique = IonPolyAtomique  \
= Noyau                                    \
= Quark = QUp = QDown                      \
= None

listes_noms = (
    'Neutron',
    'Proton',
    'Electron',
    'Atome',
    'Ion',
    'IonMonoAtomique',
    'IonPolyAtomique',
    'Molecule'
)

from . import (
    molecule, atome, ion, noyau, electron, proton, neutron, quark
)

from .. import utile

for module in [
        molecule, atome, ion, noyau, electron, proton, neutron, quark,
        utile, utile.equation
    ]:
    module.MAJ_TYPE()