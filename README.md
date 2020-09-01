# Atomion

Module pour atomes, ions _(monoatomiques/polyatomiques)_ et molécules.  
  
Vous trouverez un fichier `exemple.py` avec les diverses fonctionnalités.  
  
Le module est compatible avec `Micro Python 1.9.4`, donc aussi pour les calculatrices !  
  
# Aperçu

```python
from atomion import *

oxygene = Atome('O')
hydrogene = Atome(1)

eau = hydrogene * 2 + oxygene
# Ou
eau = Molecule('H2O')

print(eau)

chlorure = Ion('Cl')
carbonate = Ion('CO3')

print(chlorure)
print(carbonate)

from atomion.raccourcis import *

eau = H * 2 + O
# ou
eau = H2O

print(eau)
```

# Documentation

Elle n'est pas fini, mais disponible :
- 🇫🇷 [En français](https://4surix.github.io/atomion-doc/fr/annotated.html)
- 🇪🇸 [En español](https://4surix.github.io/atomion-doc/es/annotated.html)  
  
_Fait avec [DoxyTH](https://github.com/BioTheWolff/DoxyTH)._