# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .objets import Atome, Molecule, Electron, Neutron, Proton
from .elements import elements


###>>> CAPTURE FICHIER CALC

e = Electron()
n = Neutron()
p = Proton()


u = 1.660538921*(10**-27)
mol = 6.02214076*(10**23)

Me = 9.109*(10**-31)
Mp = 1.672649*(10**-27)
Mn = 1.67493*(10**-27)


variables = globals()


### Atomes

for element in elements:
    atome = Atome(element['symbol'])
    variables[atome.symbole] = atome


### Molécules

for symbole in [
    'H2',
    'O2',
    'CH4',
    'H2O',
    'SO3',
    'CO2',
    'NH3',
    'C60',
    'CH4',
    'NH3',
    'C2H6',
    'C2H4',
    'C3H4',
    'C2H2',
    'C6H6',
    'Cr2O7',
    'C6H6O',
    'C2H4O',
    'C3H6O',
    'C2H5OH',
    'C2H4O2',
    'C4H10O',
    'C2H3OH',
    'CH3CHO',
    'C2O2H4',
    'C2H5CHO',
    'C6H12O6'
]:
    molecule = Molecule(symbole, verif_stable=False)
    variables[symbole] = molecule


# Netoyage variable inutile

del variables['elements']
del variables['element']
del variables['symbole']
del globals()['variables']

###<<< CAPTURE FICHIER CALC