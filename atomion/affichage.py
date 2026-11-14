# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Profil d'affichage et paramètres globaux.

Toute la mise en forme des notations (exposants, indices, charges, accents)
 passe par le profil actif. Les objets gardent une référence vers l'unique
 instance d'`Affichage` : changer de profil (`params.config`) s'applique donc
 immédiatement, y compris aux objets déjà créés.
"""

from __future__ import annotations

from . import exception

from typing import Any


### Verif si calculatrice

# MicroPython fournit le module `micropython` sur tous ses ports 
#  (y compris `unix`) : c'est un signal fiable et documenté.
try:
    import micropython
except ImportError:
    is_calculatrice: bool = False
else:
    is_calculatrice: bool = True


### Paramètres

class params:
    """Paramètres globaux de l'affichage et du comportement de la bibliothèque."""

    calculatrice: bool = is_calculatrice

    langue = 'fr'

    strict = True

    nom = True
    categorie = True

    proton = True
    neutron = True
    electron = True

    masse = True
    masse_relative = True

    couches = True
    configuration = True

    def config(**params_: Any) -> None:  # noqa: ANN401
        """Configure les paramètres globaux d'affichage.

        Args:
            **params_: Paires clé/valeur des paramètres à modifier.
                La clé spéciale ``affichage`` accepte ``'unicode'`` ou ``'ascii'``.
        """
        if 'affichage' in params_:
            mode = params_.pop('affichage')
            if mode not in ('unicode', 'ascii'):
                raise exception.ValeurIncorrecte(
                    "L'affichage doit valoir 'unicode' ou 'ascii'."
                )
            params_['calculatrice'] = (mode == 'ascii')

        for key, valeur in params_.items():
            if not hasattr(params, key):
                raise exception.ValeurIncorrecte(
                    "Le paramètre '%s' n'existe pas." % key
                )
            setattr(params, key, valeur)

        definir_affichage(params.calculatrice)


### Caractères

exposants: tuple[str, ...] = tuple('⁰¹²³⁴⁵⁶⁷⁸⁹')
sous_exposants: tuple[str, ...] = tuple('₀₁₂₃₄₅₆₇₈₉')


### Profil d'affichage

class Profil:
    """Mise en forme des notations (classe de base, a specialiser)."""

    def nombre_de_masse(self, valeur: int) -> str:
        """Rendu du nombre de masse (A), au-dessus du symbole : `12` dans `¹²₆C`."""
        raise NotImplementedError

    def numero_atomique(self, valeur: int) -> str:
        """Rendu du numero atomique (Z), sous le symbole : `6` dans `¹²₆C`."""
        raise NotImplementedError

    def indice(self, valeur: int) -> str:
        """Indice de formule (nombre d'atomes dans une molecule)."""
        raise NotImplementedError

    def exposant(self, valeur: int) -> str:
        """Exposant (electrons d'une couche, configuration electronique)."""
        raise NotImplementedError

    def nombre_indice(self, nombre: int) -> str:
        """Indice de formule, omis lorsque le nombre vaut 1."""
        raise NotImplementedError

    def facteur(self, nombre: int) -> str:
        """Multiplicite d'une charge (1 -> omise en Unicode)."""
        raise NotImplementedError

    def signe(self, symbole: str) -> str:
        """Symbole d'une charge : '-' , '+' ou '0' (neutre)."""
        raise NotImplementedError

    def encadrement(self, actif: bool) -> tuple[str, str, str]:
        """Retourne `(ouvrant, separateur, fermant)` autour de la charge."""
        raise NotImplementedError

    def sans_accents(self, texte: str) -> str:
        """Texte des descriptions (accents retires si necessaire)."""
        raise NotImplementedError


class ProfilUnicode(Profil):
    """Profil d'affichage Unicode (caractères spéciaux exposants/indices)."""

    def exposant(self, valeur: int) -> str:
        """Rendu d'un exposant Unicode."""
        return ''.join(exposants[int(num)] for num in str(valeur))

    def indice(self, valeur: int) -> str:
        """Rendu d'un indice Unicode."""
        return ''.join(sous_exposants[int(num)] for num in str(valeur))

    nombre_de_masse = exposant
    numero_atomique = indice

    def nombre_indice(self, nombre: int) -> str:
        """Indice de formule Unicode, omis lorsque le nombre vaut 1."""
        return '' if nombre == 1 else self.indice(nombre)

    def facteur(self, nombre: int) -> str:
        """Facteur de charge Unicode, omis lorsque le nombre vaut 1."""
        return '' if nombre == 1 else self.exposant(nombre)

    def signe(self, symbole: str) -> str:
        """Symbole de charge Unicode."""
        return {'-': '⁻', '+': '⁺', '0': '⁰'}[symbole]

    def encadrement(self, actif: bool) -> tuple[str, str, str]:
        """Encadrement de charge Unicode (aucun)."""
        return ('', '', '')

    def sans_accents(self, texte: str) -> str:
        """Retourne le texte inchangé (Unicode conserve les accents)."""
        return texte


class ProfilAscii(Profil):
    """Profil d'affichage ASCII (calculatrices, caractères simples)."""

    def nombre_de_masse(self, valeur: int) -> str:
        """Nombre de masse ASCII (vide sur calculatrice)."""
        # Les caractères spéciaux ne sont pas disponibles sur la calculatrice,
        #  la notation du nucleide (`¹²₆C`) est omise,
        #  le symbole seul suffit (`C`).
        return ''

    def numero_atomique(self, valeur: int) -> str:
        """Numéro atomique ASCII (vide sur calculatrice)."""
        return ''

    def indice(self, valeur: int) -> str:
        """Indice de formule ASCII."""
        return str(valeur)

    def exposant(self, valeur: int) -> str:
        """Exposant ASCII."""
        return str(valeur)

    def nombre_indice(self, nombre: int) -> str:
        """Indice de formule ASCII, omis lorsque le nombre vaut 1."""
        return '' if nombre == 1 else str(nombre)

    def facteur(self, nombre: int) -> str:
        """Facteur de charge ASCII."""
        return str(nombre)

    def signe(self, symbole: str) -> str:
        """Symbole de charge ASCII."""
        return {'-': '-', '+': '+', '0': ''}[symbole]

    def encadrement(self, actif: bool) -> tuple[str, str, str]:
        """Encadrement de charge ASCII (accolades si calculatrice)."""
        return ('{', ' ', '}') if actif else ('', '', '')

    def sans_accents(self, texte: str) -> str:
        """Supprime les accents d'un texte pour l'affichage ASCII."""
        return texte.replace('è', 'e').replace('é', 'e')


class Affichage:
    """Profil d'affichage actif.

    Les objets conservent une reference vers cette instance.
    Changer de profil remplace simplement son `profil` interne,
     sans casser les references deja prises.
    """

    def __init__(self, profil: Profil) -> None:
        """Initialise l'affichage avec un profil donné.

        Args:
            profil: Instance de Profil à utiliser pour le rendu.
        """
        self.profil = profil

    def definir(self, profil: Profil) -> None:
        """Change le profil d'affichage actif.

        Args:
            profil: Nouvelle instance de Profil à utiliser.
        """
        self.profil = profil

    def __getattr__(self, nom: str) -> Any:  # noqa: ANN401
        """Redirige l'accès aux attributs vers le profil actif."""
        if nom == 'profil':
            raise AttributeError(nom)
        return getattr(self.profil, nom)


affichage: Affichage = Affichage(
    ProfilAscii() if is_calculatrice else ProfilUnicode()
)


def definir_affichage(calculatrice: bool) -> None:
    """Selectionne le profil d'affichage et synchronise `params.calculatrice`."""

    params.calculatrice = bool(calculatrice)

    affichage.definir(
        ProfilAscii() if params.calculatrice else ProfilUnicode()
    )
