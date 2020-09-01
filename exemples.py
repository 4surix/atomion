from atomion import *


### Création

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

### Conversation

# Convertire un atome en ion
cuivre = Atome('Cu')
ion_cuivre = Ion(cuivre)

# Convertire un ion en atome
ion_cuivre = Ion('Cu')
cuivre = Atome(ion_cuivre)


### Opération

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
    from atomion.utile import mul
    assert mul(Atome('O'), 2) == Molecule('O2')

else:

    # Sur Python normal :
    assert Atome('O') * 2 == Molecule('O2')


# Addition de molécule
assert Molecule('CO2') + Molecule('CH4') == Molecule('C2O2H4')

# Ajout d'un atome à une molécule
assert Molecule('C2H4') + Atome('C') == Molecule('C3H4')

# Suppression d'un atome à une molécule
assert Molecule('C2H4') - Atome('C') == Molecule('CH4')


### Raccourcis

from atomion.raccourcis import *

assert C + Proton(3) == F

assert O + O == O2

if params.calculatrice:
    assert mul(O, 2) == O2
else:
    assert O * 2 == O2

assert CO2 + CH4 == C2O2H4

assert C2H4 + C == C3H4

assert C2H4 - C == CH4


### Gestion des erreurs

try: molecule = Molecule('CO3')
except exception.Instable:
    molecule = Ion('CO3')

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

# Pour les Molecules
print('\n--- Molecules ---\n')
print(Molecule('O2'))

# Pour les ions monoatomique
print('\n--- Ions monoatomique ---\n')
print(Ion('K'))

# Pour les ions polyatomique
print('\n--- Ions polyatomique ---\n')
print(Ion('CO2'))


### Equilibrage d'équation

print('\n--- Equilibrage équation chimique ---\n')

print(utile.equilibrage_equation_chimique('Cu2S + Cu2O -> Cu + SO2'))
print(utile.equilibrage_equation_chimique('CH4 + H2O ->  CO2 + H2'))


### Fin
input()