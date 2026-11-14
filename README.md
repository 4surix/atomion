- [Atomion](https://github.com/4surix/atomion#atomion)
- [Aperçu](https://github.com/4surix/atomion#aper%C3%A7u)
- [Installer](https://github.com/4surix/atomion#installer)
- [Licence](https://github.com/4surix/atomion#licence)

# Atomion

[![CI](https://github.com/4surix/atomion/actions/workflows/ci.yml/badge.svg)](https://github.com/4surix/atomion/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/atomion)](https://pypi.org/project/atomion/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/atomion)](https://github.com/4surix/atomion/issues)
[![Download](https://img.shields.io/pypi/dm/atomion)](https://pypi.org/project/atomion/)
[![Licence](https://img.shields.io/badge/licence-AGPL--3.0--or--later-blue)](LICENSE)
![Version python](https://img.shields.io/pypi/pyversions/atomion)
![Version micropython](https://img.shields.io/badge/micropython-1.9.4-blue)

Module servant à manipuler facilement :
- Quark
- Proton, Neutron, Electron
- Noyau
- Atome
- Ion _(monoatomique/polyatomique)_
- Molécule
- Equation chimique
- Réaction chimique
- Demi-équation
- Oxydo-réduction
- Électronégativité
- Molécule organique
- Reaction acido-basique
##### Prévues :
- _Fusion nucléaire (Non-fini)_
- Fission nucléaire
- Gluons
- Antimatière
- Maintien des liaisons

Vous trouverez un dossier [`exemples`](https://github.com/4surix/atomion/blob/master/exemples) avec les diverses fonctionnalités.

Le module est compatible avec `Micro Python 1.9.4`, donc aussi pour les calculatrices !

# Aperçu

```python
from atomion import *

oxygene = Atome('O') # Avec symbole
hydrogene = Atome(1) # Avec nombre proton

chlorure = Ion('Cl')
# Ou
chlorure = IonMonoAtomique('Cl')

carbonate = Ion('CO3')
# Ou
carbonate = Ion('{CO3 2-}')
# Ou
carbonate = IonPolyAtomique('CO3')


eau = hydrogene * 2 + oxygene
# Ou
eau = Molecule('H2O')

from atomion.raccourcis import *

eau = H * 2 + O
# Ou
eau = H2O


# Quark
proton = QUp('R') + QDown('B') + QUp('V')
neutron = QUp('R') + QDown('B') + QDown('V')


# Fusion
noyauH = Noyau(Proton(1), Neutron(1))
noyauHe, *particules = noyauH << noyauH
atomeHe = noyauHe + Electron(2)


equation = Equation('H2 + O2 -> H2O')
equation.equilibrer()
equation == '2 H₂ + O₂ -> 2 H₂O'

equation = DemiEquation('Cl2', '{Cl -}')
equation.equilibrer()
equation == 'Cl₂ + 2 e⁻ -> 2 Cl⁻'


reaction = Reaction(
    equation = equation,
    quantites_reactifs = {H2: 1.6, O2: 1.3}
)
reaction.final() == {H2: 0, O2: 0.5, H2O: 1.6}

oxydoR = OxydoReduction(
    Ion('{Cr2O7 2-}'),
    Atome('Fe')
)
oxydoR.don == 'Fe -> Fe²⁺ + 2 e⁻'
oxydoR.gain == 'Cr₂O₇²⁻ + 14 H⁺ + 6 e⁻ -> 2 Cr³⁺ + 7 H₂O'

reaction = AcidoBasique('{C3H5O2 -}', '{H3O +}')
reaction.gain == 'C₃H₅O₂⁻ + H⁺ -> C₃H₆O₂'
reaction.don ==  'H₃O⁺ -> H₂O + H⁺'
reaction.equation == 'H₃O⁺ + C₃H₅O₂⁻ -> H₂O + C₃H₆O₂'
```

### Affichage

Le rendu des notations suit l'environnement : `¹²₆C`, `H₂O`, `Cl⁻` sur ordinateur,
`C`, `H2O`, `{Cl 1-}` sur calculatrice. Il peut être forcé à tout moment :

```python
from atomion import *
from atomion.utile import params

params.config(affichage = 'ascii')    # notation calculatrice
params.config(affichage = 'unicode')  # notation scientifique
```

_(`params.config(calculatrice = True)` équivaut à `affichage = 'ascii'` : c'est ce mode qui est actif dans le fichier unique destiné aux calculatrices.)_

Pour voir le reste des fonctionnalités, regardez le dossier [`exemples`](https://github.com/4surix/atomion/blob/master/exemples).

# Installer

### Ordinateur

- Ouvrez une invite de commande.
  <details>
    <summary>Comment faire ?</summary>

  Sur Windows, appuyez sur la touche `Windows` + la touche `R`, et écrivez `cmd` dans la fenêtre qui s'est ouverte.
  </details>

- Assurez-vous d'avoir `Python >=3.9` d'installé.
  <details>
    <summary>Comment savoir ?</summary>

  Ecrivez `python --version` dans l'invite de commande. Si Python est installé cela affichera la version qui doit être supérieur à `3.9`.
  Si ce n'est pas le cas, [installer Python](https://www.python.org/downloads/) dans une version égal ou supérieur à 3.9 pour éviter les soucis de compatibilité.
  </details>

- Vérifiez que `pip` est installé.
  <details>
    <summary>Comment vérifier ?</summary>

  Ecrivez `pip --version` dans l'invite de commande. Si `pip` est installé cela affichera la version qui doit être supérieur à `20.0.0`.  
   Si ce n'est pas le cas, écrivez `python -m pip install --upgrade pip` pour mettre à jour.
  </details>

- Ecrivez la commande suivante :
  ```sh
  pip install atomion
  ```
- Lors de nouvelle mise à jour il suffira de rajouter `--upgrade` pour mettre le module à jour :

  ```sh
  pip install atomion --upgrade
  ```

- Ensuite créez un nouveau fichier, importez le module, et amusez vous !

  ```python
  from atomion import *

  print(Atome('C') + Molecule('O2'))
  ```

### Calculatrice

- [Téléchargez le code.](https://github.com/4surix/atomion/archive/master.zip)
- Ouvrez le `.zip` et glissez le dossier qui se trouve à l'intérieur autre part (dans un endroit accessible).
- Ouvrez le dossier que vous avez déplacé et executer le fichier `mk_file_calculatrice.py`.
- Un fichier `atomion.py` va se créer, mettez le dans votre calculatrice _(que vous aurez branchée à votre ordi via câble USB ou autre)_.
- Si vous n'avez plus rien d'autre à faire, débranchez votre calculatrice et amusez-vous !
  
Si le fichier est trop grand, installer [`python_minifier`](https://pypi.org/project/python-minifier/) (`pip install python-minifier`), et recréer le fichier.  
  
Si vous avez un problème, n'hésitez pas à regarder les [issues](https://github.com/4surix/atomion/issues) déjà exitantes ou à en ouvrir une.  

# Licence

Ce projet est distribué sous **GNU Affero General Public License v3.0 ou ultérieure** (`AGPL-3.0-or-later`).

- Texte complet : [`LICENSE`](LICENSE) - [gnu.org](https://www.gnu.org/licenses/agpl-3.0.html)
- Vous pouvez utiliser, étudier, modifier et redistribuer atomion, y compris à des fins commerciales.
- En contrepartie : tout dérivé distribué ou exposé via un réseau (site web, API, SaaS) doit rester sous AGPL et fournir son code source à ses utilisateurs.
- La mention de copyright et la licence doivent être conservées (pas de réappropriation).

Copyright (C) 2026 Asurix.