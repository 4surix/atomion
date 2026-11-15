# Atomion

[![CI](https://github.com/4surix/atomion/actions/workflows/ci.yml/badge.svg)](https://github.com/4surix/atomion/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/atomion)](https://pypi.org/project/atomion/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/atomion)](https://github.com/4surix/atomion/issues)
[![Download](https://img.shields.io/pypi/dm/atomion)](https://pypi.org/project/atomion/)
[![Licence](https://img.shields.io/badge/licence-AGPL--3.0--or--later-blue)](LICENSE)
![Version python](https://img.shields.io/pypi/pyversions/atomion)
![Version micropython](https://img.shields.io/badge/micropython-1.9.4-blue)

---

[Prochaine version](#prochaine-version--v19) • [Installation](#installation) • [Contribuer](#contribuer) • [Licence](#licence)

---

**Bibliothèque Python pure permettant de manipuler des atomes, ions, molécules et réactions chimiques de manière intuitive, aussi bien sur ordinateur que sur calculatrice.**

- **Syntaxe naturelle** : instanciez un atome, un ion ou une équation en une seule ligne (`H + Cl -> HCl`), presque comme sur papier.
- **Légèreté absolue** : 100 % Python pur, sans dépendance lourde (`numpy`, `scipy` ou `pandas`).
- **Compatibilité universelle** : fonctionne sur ordinateur, dans le navigateur (Pyodide / JupyterLite), sur Raspberry Pi et sur calculatrice via **MicroPython 1.9.4**.
- **Rendu scientifique riche** : affichage clair en console (configuration électronique, formules avec indices/exposants) _(et futur intégration Jupyter via `_repr_html_()`)_.
- **Approche pédagogique** : équilibrage automatique (équations, oxydo-réduction, acido-basique) et messages d'erreur explicites en français.

```python
from atomion import *

eau = Molecule('H2O')
equation = Equation('H2 + O2 -> H2O')
equation.equilibrer()
print(equation)  # 2 H₂ + O₂ -> 2 H₂O
```

<details>
  <summary>Afficher l'aperçu détaillé des fonctionnalités</summary>

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

  equation = DemiEquation('Cl2', '{Cl -}')
  equation.equilibrer()
  equation == 'Cl₂ + 2 e⁻ -> 2 Cl⁻'

  equation = Equation('H2 + O2 -> H2O')
  equation.equilibrer()
  equation == '2 H₂ + O₂ -> 2 H₂O'

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
</details>

> _**Vous trouverez un dossier [`exemples`](https://github.com/4surix/atomion/blob/master/exemples) avec les diverses fonctionnalités.**_

### Affichage

Le rendu des notations suit l'environnement : `¹²₆C`, `H₂O`, `Cl⁻` sur ordinateur,
`C`, `H2O`, `{Cl 1-}` sur calculatrice. Il peut être forcé à tout moment :

```python
from atomion import *
from atomion.utile import params

params.config(affichage = 'ascii')    # notation calculatrice
params.config(affichage = 'unicode')  # notation scientifique
```

## Prochaine version : v1.9

- [ ] **Tableau d'avancement** : génération complète (état initial, intermédiaire, final avec $x_{\max}$ et réactif limitant) adaptée à l'affichage console et calculatrice.
- [ ] **Calculs de grandeurs physiques** : masse molaire ($M$), quantité de matière ($n$), concentration massique, pH (acides/bases forts et faibles, solutions tampons) et énergie nucléaire ($\Delta m \cdot c^2$).
- [ ] **Physique nucléaire** :
  - **Fusion (`<<`)** : calcul d'énergie libérée et vérification de stabilité du noyau produit.
  - **Fission (`>>`)** : implémentation complète avec lois de Soddy et bilan énergétique.
  - **Radioactivité ($\alpha$, $\beta^+$, $\beta^-$, $\gamma$)** : désintégrations et énergie associée.
- [ ] **Mode pédagogique & pas-à-pas** : paramètre `etapes=True` pour détailler l'équilibrage des équations et réactions d'oxydo-réduction, accompagné de messages d'erreur explicites en français.
- [ ] **Acido-basique** : détection automatique du couple acide/base conjugué lorsqu'il n'est pas renseigné.
- [ ] **Chimie organique** : nomenclature IUPAC des molécules linéaires simples et affichage des formules semi-développées en ASCII (ex. : `CH3-CH2-CH2-OH` $\rightarrow$ *propan-1-ol*).
- [ ] **Assistant interactif calculatrice** : menu guidé (`atomion.menu` / `assistant()`) pour utiliser la bibliothèque sans connaître la syntaxe par cœur.

## Installation

### Prérequis

1. **Ouvrez un terminal (invite de commande).**
   <details>
     <summary>Comment faire selon votre système ?</summary>

   - **Windows :** appuyez sur `Windows` + `R`, tapez `cmd` (ou `powershell`), puis validez avec `Entrée`.
   - **macOS :** appuyez sur `Cmd` + `Espace` pour ouvrir Spotlight, tapez `Terminal`, puis validez avec `Entrée`.
   - **Linux :** appuyez sur `Ctrl` + `Alt` + `T` ou ouvrez l'application *Terminal* depuis le menu de vos applications.
   </details>

2. **Vérifiez que Python `>= 3.9` est installé.**
   <details>
     <summary>Comment vérifier ?</summary>

   Exécutez `python --version` (ou `python3 --version` sur macOS et Linux). La version affichée doit être supérieure ou égale à `3.9`.  
   Si ce n'est pas le cas, [téléchargez et installez Python](https://www.python.org/downloads/) (version 3.9 ou plus récente).
   </details>

3. **Vérifiez que `pip` est à jour.**
   <details>
     <summary>Comment vérifier ?</summary>

   Exécutez `pip --version` (ou `python -m pip --version`). La version affichée doit être supérieure ou égale à `20.0.0`.  
   Pour mettre `pip` à jour, exécutez :
   ```sh
   python -m pip install --upgrade pip
   ```
   </details>

### Sur ordinateur

1. Installez le paquet :
   ```sh
   pip install atomion
   ```
2. Pour mettre à jour le module lors d'une nouvelle version :
   ```sh
   pip install --upgrade atomion
   ```
3. Ensuite créez un nouveau fichier, importez le module, et amusez vous !
   ```python
   from atomion import *

   print(Atome('C') + Molecule('O2'))
   ```

### Sur calculatrice

Atomion est compatible avec **MicroPython 1.9.4**, utilisé sur de nombreuses calculatrices graphiques (NumWorks, TI, Casio, etc.).

1. Installez les dépendances nécessaires à la génération du fichier unique :
   ```sh
   pip install "atomion[calc]"
   ```
2. Générez le fichier autonome `atomion.py` dans la langue souhaitée :
   ```sh
   python3 -m mk_file_calculatrice --lang fr
   # Ou en anglais :
   python3 -m mk_file_calculatrice --lang en
   ```
3. Branchez votre calculatrice à votre ordinateur et copiez-y le fichier `atomion.py` généré.
4. Débranchez votre calculatrice en toute sécurité, importez `atomion` et amusez-vous !

> **Besoin d'aide ?** Si vous rencontrez un problème, consultez les [issues existantes](https://github.com/4surix/atomion/issues) ou ouvrez-en une nouvelle.

## Contribuer

```bash
# Cloner
git clone https://github.com/4surix/atomion.git
cd atomion

# Installer en mode dev
pip install -e ".[dev]"

# Lancer les tests
python -m unittest discover -s tests

# Lint
ruff check .
```

## Licence

Ce projet est distribué sous **GNU Affero General Public License v3.0 ou ultérieure** (`AGPL-3.0-or-later`).

- Texte complet : [`LICENSE`](LICENSE) - [gnu.org](https://www.gnu.org/licenses/agpl-3.0.html)
- Vous pouvez utiliser, étudier, modifier et redistribuer atomion, y compris à des fins commerciales.
- En contrepartie : tout dérivé distribué ou exposé via un réseau (site web, API, SaaS) doit rester sous AGPL et fournir son code source à ses utilisateurs.
- La mention de copyright et la licence doivent être conservées (pas de réappropriation).

Copyright (C) 2026 Asurix.