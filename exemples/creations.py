from atomion import *


# Créer un quark
Quark(+ 2/3, 'R') == QUp('R')
Quark(- 1/3, 'V') == QDown('V')

# Créer 3 Proton
Proton(3)

# Créer 1 Neutron
Neutron()

# Créer 2 Electron
Electron(2)

# Créer un noyeau
Noyau(Proton(6), Neutron(6))

# Créer un Atome
Atome('H')

# Créer un Ion
Ion('H')
# On peut aussi écrire :
IonMonoAtomique('H')

# Créer une molécule
Molecule('CH4')

# Créer un Ion polyatomique
Ion('CO3')
# On peut aussi écrire :
IonPolyAtomique('CO3')