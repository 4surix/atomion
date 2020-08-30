# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import sys
from atomion import *
from atomion.raccourcis import *


print(utile.params.calculatrice)

#print(equilibrage_equation_chimique('CO + Fe3O4 -> CO2 + Fe'))
print(utile.equilibrage_equation_chimique('Cu2S + Cu2O -> Cu + SO2'))
print(utile.equilibrage_equation_chimique('CH4 + H2O ->  CO2 + H2'))

input(N)
input(CH4)


STABLE = {
    'CH4',
    'C6H12O6',
    'CO2',
    'NH3',
    'C60',
    'C2H6',
    'CH4',
    'C2H4',
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
    'CH3CHCH(OH)',
    'C2H5CHO',
    'C2H3OH',
    'CH3CHO'
}

INSTABLE = {
    'H3',
    'CH5'
}

for notation in {*STABLE, *INSTABLE}:
    try: Molécule(notation)
    except:
    	print('' if notation in INSTABLE else '[!]', 'Instable:', notation)
    else:
        print('' if notation in STABLE else '[!]', 'Stable:', notation)

input()
