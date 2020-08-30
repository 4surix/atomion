from atomion import *


### Création

# Créer un Atome
Atome('H')

# Créer un Ion
Ion('H')

# Créer une molécule
Molecule('CH4')


### Conversation

# Convertire un Atome en Ion
cuivre = Atome('Cu')
ion_cuivre = Ion(cuivre)

# Convertire un Ion en Atome
ion_cuivre = Ion('Cu')
cuivre = Atome(ion_cuivre)


### Opération

# Addition d'atome avec un/des proton(s) donne un nouvelle atome
Atome('C') + Proton(3) == Atome('F')

# Addition d'atome donne une molécule
Atome('O') + Atome('O') == Molecule('O2')

# Multiplier un atome donne une molécule
if params.calculatrice:
    # Utilisez `mul` sur calculatrice :
    from atomion.utile import mul
    mul(Atome('O'), 2) == Molecule('O2')
else:
    # Sur Python normal :
    Atome('O') * 2 == Molecule('O2')

# Addition de molécule
Molecule('CO2') + Molecule('CH4') == Molecule('C2O2H4')

# Ajout d'un atome à une molécule
Molecule('C2H4') + Atome('C') == Molecule('C3H4')

# Suppression d'un atome à une molécule
Molecule('C2H4') - Atome('C') == Molecule('CH4')


### Raccourcis

from atomion.raccourcis import *

C + Proton(3) == F

O + O == O2

if params.calculatrice:
    mul(O, 2) == O2
else:
    O * 2 == O2

CO2 + CH4 == C2O2H4

C2H4 + C == C3H4

C2H4 - C == CH4


### Gestion des erreurs

try: molecule = Molecule('H3')
except exception.Instable:
    molecule = Molecule('H2')

try: carbone = Atome('Carbone')
except exception.ValeurIncorrecte:
    carbone = Atome('C')

try: oxygene = carbone + 2
except exception.Incompatible:
    oxygene = carbone + Proton(2)


### Informations

# Pour les atomes
print('\n--- Atomes ---\n')

print(Atome('C'))

# Pour les ions
print('\n--- Ions ---\n')

print(Ion('K'))

# Pour les Molecules
print('\n--- Molecules ---\n')

print(Molecule('O2'))


### Equilibrage d'équation

print(utile.equilibrage_equation_chimique('Cu2S + Cu2O -> Cu + SO2'))
print(utile.equilibrage_equation_chimique('CH4 + H2O ->  CO2 + H2'))


### Fin
input()