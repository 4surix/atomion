from atomion import *


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