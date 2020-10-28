# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from .typing import *

from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)

from .. import irregularites
from .. import exception
from ..elements import elements


###>>> CAPTURE FICHIER CALC

### Verif si calculatrice

try:
    enumerate = enumerate
    type(
        'EssaieMul',
        (), 
        {'__mul__': lambda self, objet: 1 * objet}
    )() * 2
except:

    is_calculatrice = True

    def enumerate(iterable, index=0):
        for valeur in iterable:
            yield index, valeur
            index += 1

    def mul(inicial, *elements):
        for element in elements:
            inicial = inicial.__mul__(element)
        return inicial

else:
    is_calculatrice = False


### Paramètres

class params:
    calculatrice = is_calculatrice

    langue = 'fr'

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
        for key, valeur in params_.items():
            if getattr(params, key, None) is not None:
                setattr(params, key, valeur)


### Valeur de base pour les calculs

u = 1.660538921*(10**-27)

masse_electron = 9.109*(10**-31)
masse_proton = 1.672649*(10**-27)
masse_neutron = 1.67493*(10**-27)

mol = 6.02*10**23


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


### Utitaire

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


    exception = irregularites.configuration.get(protons)

    if exception:
        couches[-len(exception):] = exception

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

        if valeur >= len(elements):
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
        obj.masse_atomique_relative

        ) = (

        element['name'],
        element['symbol'],
        element['category'],
        element['shells'][:],
        element['atomic_mass']
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
                    convertie_notation_vers_atomes(in_molecule) 
                    * (int(nbr) if nbr else 1)
                )
                nbr = ''

            in_molecule = []


        elif carac.isupper():

            if in_molecule:
                # (H2)2Ca
                #      ^
                elements.extend(
                    convertie_notation_vers_atomes(in_molecule) 
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
    """
    Vérifie si des éléments sont stable en vérifiant leurs nombre de liaison.
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

    for I in range_charges:

        if not charges[I]:
            continue

        for i in range_charges:

            if not charges[I]:
                break

            if (not charges[i] 
                or (
                    # Si c'est le même index pour les 2
                    #   c'est que c'est le même atome
                    #   et un atome ne peut pas s'auto-lier.
                    i == I

                    # Evite qu'un atome subit 2 liaisons de suite.
                    # Je ne commprend pas trop comment ça fonctionne
                    #    mais ça fonctionne.
                    or i == index_dernier_atome_liee
                )
            ):
                continue

            index_dernier_atome_liee = i

            if charges[i] == 4:
                
                if charges[I] == 4:
                    charges[I] -= 3
                    charges[i] -= 3

                else:
                    charges[i] -= charges[I]
                    charges[I] = 0

            elif charges[i] == 3:
                
                if (
                    charges[I] == 4 
                    or (
                        # Si il n'y a que 2 éléments restant
                        #   avec 3 liaisons disponibles,
                        #   alors ils peuvent se lier entre eux avec 3 liaisons
                        #   vu qu'il ne reste aucun autre élément à se lier.
                        charges[I] == 3
                        and nbr_charge == I + 1
                    )
                ):
                    charges[I] -= 3
                    charges[i] -= 3

                elif charges[I] == 3:
                    charges[I] -= 2
                    charges[i] -= 2

                else:
                    charges[i] -= charges[I]
                    charges[I] = 0

            elif charges[i] == 2:
                
                if (
                    charges[I] == 4
                    or charges[I] == 3
                    or (
                        # Si il n'y a que 2 éléments restant
                        #   avec 2 liaisons disponibles,
                        #   alors ils peuvent se lier entre eux avec 2 liaisons
                        #   vu qu'il ne reste aucun autre élément à se lier.
                        charges[I] == 2
                        and nbr_charge == I + 1
                    )
                ):
                    charges[I] -= 2
                    charges[i] -= 2

                else: # 2 ou 1
                    charges[I] -= 1
                    charges[i] -= 1

            else: # charges[i] == 1
                charges[I] -= 1
                charges[i] -= 1


    # Il faut que toute les charges soit égal à 0
    #   sinon ce n'est pas stable.
    return not any(charges)


# Méthodes Atome/Ion

def notation_couche(self:Union[Atome, IonMonoAtomique]):

    return ' '.join(
        '(%s)%s' % infos
        for infos in zip(
            notations_couche,
            (
                (
                    electron if params.calculatrice
                    else
                        ''.join(
                            exposants[int(num)] 
                            for num in str(electron)
                        )
                )
                for electron in self.couches
            )
        )
    )

def notation_configuration(self:Union[Atome, IonMonoAtomique]):

    return ' '.join(
        '%s%s' % (
            notation,
            (
                electron if params.calculatrice
                else
                    ''.join(
                        exposants[int(num)] 
                        for num in str(electron)
                    )
            )
        )
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