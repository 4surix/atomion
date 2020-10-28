# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .objets import Atome, Molecule
from .elements import elements


###>>> CAPTURE FICHIER CALC

variables = globals()


### Atomes

for element in elements:
    atome = Atome(element['symbol'])
    variables[atome.symbole] = atome


### Molécules

for symbole in [
    'CH4',
    'C6H12O6',
    'O2',
    'CO2',
    'NH3',
    'C60',
    'C2H6',
    'CH4',
    'C2H4',
    'C3H4',
    'C2H2',
    'C6H6',
    'C2H5Br',
    'C2H5OH',
    'C6H6O',
    'C2H4O2',
    'C2H4O',
    'C3H6O',
    'H2O',
    'SO3',
    'C4H10O',
    'NH3',
    'C2H5CHO',
    'C2H3OH',
    'CH3CHO',
    'C2O2H4'
]:
    molecule = Molecule(symbole)
    variables[symbole] = molecule


# Netoyage variable inutile

del variables['elements']
del variables['element']
del variables['symbole']
del globals()['variables']

###<<< CAPTURE FICHIER CALC