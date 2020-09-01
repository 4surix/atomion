# Atomion

Module pour atomes, ions et molécules.  
  
- 🇫🇷 [Documentation en français !](https://4surix.github.io/atomion-doc/FR/annotated.html)
- 🇪🇸 [Documentacion en español !](https://4surix.github.io/atomion-doc/ES/annotated.html)
  
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

print(chlorure)

from atomion.raccourcis import *

eau = H * 2 + O
# ou
eau = H2O

print(eau)
```