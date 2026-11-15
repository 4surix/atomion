# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

print('\n\n> Quark: \n')
print(Quark(+ 2/3, 'R'))

print('\n\n> Proton: \n')
print(Proton(3))

print('\n\n> Neutron: \n')
print(Neutron(6))

print('\n\n> Electron: \n')
print(Electron(9))

print('\n\n> Noyau: \n')
print(Noyau(Proton(6), Neutron(6)))

print('\n\n> Atome: \n')
print(Atome('C'))

print('\n\n> Molecule: \n')
print(Molecule('O2'))

print('\n\n> Ions monoatomique: \n')
print(Ion('K'))

print('\n\n> Ions polyatomique: \n')
print(Ion('CO2'))

# Choisir le rendu des notations (indépendamment du mode calculatrice)

params.config(affichage = 'ascii')
print(Atome('C').notation_symbole())    # 'C'

params.config(affichage = 'unicode')
print(Atome('C').notation_symbole())    # '¹²₆C'

# Paramètrer affichage

params.config(
    calculatrice = False,
    langue = 'fr',
    nom = True,
    categorie = True,
    proton = True,
    neutron = True,
    electron = True,
    masse = True,
    masse_relative = True,
    couches = True,
    configuration = True
)
