from atomion import *

if not params.calculatrice:
    from atomion.exception import *


try: molecule = Molecule('C3O')
except Instable:
    molecule = Ion('C3O')

try: carbone = Atome('Carbone')
except ValeurIncorrecte:
    carbone = Atome('C')

try: oxygene = carbone + 2
except Incompatible:
    oxygene = carbone + Proton(2)