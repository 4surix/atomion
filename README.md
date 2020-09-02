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

# Utilisation

### Ordinateur

- Ouvrez une invite de commande.  
  <details>
    <summary>Comment faire ?</summary>

    Appuyez sur la touche `Windows` + la touche `R`, et écrivez `cmd` dans la fenêtre qui s'est ouverte.
  </details>
  
- Assurez vous d'avoir `Python >=3.6` d'installé. 
  <details>
    <summary>Comment savoir ?</summary>

    Ecrivez `python --version` dans l'invite de commande. Si Python est installé cela affichera la version qui doit être supérieur à `3.6`.
    Si ce n'est pas le cas, [installer Python](https://www.python.org/downloads/) dans une version égal ou supérieur à 3.6 pour éviter les soucis de compatibilité.
  </details>
  
- Assurez vous d'avoir `pip` d'installé. 
  <details>
    <summary>Comment savoir ?</summary>

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

- Reperez le bouton vert avec écris `Code` sur cette page et appuyez dessus.
- Cliquez sur `Download ZIP`.
- Une fois le téléchargement terminé, ouvrez le `.zip` et glissez le dossier qui se trouve à l'intérieur autre part (dans un endroit accesible).
- Ouvrez le dossier que vous avez déplacez et mettez le dossier `atomion` dans votre calculatrice (que vous aurez branchée à votre ordi via cable USB ou autre).
- Vous pouvez aussi rajoutez le fichier `exemples.py` dans votre calculatrice, cela permettra de vérifier que tout fonctionne quand vous l'executerez.
- Si vous n'avez plus rien d'autre à faire, débranchez votre calcultarive, executez le fichier `exemples.py` si vous l'avez mit, et si tout fonctionne, amusez vous !
 
# Documentation

Elle n'est pas fini, mais disponible :
- 🇫🇷 [En français](https://4surix.github.io/atomion-doc/fr/annotated.html)
- 🇪🇸 [En español](https://4surix.github.io/atomion-doc/es/annotated.html)  
  
_Fait avec [DoxyTH](https://github.com/BioTheWolff/DoxyTH)._