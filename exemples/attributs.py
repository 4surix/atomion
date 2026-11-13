from atomion import *


# Atome

hydrogene = Atome('H')

assert hydrogene.nom['fr'] == 'Hydrogène'
assert hydrogene.symbole == 'H'
assert hydrogene.categorie['fr'] == 'diatomique non-metal'
assert hydrogene.proton == 1
assert hydrogene.neutron == 0
assert hydrogene.nucleon == 1
assert hydrogene.electron == 1
assert hydrogene.masse == 1.6735599*(10**-27)
assert hydrogene.masse_atomique_relative == 1.008
assert hydrogene.configuration == [1]
assert hydrogene.couches == [1]

# Ion monoatomique

chlorure = Ion('Cl')

assert chlorure.nom['fr'] == 'Chlore'
assert chlorure.symbole == 'Cl'
assert chlorure.categorie['fr'] == 'diatomique non-metal'
assert chlorure.proton == 17
assert chlorure.neutron == 18
assert chlorure.nucleon == 35
assert chlorure.electron == 18
assert chlorure.masse == 5.86001692*(10**-26)
assert chlorure.masse_atomique_relative == 35.45
assert chlorure.configuration == [2, 2, 6, 2, 6]
assert chlorure.couches == [2, 8, 8]
assert chlorure.diff == 1
assert chlorure.charge == '-'

# Molecule

dioxyde_carbone = Molecule('CO2')

assert dioxyde_carbone.atomes == [Atome('C'), Atome('O'), Atome('O')]
assert dioxyde_carbone.proton == 22
assert dioxyde_carbone.neutron == 22
assert dioxyde_carbone.nucleon == 44
assert dioxyde_carbone.electron == 22
assert dioxyde_carbone.masse == 7.36667778*(10**-26)
assert dioxyde_carbone.masse_moleculaire_relative == 44.009

# Ion polyatomique

dioxyde_carbone = Ion('CO2')

assert dioxyde_carbone.ions == [Ion('C'), Ion('O'), Ion('O')]
assert dioxyde_carbone.proton == 22
assert dioxyde_carbone.neutron == 22
assert dioxyde_carbone.nucleon == 44
assert dioxyde_carbone.electron == 22
assert dioxyde_carbone.masse == 7.36667778*(10**-26)
assert dioxyde_carbone.masse_moleculaire_relative == 44.009
