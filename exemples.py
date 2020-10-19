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


### Conversions

# Convertire un atome en ion
cuivre = Atome('Cu')
ion_cuivre = Ion(cuivre)

# Convertire un ion en atome
ion_cuivre = Ion('Cu')
cuivre = Atome(ion_cuivre)


### Opération

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

try: molecule = Molecule('CO3')
except exception.Instable:
    molecule = Ion('CO3')

try: carbone = Atome('Carbone')
except exception.ValeurIncorrecte:
    carbone = Atome('C')

try: oxygene = carbone + 2
except exception.Incompatible:
    oxygene = carbone + Proton(2)


### Affichage

print('\n\n> Atomes: \n')
print(Atome('C'))

print('\n\n> Molecule: \n')
print(Molecule('O2'))

print('\n\n> Ions monoatomique: \n')
print(Ion('K'))

print('\n\n> Ions polyatomique: \n')
print(Ion('CO2'))

# Paramètrer affichage

params.config(
    calculatrice = False,
    langue = 'fr',
    element = True,
    categorie = True,
    proton = True,
    neutron = True,
    electron = True,
    masse = True,
    masse_relative = True,
    couches = True,
    configuration = True
)


### Equation chimlique

# Equilibre atomes
equation = Equation('Cu2S + Cu2O -> Cu + SO2')
equation.equilibrer() == 'Cu₂S + 2 Cu₂O -> 6 Cu + SO₂'

# Equilibre charges
equation = Equation('{Cu 2+} + Al -> Cu + {Al 3+}')
equation.equilibrer() == '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'

# Attributs
equation.notation == '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'
equation.coefficients == [[3, 2], [3, 2]]
equation.spectatrices == []
equation.reactifs == [Ion('Cu'), Atome('Al')]
equation.produits == [Atome('Cu'), Atome('Al')]


### Reaction chimique

reaction = Reaction(
    equation = Equation('Al + O2 -> Al2O3'),
    quantites_reactifs = {Atome('Al'): 1.6, Molecule('O2'): 1.3}
)
reaction.initial() == {
    Atome('Al'): 1.6,
    Molecule('O2'): 1.3,
    Molecule('Al2O3'): 0
}
reaction.intermediaire(0.1) == {
    Atome('Al'): 1.2,
    Molecule('O2'): 1.0,
    Molecule('Al2O3'): 0.2
}
reaction.final() == {
    Atome('Al'): 0.0,
    Molecule('O2'): 0.1,
    Molecule('Al2O3'): 0.8
}
reaction.reactifs_limitants() == [Atome('Al')]

reaction = Reaction(
    equation = Equation('Al + O2 -> Al2O3'),
    quantites_produits = {Molecule('Al2O3'): 0.7}
)
reaction.initial() == {
    Atome('Al'): 1.4,
    Molecule('O2'): 1.05,
    Molecule('Al2O3'): 0
}
reaction.intermediaire(0.1) == {
    Atome('Al'): 1.0,
    Molecule('O2'): 0.75,
    Molecule('Al2O3'): 0.2
}
reaction.final() == {
    Atome('Al'): 0,
    Molecule('O2'): 0,
    Molecule('Al2O3'): 0.7
}
reaction.reactifs_limitants() == [Atome('Al'), Molecule('O2')]

### Attributs

# Atome

hydrogene = Atome('H')

hydrogene.nom == 'Hydrogène'
hydrogene.symbole == 'H'
hydrogene.categorie == 'diatomique non-metal'
hydrogene.proton == 1
hydrogene.neutron == 0
hydrogene.nucleon == 1
hydrogene.electron == 1
hydrogene.masse == 1.635*(10**-26)
hydrogene.masse_atomique_relative == 1.008
hydrogene.configuration == [1]
hydrogene.couches == [1]

# Ion monoatomique

chlorure = Ion('Cl')

chlorure.nom == 'Chlore'
chlorure.symbole == 'Cl'
chlorure.categorie == 'diatomique non-metal'
chlorure.proton == 17
chlorure.neutron == 18
chlorure.nucleon == 35
chlorure.electron == 18
chlorure.masse == 5.28*(10**-26)
chlorure.masse_atomique_relative == 35.45
chlorure.configuration == [2, 2, 6, 2, 6]
chlorure.couches == [2, 8, 8]
chlorure.diff == '-'
chlorure.charge == 1

# Molecule

dioxyde_carbone = Molecule('CO2')

dioxyde_carbone.atomes == [Atome('C'), Atome('O'), Atome('O')]
dioxyde_carbone.proton == 22
dioxyde_carbone.neutron == 22
dioxyde_carbone.nucleon == 44
dioxyde_carbone.electron == 22
dioxyde_carbone.masse == 7.366*(10**-26)
dioxyde_carbone.masse_moleculaire_relative == 44.009

# Ion polyatomique

dioxyde_carbone = Ion('CO2')

dioxyde_carbone.ions == [Ion('C'), Ion('O'), Ion('O')]
dioxyde_carbone.proton == 22
dioxyde_carbone.neutron == 22
dioxyde_carbone.nucleon == 44
dioxyde_carbone.electron == 22
dioxyde_carbone.masse == 7.366*(10**-26)
dioxyde_carbone.masse_moleculaire_relative == 44.009


### Fin
input()