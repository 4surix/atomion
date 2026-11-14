# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

###>>> CAPTURE FICHIER CALC

Neutron = Proton = Electron                \
= Atome = Molecule = MoleculeOrganique     \
= Ion = IonMonoAtomique = IonPolyAtomique  \
= Liaison                                  \
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
    'MoleculeOrganique',
    'Ion',
    'IonMonoAtomique',
    'IonPolyAtomique',
    'Liaison',
    'Noyau',
    'Quark',
    'QUp',
    'QDown'
)

from .. import utile
from . import atome, electron, ion, liaison, molecule, neutron, noyau, proton, quark

for module in [
        molecule, atome, ion, noyau, electron, proton, neutron, quark, liaison,
        utile, utile.equation, utile.oxydo_reduction, utile.acido_basique
    ]:
    module.MAJ_TYPE()
