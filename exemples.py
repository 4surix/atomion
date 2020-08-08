from atomion import *


### Création

# Créer un Atome
Atome('H')

# Créer un Ion
Ion('H')

# Créer une molécule
Molécule('CH4')


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
Atome('O') + Atome('O') == Molécule('O2')

# Multiplier un atome donne une molécule
Atome('O') * 2 == Molécule('O2')


# Addition de molécule
Molécule('CO2') + Molécule('CH4') == Molécule('C2O2H4')


# Ajout d'un atome à une molécule
Molécule('C2H4') + Atome('C') == Molécule('C3H4')

# Suppression d'un atome à une molécule
Molécule('C2H4') - Atome('C') == Molécule('CH4')


### Gestion des erreurs

try: molécule = Molécule('H3')
except exception.MoleculeInstable:
	molécule = Molécule('H2')

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

# Pour les molécules
print('\n--- Molécules ---\n')

print(Molécule('O2'))


### Démonstration

# Récupérer le nombre d'électron suivant la masse
print('\n--- Nombre électron suivant masse ---\n')

carbone = Atome('C')
demo = carbone.demonstration(recup='électron', avec='masse')
print(demo)

# Récupérer le nombre de neutron suivant le nombre de proton
print('\n--- Nombre neutron suivant nombre proton ---\n')

carbone = Atome('C')
demo = carbone.demonstration(recup='neutron', avec='Z')
print(demo)


### Fin
input()