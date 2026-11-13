# Journal des modifications

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et ce projet adhère au [versionnage sémantique](https://semver.org/lang/fr/).

## [Non publié]

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
