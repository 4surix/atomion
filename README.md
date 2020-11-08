- [Atomion](https://github.com/4surix/atomion#atomion)
- [Aperçu](https://github.com/4surix/atomion#aper%C3%A7u)
- [Installer](https://github.com/4surix/atomion#installer)
- [Licence](https://github.com/4surix/atomion#licence)

# Atomion

[![Build Status](https://travis-ci.com/4surix/atomion.svg?branch=master)](https://travis-ci.com/4surix/atomion)
[![PyPI](https://img.shields.io/pypi/v/atomion)](https://pypi.org/project/atomion/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/atomion)](https://github.com/4surix/atomion/issues)
[![Download](https://img.shields.io/pypi/dm/atomion)](https://pypi.org/project/atomion/)
![Version python](https://img.shields.io/pypi/pyversions/atomion)
![Code size](https://img.shields.io/github/languages/code-size/4surix/atomion)
![Code size file](https://img.shields.io/badge/code%20size%20file%20calc-34%20kB-blue)

Module servant à manipuler facilement :
- Quark
- Proton, Neutron, Electron
- Noyau
- Atome
- Ion _(monoatomique/polyatomique)_
- Molécule
- Equation chimique
- Réaction chimique
##### Prochainement
- Fusion nucléaire
- Fission nucléaire
- Gluons
- Antimatière

Vous trouverez un dossier [`exemples`](https://github.com/4surix/atomion/blob/master/exemples) avec les diverses fonctionnalités.

Le module est compatible avec `Micro Python 1.9.4`, donc aussi pour les calculatrices !

# Aperçu

```python
from atomion import *

oxygene = Atome('O') # Avec symbole
hydrogene = Atome(1) # Avec nombre proton

eau = hydrogene * 2 + oxygene
# Ou
eau = Molecule('H2O')

chlorure = Ion('Cl')
# Ou
chlorure = IonMonoAtomique('Cl')

carbonate = Ion('CO3')
# Ou
carbonate = IonPolyAtomique('CO3')

equation = Equation('Cu + O2 -> CuO')
equation.equilibrer()
equation == '2 Cu + O₂ -> 2 CuO'

reaction = Reaction(
    equation = equation,
    quantites_reactifs = {
        Atome('Cu'): 1.6,
        Molecule('O2'): 1.3
    }
)
reaction.final() == {
    Atome('Cu'): 0.0,
    Molecule('O2'): 0.5,
    Molecule('CuO'): 1.6
}

from atomion.raccourcis import *

eau = H * 2 + O
# Ou
eau = H2O
```

Pour voir le reste des fonctionnalités, regardez le dossier [`exemples`](https://github.com/4surix/atomion/blob/master/exemples).

# Installer

### Ordinateur

- Ouvrez une invite de commande.
  <details>
    <summary>Comment faire ?</summary>

  Sur Windows, appuyez sur la touche `Windows` + la touche `R`, et écrivez `cmd` dans la fenêtre qui s'est ouverte.
  </details>

- Assurez-vous d'avoir `Python >=3.6` d'installé.
  <details>
    <summary>Comment savoir ?</summary>

  Ecrivez `python --version` dans l'invite de commande. Si Python est installé cela affichera la version qui doit être supérieur à `3.6`.
  Si ce n'est pas le cas, [installer Python](https://www.python.org/downloads/) dans une version égal ou supérieur à 3.6 pour éviter les soucis de compatibilité.
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

Je ne sais pas quelle licence mettre.  
Tout ce que je veux c'est que tout le monde puisse l'utiliser gratuitement et librement que cela soit pour le privé, dans leur projet publique, à but éducatif ; mais je ne veux pas qu'une personne : puisse se faire de l'argent avec le projet atomion, prétend que le code du projet atomion soit le sien et pas le mien, ne cite pas le projet atomion dans leur projet.