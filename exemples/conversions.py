from atomion import *


# Convertire un atome en ion
cuivre = Atome('Cu')
ion_cuivre = Ion(cuivre)

# Convertire un ion en atome
ion_cuivre = Ion('Cu')
cuivre = Atome(ion_cuivre)