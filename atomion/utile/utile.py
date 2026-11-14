# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from .. import exception, irregularites, objets
from ..elements import elements
from ..objets import Atome, Ion, IonMonoAtomique, Molecule
from .typing import *

###>>> CAPTURE FICHIER CALC

### Verif si calculatrice

# MicroPython fournit le module `micropython` sur tous ses ports 
#  (y compris `unix`) : c'est un signal fiable et documenté.
try:
    import micropython
except ImportError:
    is_calculatrice = False
else:
    is_calculatrice = True


if is_calculatrice:

    def mul(inicial, *elements):
        for element in elements:
            inicial = inicial.__mul__(element)
        return inicial


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


### Valeur de base pour les calculs

u = 1.660538921*(10**-27)

masse_electron = 9.109*(10**-31)
masse_proton = 1.672649*(10**-27)
masse_neutron = 1.67493*(10**-27)

# Alias des masses, utilisés par `raccourcis` (source unique de vérité).
# `Mn` n'est pas défini ici : ce symbole est réservé au Manganèse.
Me = masse_electron
Mp = masse_proton

mol = 6.02214076*(10**23)


### Fonctions

## Séparées par couche, récupérants la configuration d'un ion

fonctions_configuration_ion = (
    lambda c: ([c if c <= 2 else 2], c-2),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2 if c <= 8 else 6], c-8),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2], c-8) if c <= 8
            else
                ([2, 6, c-8 if c <= 18 else 10], c-18),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2], c-8) if c <= 8
            else
                ([2, 6, c-8], c-18) if c <= 18
                else
                    ([2, 6, 10, c-18 if c <= 32 else 14], c-32),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2], c-8) if c <= 8
            else
                ([2, 6, c-8], c-18) if c <= 18
                else
                    ([2, 6, 10, c-18], c-32) if c <= 32
                    else
                        ([2, 6, 10, 14, c-32 if c <= 50 else 18], c-50),
)

## Séparées par couche, récupérants la configuration d'un atome

fonctions_configuration_atome = (
    lambda c: ([c if c <= 2 else 2], c-2),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2 if c <= 8 else 6], c-8),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2 if c <= 8 else 6], c-8),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2], c-12) if c <= 12
            else
                ([2, 10, c-12 if c <= 18 else 6], c-18),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2], c-12) if c <= 12
            else
                ([2, 10, c-12 if c <= 18 else 6], c-18),
    lambda c:
        ([c], c-2) if c <= 2
        else
            ([2, c-2], c-16) if c <= 16
            else
                ([2, 14, c-16], c-26) if c <= 26
                else
                    ([2, 14, 10, c-26 if c <= 32 else 6], c-32)
)

fonctions_get = {
    # electron(s) = (
    #   Masse de l'Atome - (
    #       Masse des protons + Masse des neutrons
    #   )
    # ) / Masse d'un eletron
    'electron': lambda obj: round(
        (
            obj.masse_atomique_relative * u
            - (
                (masse_neutron * obj.neutron)
                + (masse_proton * obj.proton)
            )
        ) / masse_electron
    ),

    # Proton(s) = (
    #   Masse de l'Atome - (
    #       Masse des electrons + Masse des neutrons
    #   )
    # ) / Masse d'un proton
    'proton': lambda obj: round(
        (
            obj.masse_atomique_relative * u
            - (
                (masse_electron * obj.electron)
                + (masse_neutron * obj.neutron)
            )
        ) / masse_proton
    ),

    # Neuton(s) = (
    #   Masse de l'Atome - (
    #       Masse des electrons + Masse des protons
    #   )
    # ) / Masse d'un neutron
    'neutron': lambda obj: round(
        (
            obj.masse_atomique_relative * u
            - (
                (masse_electron * obj.electron)
                + (masse_proton * obj.proton)
            )
        ) / masse_neutron
    ),
}


### Notations

notation_configuration_ion = (
    '1s','2s','2p','3s','3p','3d','4s','4p','4d','4f','5s','5p','5d','5f','5g'
)

notation_configuration_atome = (
    '1s','2s','2p','3s','3p','4s','3d','4p','5s','4d','5p','6s','4f','5d',
    '6p', '7s','5f','6d','7p'
)

notations_couche = (
    'K','L','M','N','O','P'
)

exposants = tuple('⁰¹²³⁴⁵⁶⁷⁸⁹')
sous_exposants = tuple('₀₁₂₃₄₅₆₇₈₉')


### Profil d'affichage
#
# Toute la mise en forme des notations (exposants, indices, charges, accents)
#  passe par ici. Deux profils :
#  - ProfilUnicode : notation scientifique (¹²₆C, H₂O, Cl⁻)
#  - ProfilAscii   : notation compatible calculatrices ({Cl 1-}, H2O)
#
#  Le profil est choisi automatiquement (MicroPython -> ASCII) et peut etre
#  force : `params.config(affichage='unicode')` ou `affichage='ascii'`.


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


### Utilitaire

def configuration_electronique(element:Union[Atome, Ion]) -> List[int]:
    """

    Génére la configuration électronique d'un atome/ion.

    ---------
    Arguments

    element
        :Atome
        :Ion

    -------
    Retours
 
    :list
        Liste contenant le nombre d'électron par couche.
    """

    couches = []

    electrons = element.electron
    protons = element.proton

    if isinstance(element, Atome):
        fonctions = fonctions_configuration_atome
    elif isinstance(element, IonMonoAtomique):
        fonctions = fonctions_configuration_ion


    for i in range(5):
        couche, electrons = fonctions[i](electrons)
        couches.extend(couche)

        if electrons <= 0:
            break


    irregularite = irregularites.configuration.get(protons)

    if irregularite:
        couches[-len(irregularite):] = irregularite

    return couches


def get_info(
        obj:Union[Atome, Ion],
        valeur:Union[str, int, Ion, Atome]
    ) -> None:
    """

    Récupére les informations d'un atome grâce à son nombre de proton
      ou son symbole.

    ---------
    Arguments

    obj
        :Atome
        :Ion

    valeur
        :str
            Récupérer les infos suivant le symbole indiqué
        :int
            Récupérer les infos suivant le nombre de proton indiqué
        :Ion
            Récupérer les infos suivant le nombre de proton de l'ion,
            Pour la conversation Ion -> Atome
        :Atome
            Récupérer les infos suivant le nombre de proton de l'atome,
            Pour la conversation Atome -> Ion


    -------
    Retours

    None
    """

    if isinstance(valeur, type(obj)):
        raise exception.ValeurIncorrecte(
            "Cette objet est déjà un '%s' !" % type(obj)
        )

    elif isinstance(valeur, (IonMonoAtomique, Atome)):

        obj.proton = valeur.proton
        obj.neutron = valeur.neutron

    elif isinstance(valeur, int):

        if valeur > len(elements):
            raise exception.ValeurIncorrecte(
                "Le nombre de proton doit exister !"
            )
        elif valeur <= 0:
            raise exception.ValeurIncorrecte(
                "Le nombre de proton doit être superieur à zero !"
            )
        else:
            obj.proton = valeur

    elif isinstance(valeur, str):

        obj.proton = None

        proton = 1

        valeur = valeur.strip()

        for element in elements:
            if element['symbol'] == valeur:
                obj.proton = proton
                break
            proton += 1

        if not obj.proton:
            raise exception.ValeurIncorrecte(
                "Le symbole '%s'" % valeur
                + "ne correspond à aucun élément existant !"
            )


    element = elements[obj.proton-1]

    (
        obj.nom,
        obj.symbole,
        obj.categorie,
        obj.couches,
        obj.masse_atomique_relative,
        obj.electronegativite

        ) = (

        element['name'],
        element['symbol'],
        element['category'],
        element['shells'][:],
        element['atomic_mass'],
        element['electronegativity_pauling']
    )


def get_value(item:str, obj:Union[Atome, Ion]) -> int:
    """

    Recupere une valeur d'un item.

    ---------
    Arguments

    item
        :str
            'electron'
                Récupére les électrons de l'objet
            'proton'
                Récupére les protons de l'objet
            'neutron'
                Récupére les neutrons de l'objet

    obj
        :Atome
        :Ion

    -------
    Retours

    Cela depend.
    """
    return fonctions_get.get(item, lambda x:None)(obj)


def get_masse(obj:Union[Atome, Ion]) -> float:
    """

    Récupére la masse de l'objet.

    ---------
    Arguments

    obj
        :Atome
        :Ion

    -------
    Retours

    :float
        Masse de l'objet.
    """
    return (
        (obj.proton*masse_proton)
        + (obj.neutron*masse_neutron)
        + (obj.electron*masse_electron)
    )


def convertie_notation(notation:str) -> Union[Ion, Molecule, Atome]:

    if '{' == notation[0] and notation[-1] == '}':
        return Ion(notation)

    else:
        try: return Molecule(notation, verif_stable=False)
        except exception.ValeurIncorrecte:
            return Atome(notation)


def convertie_notation_vers(
        type_obj:str, data:str
    ) -> List[Union[Ion, Atome]]:
    """
    Transforme un str en list d'atomes
    """

    element = ''
    elements = []
    nbr = ''

    in_molecule = False

    chiffres = list('0123456789')

    if type_obj == 'atomes':
        type_obj = Atome
    elif type_obj == 'ions':
        type_obj = IonMonoAtomique


    for carac in data.strip():

        if carac == ')':
            # in_molecule == ['C', 'O', '2'] -> in_molecule == 'CO2'
            in_molecule = ''.join(in_molecule)


        elif isinstance(in_molecule, list):
            # (CO2)3 -> in_molecule == ['C', 'O', '2']
            in_molecule.append(carac)


        elif carac == '(':

            if element:
                # CO2(H2)
                #    ^
                elements.extend(
                    [type_obj(element)] * (int(nbr) if nbr else 1)
                )
                element = ''
                nbr = ''

            if isinstance(in_molecule, str):
                # CO2(H2)4(Ag7)2
                #         ^
                elements.extend(
                    convertie_notation_vers(type_obj, in_molecule)
                    * (int(nbr) if nbr else 1)
                )
                nbr = ''

            in_molecule = []


        elif carac.isupper():

            if in_molecule:
                # (H2)2Ca
                #      ^
                elements.extend(
                    convertie_notation_vers(type_obj, in_molecule)
                    * (int(nbr) if nbr else 1)
                )
                in_molecule = False
                nbr = ''

            if element:
                # CaAg
                #   ^
                elements.extend(
                    [type_obj(element)] * (int(nbr) if nbr else 1)
                )

            element = carac
            nbr = ''


        elif carac.islower():
            # Ca
            #  ^
            element += carac


        elif carac in chiffres:
            # Ca6
            #   ^
            nbr += carac


    # Element restant

    if element:
        elements.extend(
            [type_obj(element)] * (int(nbr) if nbr else 1)
        )

    elif isinstance(in_molecule, str):
        elements.extend(
            convertie_notation_vers(type_obj, in_molecule)
            * (int(nbr) if nbr else 1)
        )
        in_molecule = False
        nbr = ''


    return elements


def verif_espece_stable(elements:List[Union[Atome, Ion]]) -> bool:
    """Vérifie approximativement si une espèce (molécule) est stable.

    Principe (heuristique) :
    1. Chaque atome est converti en ion (`IonMonoAtomique`) afin de
       déterminer son nombre de liaisons disponibles (`diff`).
    2. Ces nombres sont triés par ordre décroissant puis « consommés »
       par paires : chaque liaison retire une unité aux deux partenaires.
    3. L'espèce est considérée stable si toutes les charges de liaison
       disponibles sont ramenées à zéro.

    ---------
    Arguments

    elements
        :list
        Liste d'atomes/ions constituant l'espèce.

    -------
    Retours

    :bool
        `True` si l'espèce est jugée stable, `False` sinon.

    -------
    Limites

    Il s'agit d'une approximation : certaines espèces réelles peuvent être
    rejetées, et inversement (voir `tests/tests_objets.py`).
    """

    charges = sorted(
        (
            ion.diff
            for ion in [
                element if isinstance(element, IonMonoAtomique)
                else
                    IonMonoAtomique(element)
                for element in elements
            ]
        ),
        reverse=True
    )


    index_dernier_atome_liee = None

    nbr_charge = len(charges)

    range_charges = range(nbr_charge)

    for indice in range_charges:

        if not charges[indice]:
            continue

        for autre in range_charges:

            if not charges[indice]:
                break

            if (not charges[autre]
                or (
                    # Si c'est le même index pour les 2
                    #   c'est que c'est le même atome
                    #   et un atome ne peut pas s'auto-lier.
                    autre == indice

                    # Évite qu'un atome subisse 2 liaisons de suite
                    #  (le dernier atome lié n'est pas réutilisé aussitôt).
                    or autre == index_dernier_atome_liee
                )
            ):
                continue

            index_dernier_atome_liee = autre

            if charges[autre] == 4:
                
                if charges[indice] == 4:
                    charges[indice] -= 3
                    charges[autre] -= 3

                else:
                    charges[autre] -= charges[indice]
                    charges[indice] = 0

            elif charges[autre] == 3:
                
                if (
                    charges[indice] == 4
                    or (
                        # Si il n'y a que 2 éléments restant
                        #   avec 3 liaisons disponibles,
                        #   alors ils peuvent se lier entre eux avec 3 liaisons
                        #   vu qu'il ne reste aucun autre élément à se lier.
                        charges[indice] == 3
                        and nbr_charge == indice + 1
                    )
                ):
                    charges[indice] -= 3
                    charges[autre] -= 3

                elif charges[indice] == 3:
                    charges[indice] -= 2
                    charges[autre] -= 2

                else:
                    charges[autre] -= charges[indice]
                    charges[indice] = 0

            elif charges[autre] == 2:
                
                if (
                    charges[indice] == 4
                    or charges[indice] == 3
                    or (
                        # Si il n'y a que 2 éléments restant
                        #   avec 2 liaisons disponibles,
                        #   alors ils peuvent se lier entre eux avec 2 liaisons
                        #   vu qu'il ne reste aucun autre élément à se lier.
                        charges[indice] == 2
                        and nbr_charge == indice + 1
                    )
                ):
                    charges[indice] -= 2
                    charges[autre] -= 2

                else: # 2 ou 1
                    charges[indice] -= 1
                    charges[autre] -= 1

            else: # charges[autre] == 1
                charges[indice] -= 1
                charges[autre] -= 1


    # Il faut que toute les charges soit égal à 0
    #   sinon ce n'est pas stable.
    return not any(charges)


# Méthodes Atome/Ion

def notation_couche(self:Union[Atome, IonMonoAtomique]):

    return ' '.join(
        '(%s)%s' % infos
        for infos in zip(
            notations_couche,
            (affichage.exposant(electron) for electron in self.couches)
        )
    )

def notation_configuration(self:Union[Atome, IonMonoAtomique]):

    return ' '.join(
        '%s%s' % (notation, affichage.exposant(electron))
        for notation, electron in zip(
            notation_configuration_atome,
            self.configuration
        )
        if electron
    )

###<<< CAPTURE FICHIER CALC


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)
