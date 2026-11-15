# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *

# Addition de quark donne soit un proton soit un neutron
assert QUp('R') + QUp('V') + QDown('B') == Proton()
assert QUp('R') + QDown('V') + QDown('B') == Neutron()

# Addition de proton avec neutron donne un noyau
assert Proton(6) + Neutron(6) == Noyau(Proton(6), Neutron(6))

# Addition de noyau avec electron donne un atome
assert Noyau(Proton(6), Neutron(6)) + Electron(6) == Atome(6)
# Equivaut à
assert Proton(6) + Neutron(6) + Electron(6) == Atome(6)

# Addition d'atome avec un/des proton(s) donne un nouvelle atome
assert Atome('C') + Proton(3) == Atome('F')

# Addition d'atome donne une molécule
assert Atome('O') + Atome('O') == Molecule('O2')

# Addition d'ion monoatomique donne un ion polyatomique
assert IonMonoAtomique('O') + IonMonoAtomique('O') == IonPolyAtomique('O2')
# Juste écrire Ion suffit aussi :
assert Ion('O') + Ion('O') == Ion('O2')


# Multiplier un atome donne une molécule

if params.calculatrice:
    # Utilisez `mul` sur calculatrice :
    assert mul(Atome('O'), 2) == Molecule('O2')

else:
    # Sur Python normal :
    assert Atome('O') * 2 == Molecule('O2')
    # Ou
    assert 2 * Atome('O') == Molecule('O2')


# Addition de molécule
assert Molecule('CO2') + Molecule('CH4') == Molecule('C2O2H4')

# Ajout d'un atome à une molécule
assert Molecule('C2H4') + Atome('C') == Molecule('C3H4')

# Suppression d'un atome à une molécule
assert Molecule('C2H4') - Atome('C') == Molecule('CH4')

# On peut empiler facilement les objets,
#   il faut juste faire attention aux parentèses.
Helium = (
    (   # Noyau
        (QUp(1) + QUp(2) + QDown(3)) # Proton
        +
        (QUp(1) + QDown(2) + QDown(3)) # Neutron
        +
        (Quark(+ 2/3, 1) + Quark(+ 2/3, 2) + Quark(- 1/3, 3)) # Proton
        +
        (Quark(+ 2/3, 1) + Quark(- 1/3, 2) + Quark(- 1/3, 3)) # Neutron
    )
    +
    Electron(2)
)
# Reviens à écrire :
Helium = (
    (   # Noyau
        Proton(2)
        +
        Neutron(2)
    )
    +
    Electron(2)
)
# Qui reviens à écrire :
Helium = Atome('He')
