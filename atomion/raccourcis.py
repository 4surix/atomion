# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from .elements import elements
from .objets import Atome, Electron, Molecule, Neutron, Proton
from .utile import Me as Me
from .utile import Mp as Mp
from .utile import mol as mol
from .utile import u as u


e = Electron()
n = Neutron()
p = Proton()


variables = globals()


### Atomes

for element in elements:
    atome = Atome(element['symbol'])
    variables[atome.symbole] = atome


### Molécules

for symbole in [
    'H2',
    'O2',
    'CH4',
    'H2O',
    'SO3',
    'CO2',
    'NH3',
    'C60',
    'C2H6',
    'C2H4',
    'C3H4',
    'C2H2',
    'C6H6',
    'Cr2O7',
    'C6H6O',
    'C2H4O',
    'C3H6O',
    'C2H5OH',
    'C2H4O2',
    'C4H10O',
    'C2H3OH',
    'CH3CHO',
    'C2O2H4',
    'C2H5CHO',
    'C6H12O6'
]:
    molecule = Molecule(symbole, verif_stable=False)
    variables[symbole] = molecule


# Nettoyage des variables temporaires
del variables['element']
del variables['symbole']
del globals()['variables']


# Noms exportés par `from atomion.raccourcis import *`
#  (raccourcis d'éléments/molécules + constantes ; le reste est interne).
__all__ = [
    nom for nom in globals()
    if not nom.startswith('_')
    and nom not in (
        'elements', 'Atome', 'Molecule', 'Electron', 'Neutron', 'Proton'
    )
]
