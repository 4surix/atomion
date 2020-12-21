from atomion import *


# Addition de quark donne soit un proton soit un neutron
QUp('R') + QUp('V') + QDown('B') == Proton()
QUp('R') + QDown('V') + QDown('B') == Neutron()

# Addition de proton avec neutron donne un noyau
Proton(6) + Neutron(6) == Noyau(Proton(6), Neutron(6))

# Addition de noyau avec electron donne un atome
Noyau(Proton(6), Neutron(6)) + Electron(6) == Atome(6)
# Equivaut à
Proton(6) + Neutron(6) + Electron(6) == Atome(6)

# Addition d'atome avec un/des proton(s) donne un nouvelle atome
Atome('C') + Proton(3) == Atome('F')

# Addition d'atome donne une molécule
Atome('O') + Atome('O') == Molecule('O2')

# Addition d'ion monoatomique donne un ion polyatomique
IonMonoAtomique('O') + IonMonoAtomique('O') == IonPolyAtomique('O2')
# Juste écrire Ion suffit aussi :
Ion('O') + Ion('O') == Ion('O2')


# Multiplier un atome donne une molécule

if params.calculatrice:
    # Utilisez `mul` sur calculatrice :
    mul(Atome('O'), 2) == Molecule('O2')

else:
    # Sur Python normal :
    Atome('O') * 2 == Molecule('O2')
    # Ou
    2 * Atome('O') == Molecule('O2')


# Addition de molécule
Molecule('CO2') + Molecule('CH4') == Molecule('C2O2H4')

# Ajout d'un atome à une molécule
Molecule('C2H4') + Atome('C') == Molecule('C3H4')

# Suppression d'un atome à une molécule
Molecule('C2H4') - Atome('C') == Molecule('CH4')

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
Helium = Atome('H')