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

from . import exception


### Verif si calculatrice

# MicroPython fournit le module `micropython` sur tous ses ports 
#  (y compris `unix`) : c'est un signal fiable et documenté.
try:
    import micropython
except ImportError:
    is_calculatrice = False
else:
    is_calculatrice = True


### Paramètres

class params:
    calculatrice = is_calculatrice

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

    def config(**params_):
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

exposants = tuple('⁰¹²³⁴⁵⁶⁷⁸⁹')
sous_exposants = tuple('₀₁₂₃₄₅₆₇₈₉')


### Profil d'affichage

class Profil:
    """Mise en forme des notations (classe de base, a specialiser)."""

    def nombre_de_masse(self, valeur):
        """Rendu du nombre de masse (A), au-dessus du symbole : `12` dans `¹²₆C`."""
        raise NotImplementedError

    def numero_atomique(self, valeur):
        """Rendu du numero atomique (Z), sous le symbole : `6` dans `¹²₆C`."""
        raise NotImplementedError

    def indice(self, valeur):
        """Indice de formule (nombre d'atomes dans une molecule)."""
        raise NotImplementedError

    def exposant(self, valeur):
        """Exposant (electrons d'une couche, configuration electronique)."""
        raise NotImplementedError

    def nombre_indice(self, nombre):
        """Indice de formule, omis lorsque le nombre vaut 1."""
        raise NotImplementedError

    def facteur(self, nombre):
        """Multiplicite d'une charge (1 -> omise en Unicode)."""
        raise NotImplementedError

    def signe(self, symbole):
        """Symbole d'une charge : '-' , '+' ou '0' (neutre)."""
        raise NotImplementedError

    def encadrement(self, actif):
        """Retourne `(ouvrant, separateur, fermant)` autour de la charge."""
        raise NotImplementedError

    def sans_accents(self, texte):
        """Texte des descriptions (accents retires si necessaire)."""
        raise NotImplementedError


class ProfilUnicode(Profil):

    def exposant(self, valeur):
        return ''.join(exposants[int(num)] for num in str(valeur))

    def indice(self, valeur):
        return ''.join(sous_exposants[int(num)] for num in str(valeur))

    nombre_de_masse = exposant
    numero_atomique = indice

    def nombre_indice(self, nombre):
        return '' if nombre == 1 else self.indice(nombre)

    def facteur(self, nombre):
        return '' if nombre == 1 else self.exposant(nombre)

    def signe(self, symbole):
        return {'-': '⁻', '+': '⁺', '0': '⁰'}[symbole]

    def encadrement(self, actif):
        return ('', '', '')

    def sans_accents(self, texte):
        return texte


class ProfilAscii(Profil):

    def nombre_de_masse(self, valeur):
        # Les caractères spéciaux de sont pas disponible sur la calculatrice,
        #  la notation du nucleide (`¹²₆C`) est omise,
        #  le symbole seul suffit (`C`).
        return ''

    def numero_atomique(self, valeur):
        return ''

    def indice(self, valeur):
        return str(valeur)

    def exposant(self, valeur):
        return str(valeur)

    def nombre_indice(self, nombre):
        return '' if nombre == 1 else str(nombre)

    def facteur(self, nombre):
        return str(nombre)

    def signe(self, symbole):
        return {'-': '-', '+': '+', '0': ''}[symbole]

    def encadrement(self, actif):
        return ('{', ' ', '}') if actif else ('', '', '')

    def sans_accents(self, texte):
        return texte.replace('è', 'e').replace('é', 'e')


class Affichage:
    """Profil d'affichage actif.

    Les objets conservent une reference vers cette instance.
    Changer de profil remplace simplement son `profil` interne, 
     sans casser les references deja prises.
    """

    def __init__(self, profil):
        self.profil = profil

    def definir(self, profil):
        self.profil = profil

    def __getattr__(self, nom):
        if nom == 'profil':
            raise AttributeError(nom)
        return getattr(self.profil, nom)


affichage = Affichage(ProfilAscii() if is_calculatrice else ProfilUnicode())


def definir_affichage(calculatrice):
    """Selectionne le profil d'affichage et synchronise `params.calculatrice`."""

    params.calculatrice = bool(calculatrice)

    affichage.definir(
        ProfilAscii() if params.calculatrice else ProfilUnicode()
    )
