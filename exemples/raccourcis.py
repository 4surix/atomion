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