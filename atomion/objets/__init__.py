# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

###>>> CAPTURE FICHIER CALC

Neutron = Proton = Electron                \
= Atome = Molecule                         \
= Ion = IonMonoAtomique = IonPolyAtomique  \
= Noyau                                    \
= Quark = QUp = QDown                      \
= None

###<<< CAPTURE FICHIER CALC

listes_noms = (
    'Neutron',
    'Proton',
    'Electron',
    'Atome',
    'Molecule',
    'Ion',
    'IonMonoAtomique',
    'IonPolyAtomique',
    'Noyau',
    'Quark',
    'QUp',
    'QDown'
)

from . import (
    molecule, atome, ion, noyau, electron, proton, neutron, quark
)

from .. import utile

for module in [
        molecule, atome, ion, noyau, electron, proton, neutron, quark,
        utile, utile.equation, utile.oxydo_reduction
    ]:
    module.MAJ_TYPE()