# Atomion

Module pour atomes, ions et molécules.

Vous trouverez un fichier `exemple.py` avec les diverses fonctionnalités.  
  
Petit exemple :
```python
from atomion import *

oxygene = Atome('O')
hydrogene = Atome(1)

eau = hydrogene*2 + oxygene
# Ou
eau = Molécule('H2O')

print(eau)

chlorure = Ion('Cl')

print(chlorure)
```