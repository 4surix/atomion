# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from . import irregularites
from . import exception
from .elements import elements
from . import objets


### Verif si calculatrice

try:
    enumerate = enumerate
    type('EssaieMul', (), {'__mul__': lambda self, objet: None}) * 2
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
    element = True
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
    # electron(s) = (Masse de l'Atome - (Masse des protons + Masse des neutrons)) / Masse d'un eletron
    'electron': lambda obj: round(
        (
            obj.masse_atomique_relative * u
            - (
                (masse_neutron * obj.neutron)
                + (masse_proton * obj.proton)
            )
        ) / masse_electron
    ),

    # Proton(s) = (Masse de l'Atome - (Masse des electrons + Masse des neutrons)) / Masse d'un proton
    'proton': lambda obj: round(
        (
            obj.masse_atomique_relative * u
            - (
                (masse_electron * obj.electron)
                + (masse_neutron * obj.neutron)
            )
        ) / masse_proton
    ),

    # Neuton(s) = (Masse de l'Atome - (Masse des electrons + Masse des protons)) / Masse d'un neutron
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
    '1s','2s','2p','3s','3p','4s','3d','4p','5s','4d','5p','6s','4f','5d','6p',
    '7s','5f','6d','7p'
)

notations_couche = (
    'K','L','M','N','O','P'
)

exposants = tuple('⁰¹²³⁴⁵⁶⁷⁸⁹')
sous_exposants = tuple('₀₁₂₃₄₅₆₇₈₉')


### Utitaire

def configuration_electronique(element) -> list:
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

    if isinstance(element, objets.Atome):
        fonctions = fonctions_configuration_atome
    elif isinstance(element, objets.Ion):
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


def get_info(obj, valeur) -> None:
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

    elif isinstance(valeur, (objets.Ion, objets.Atome)):

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
        obj.element, 
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


def get_value(item:str, obj):
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


def get_masse(obj) -> float:
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


def convertie_notation_vers_atomes(data:str) -> list:
    """

    Transforme un str en list d'atomes

    ---------
    Arguments

    data
        :str
            Notation de l'atome

    -------
    Retours

    :list
        Liste contenant une liste d'atome.
    """

    atome = ''
    atomes = []
    nbr = ''

    in_molecule = False

    chiffres = list('0123456789')


    for carac in data.strip():          

        if carac == ')':
            # in_molecule == ['C', 'O', '2'] -> in_molecule == 'CO2'
            in_molecule = ''.join(in_molecule)


        elif isinstance(in_molecule, list):
            # (CO2)3 -> in_molecule == ['C', 'O', '2']
            in_molecule.append(carac)


        elif carac == '(':

            if atome:
                # CO2(H2)
                #    ^
                atomes.extend([objets.Atome(atome)] * (int(nbr) if nbr else 1))
                atome = ''
                nbr = ''

            if isinstance(in_molecule, str):
                # CO2(H2)4(Ag7)2
                #         ^
                atomes.extend(
                    convertie_notation_vers_atomes(in_molecule) 
                    * (int(nbr) if nbr else 1)
                )
                nbr = ''

            in_molecule = []


        elif carac.isupper():

            if in_molecule:
                # (H2)2Ca
                #      ^
                atomes.extend(
                    convertie_notation_vers_atomes(in_molecule) 
                    * (int(nbr) if nbr else 1)
                )
                in_molecule = False
                nbr = ''

            if atome:
                # CaAg
                #   ^
                atomes.extend([objets.Atome(atome)] * (int(nbr) if nbr else 1))

            atome = carac
            nbr = ''


        elif carac.islower():
            # Ca
            #  ^
            atome += carac


        elif carac in chiffres:
            # Ca6
            #   ^
            nbr += carac


    # Element restant

    if atome:
        atomes.extend([objets.Atome(atome)] * (int(nbr) if nbr else 1))

    elif isinstance(in_molecule, str):
        atomes.extend(
            convertie_notation_vers_atomes(in_molecule) 
            * (int(nbr) if nbr else 1)
        )
        in_molecule = False
        nbr = ''


    return atomes


def verif_stable(elements:list) -> bool:
    """

    Vérifie si des éléments sont stable 
      en vérifiant leurs nombre de liaison.

    ---------
    Arguments

    elements:list

    ---------
    Exception

    Lève une exception si ce n'est pas stable.

    -------
    Retours

    None
    """

    charges = sorted(
        (
            ion.diff 
            for ion in [
                element if isinstance(element, objets.IonMonoAtomique)
                else
                    objets.IonMonoAtomique(element)
                for element in elements
            ]
        ),
        reverse=True
    )


    index_dernier_atome_liee = None

    range_charges = range(len(charges))

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

            else:

                if charges[I] == 4:
                    charges[I] -= charges[i]
                    charges[i] = 0

                else:
                    charge = min(charges[i], charges[I])

                    charges[I] -= charge
                    charges[i] -= charge

    # Il faut que toute les charges soit égal à 0
    #   sinon ce n'est pas stable.
    return not any(charges)


# Méthodes Atome/Ion

def notation_couche(self):

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

def notation_configuration(self):

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


### Equilibrage équation chimique

def eec_analyse(partie):

    info = []

    for element in partie:

        nombre_atomes = {}

        for atome in (
                element.atomes
                if isinstance(element, objets.Molecule)
                else
                    [element]
            ):

            symbole = atome.symbole

            if symbole not in nombre_atomes:
                nombre_atomes[symbole] = 1
            else:
                nombre_atomes[symbole] += 1

        info.append(nombre_atomes)

    return info


def eec_convertie(notation):

    try: return objets.Molecule(notation, verif_stable=False)
    except:
        return objets.Atome(notation)


def equilibrage_equation_chimique(equation):

    partie_1, partie_2 = equation.split('->')

    partie_1_molecules = [
        eec_convertie(notation)
        for notation in partie_1.split('+')
    ]

    partie_2_molecules = [
        eec_convertie(notation)
        for notation in partie_2.split('+')
    ]

    partie_1 = eec_analyse(partie_1_molecules)
    partie_2 = eec_analyse(partie_2_molecules)

    liste_symboles_atomes = {
        symbole
        for info in partie_1
        for symbole in info
    }

    configuration = [
        [1 for _ in range(len(partie_1))],
        [1 for _ in range(len(partie_2))]
    ]

    equilibre = 0

    nbr_liste_symboles_atomes = len(liste_symboles_atomes)

    while equilibre != nbr_liste_symboles_atomes:

        for symbole in liste_symboles_atomes:

            nombre_total_p1 = sum(
                info.get(symbole, 0) * configuration[0][i]
                for i, info in enumerate(partie_1)
            )

            nombre_total_p2 = sum(
                info.get(symbole, 0) * configuration[1][i]
                for i, info in enumerate(partie_2)
            )

            if nombre_total_p1 < nombre_total_p2:

                index = None
                min_value = 2147483647

                for i, info in enumerate(partie_1):
                    value = info.get(symbole, 0) * configuration[0][i]

                    if value and value < min_value:
                        index = i
                        min_value = value

                configuration[0][index] += 1

                equilibre = 0
                break

            elif nombre_total_p2 < nombre_total_p1:

                index = None
                min_value = 2147483647

                for i, info in enumerate(partie_2):
                    value = info.get(symbole, 0) * configuration[1][i]

                    if value and value < min_value:
                        index = i
                        min_value = value

                configuration[1][index] += 1

                equilibre = 0
                break

            else:
                equilibre += 1

    return (
        ' + '.join(
            '%s%s' % (str(nbr) + ' ' if nbr != 1 else '', molecule.notation())
            for nbr, molecule in zip(configuration[0], partie_1_molecules)
        )
        + ' -> '
        + ' + '.join(
            '%s%s' % (str(nbr) + ' ' if nbr != 1 else '', molecule.notation())
            for nbr, molecule in zip(configuration[1], partie_2_molecules)
        )
    )

eec = equilibrage_equation_chimique