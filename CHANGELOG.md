# Journal des modifications

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et ce projet adhère au [versionnage sémantique](https://semver.org/lang/fr/).

## [1.8.0] - 2026-11-15

### Ajouté

- Ajout d’une configuration Dependabot (` .github/dependabot.yml`) pour les mises à jour de dépendances.
- Ajout de `__slots__` triés alphabétiquement dans les classes principales.
- Ajout complet d’annotations de type (`from __future__ import annotations`) dans l’ensemble du code.

### Modifié

- Verrouillage des actions GitHub par SHA dans `.github/workflows/ci.yml` et `.github/workflows/release.yml`.
- Chargement à la demande (`lazy loading`) du tableau périodique dans `elements.py` : passage d’une liste de dictionnaires à un format compact (tuples/chaînes) généré par `mk_file_calculatrice` lors du bundle, pour minimiser l’empreinte RAM sur les calculatrices anciennes (< 100 Ko).
- Le bundleur `mk_file_calculatrice.py` est devenu un paquet `mk_file_calculatrice/` avec point d'entrée `__main__.py` ; il s'utilise désormais via `python3 -m mk_file_calculatrice`.
- Ajustements divers dans les modules `utile/` (acido‑basique, équation, oxydo‑réduction) et nettoyage des exemples.
- Complétion des types personnalisés pour les exceptions pédagogiques (`Incompatible`, `Instable`, `ValeurIncorrecte`).

### Corrigé

- Réduction significative des erreurs `ruff` sur les classes principales.
- Resserrer configuration `ruff` : activation progressive de règles supplémentaires (dont `PTH123` → utiliser `pathlib` à la place de `open()`).

### Supprimé

- Suppression d’imports en dur dans `exemples/raccourcis.py`.

## [1.7.0] - 2026-11-14

### Ajouté

- Profil d'affichage : `params.config(affichage='unicode'|'ascii')` choisit le rendu des notations (exposants, indices, charges, accents) indépendamment du mode de calcul.
- `tests/tests_affichage.py` : verrouille les deux profils et le basculement.
- `tests/smoke_calculatrice.py` : smoke test exécuté par MicroPython 1.9.4 réel.
- `tests/tests_bundle.py` : verrouille le bundleur (extraction, aplatissement, collisions, portabilité).
- `tests/tests_calculatrice.py` : les notations du fichier unique sont comparées à celles du paquet.
- `atomion/affichage.py` : détection d'environnement, `params`, profils
  d'affichage. `utile.params` et `utile.affichage` restent valides.

### Modifié

- **Fichier unique minifié obligatoirement** : `python_minifier` (`python-minifier>=3.4,<4`, extra `atomion[calc]`) n'est plus optionnel. Il n'existe donc plus qu'un seul artefact possible, c'est lui qui est vérifié et c'est lui que teste la CI.
- Le fichier unique n'est plus vérifié *avant* minification mais **après** : c'est l'artefact livré qui est prouvé portable et exécutable.
- MicroPython 1.9.4 : support vérifié (`mpy-cross` + smoke test en CI).
- Le rendu ne dépend plus de `params.calculatrice` dans `atomion/objets/` : les objets demandent leur notation au profil actif (`atomion.affichage`, réexporté dans `utile`), via des accesseurs explicites (`nombre_de_masse`, `numero_atomique`, `indice`, `exposant`, `signe`, ...).
- `params.config(calculatrice=...)` change le profil immédiatement.
- **Génération du fichier unique réécrite et traduiten anglais** : `mk_file_calculatrice.py` recompose le paquet par analyse AST (références `utile.x` aplaties en `x`, annotations et docstrings retirées, code réservé au mode paquet écarté, collisions refusées). Le fichier obtenu est vérifié avant écriture : syntaxe, portabilité MicroPython 1.9.4 et exécution.
- `typing` standard (`from typing import ...`) dans le paquet.
- Aucun branchement d'affichage ne subsiste dans les sources : les 21 marqueurs `CAPTURE` et les remplacements de chaînes associés ont disparu.
- **Imports circulaires assainis** : les modules d'`objets` et d'`utile` se réfèrent aux classes par `objets.X`, résolu à l'appel, et non plus par `from ..objets import X`. Avec `from __future__ import annotations` (PEP 563), les annotations ne sont plus évaluées à l'import.
- `atomion.objets` ne contient plus que des réexports explicites.

### Supprimé

- Mécanisme `MAJ_TYPE` (13 fonctions, appelées en boucle depuis `objets/__init__.py`), déclarations anticipées `Atome = ... = None`, enregistrements `objets.X = X` et `objets.listes_noms`. Les noms de classes recopiés dans `atomion.utile` (`utile.Atome`, ...) sont retirés ; l'API publique reste `atomion.Atome` / `atomion.objets.Atome`.
- `couples.json` : chargeur devenu inutile (et incompatible MicroPython).
- `README-EN.md` : Documentation anglaise reportée à plus tard.
- `atomion/utile/typing.py` : devenu inutile, les annotations n'étant plus évaluées dans le fichier unique.

## [1.6.1] - 2026-11-13

### Ajouté

- Configuration de build moderne (`pyproject.toml`) et publication automatisée sur PyPI.
- Licence **AGPL-3.0-or-later**.
- Intégration continue GitHub Actions (Python 3.9 -> 3.13) + lint (`ruff`) + couverture.
- Tests dédiés : attributs, éléments, robustesse.
- Fichiers `CHANGELOG.md`, `.editorconfig`, templates GitHub.

### Corrigé

- `OxydoReduction` fonctionne avec des réactifs passés sous forme de texte.
- `DemiEquation` à un seul argument (les électrons sont désormais correctement ajoutés).
- Boucle infinie dans `AcidoBasique` lorsque les deux réactifs jouent le même rôle.
- Impossible de forcer `neutron=0` sur un atome.
- `analyse()` ne plante plus sur un `Electron`.
- Exemples corrigés (`operations.py`, `attributs.py`) et test masqué (`tests_fusions.py`).

### Modifié

- `couples.get_produit()` retourne toujours une liste de tuples `(rôle, partenaire)`.
- `params.config()` lève une erreur sur un paramètre inconnu.
- Constantes physiques : source unique de vérité (`utile`).
- Suppression de l'élément 119 (non standard) ; le tableau s'arrête à 118 (Oganesson).
- Support Python : `>=3.9` (au lieu de `>=3.6`).

## [1.6.0] - 2022-09-11

Dernière version publiée avant la reprise du projet.
