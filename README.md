- [Atomion](https://github.com/4surix/atomion#atomion)
- [Aperçu](https://github.com/4surix/atomion#aper%C3%A7u)
- [Prochainement](https://github.com/4surix/atomion#prochainement)
- [Installer](https://github.com/4surix/atomion#installer)
- [Documentation](https://github.com/4surix/atomion#documentation)

# Atomion

[![Build Status](https://travis-ci.com/4surix/atomion.svg?branch=master)](https://travis-ci.com/4surix/atomion)
[![PyPI](https://img.shields.io/pypi/v/atomion)](https://pypi.org/project/atomion/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/atomion)](https://github.com/4surix/atomion/issues)

Module servant à manipuler facilement des atomes, ions _(monoatomiques/polyatomiques)_ et molécules.  
  
Vous trouverez un fichier [`exemples.py`](https://github.com/4surix/atomion/blob/master/exemples.py) avec les diverses fonctionnalités.  
  
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

print(eau)
```
Pour voir le reste des fonctionnalités, regardez le fichier [`exemples.py`](https://github.com/4surix/atomion/blob/master/exemples.py).

# Prochainement
  
### v1.3.0
- Ajout quarks (up et down).
- Ajout objet Noyau.
    - Contiendra objet `Proton` et `Neutron`.
    - S'additionnera aux objets Electron pour former des atomes/ions.

### v1.4.0
- Ajout fusion nucléaire.
- Ajout fission nucléaire.

# Installer

### Ordinateur

- Ouvrez une invite de commande.  
  <details>
    <summary>Comment faire ?</summary>

    Appuyez sur la touche `Windows` + la touche `R`, et écrivez `cmd` dans la fenêtre qui s'est ouverte.
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

    Ecrivez `pip --version` dans l'invite de commande. Si `pip` est installé cela affichera la version qui doit être supérieur à `10.0.0`.  
    Si ce n'est pas le cas, écrivez `python -m pip install --upgrade pip` pour mettre à jour.
  </details>
  
- Ecrivez la commande suivante :  
    ```sh
    pip install atomion
    ```
  
- L'ors de nouvelle mise à jour il suffira de rajouter `--upgrade` pour mettre le module à jour : 
    ```sh
    pip install atomion --upgrade
    ```

- Ensuite créez un nouveau fichier, importez le module, et amusez vous !
    ```python
    from atomion import *

    print(Atome('C') + Molecule('O2'))
    ```

### Calculatrice

_**Attention**, pour les calculatrices qui ne peuvent pas avoir de dossiers, il n'est pas possible d'utiliser le module, mais une version en un seul fichier est en cours pour que vous puissiez l'utiliser._

- Repérez le bouton vert avec écrit "Code" sur cette page et appuyez dessus.
- Cliquez sur `Download ZIP`.
- Une fois le téléchargement terminé, ouvrez le `.zip` et glissez le dossier qui se trouve à l'intérieur autre part (dans un endroit accessible).
- Ouvrez le dossier que vous avez déplacé et mettez le dossier `atomion` dans votre calculatrice _(que vous aurez branchée à votre ordi via câble USB ou autre)_.
- Vous pouvez aussi rajouter le fichier `exemples.py` dans votre calculatrice, cela permettra de vérifier que tout fonctionne quand vous l'exécuterez.
- Si vous n'avez plus rien d'autre à faire, débranchez votre calculatrice, exécutez le fichier `exemples.py` si vous l'avez mis, et si tout fonctionne, amusez-vous !
 
# Documentation

Elle n'est pas fini, mais disponible :
- 🇫🇷 [En français](https://4surix.github.io/atomion-doc/fr/annotated.html)
- 🇪🇸 [En español](https://4surix.github.io/atomion-doc/es/annotated.html)  
  
_Fait avec [DoxyTH](https://github.com/BioTheWolff/DoxyTH)._