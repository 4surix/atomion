from atomion import *

if not params.calculatrice:
    from atomion.raccourcis import *


C + Proton(3) == F

O + O == O2

if params.calculatrice:
	# Utilisez `mul` sur calculatrice :
    mul(O, 2) == O2
else:
	# Sur Python normal :
    O * 2 == O2

CO2 + CH4 == C2O2H4

C2H4 + C == C3H4

C2H4 - C == CH4


e # 1 électron
n # 1 neutron
p # 1 proton


u # Unité de masse atomique unifiée
mol # Une mole


Me # Masse d'un électron
Mp # Masse d'un proton
Mn # Masse d'un neutron