# coding: utf-8

"""Module utilitaire pour les atomes, ions et Molécules.

Ce module a pour but de manipuler des atomes, ions et Molécules, 
 ainsi que d'avoir des informations respectives à ces éléments.

Je suis très loin d'être proffesionelle dans ce domaine,
 donc il est fort probable qu'il y est des erreurs.

Tout amélioration est la bienvenue.

Lien du github : https://github.com/4surix/atomion
"""


__version__ = '1.0.0'


import copy

from . import exceptions

from .elements import éléments


### Paramètres

class params:
    langue = 'fr'
    élément = True
    catégorie = True
    
    proton = True
    neutron = True
    électron = True

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

masse_électron = 9.109*(10**-31)
masse_proton = 1.672649*(10**-27)
masse_neutron = 1.67493*(10**-27)

mol = 6.02*10**23


### Fonction

fonctions_configuration_ion = (
    lambda c: ([c if c <= 2 else 2], c-2),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2 if c <= 8 else 6], c-8),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2], c-8) if c <= 8 else ([2, 6, c-8 if c <= 18 else 10], c-18),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2], c-8) if c <= 8 else ([2, 6, c-8], c-18) if c <= 18 else ([2, 6, 10, c-18 if c <= 32 else 14], c-32),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2], c-8) if c <= 8 else ([2, 6, c-8], c-18) if c <= 18 else ([2, 6, 10, c-18], c-32) if c <= 32 else ([2, 6, 10, 14, c-32 if c <= 50 else 18], c-50),
) 

fonctions_configuration_atome = (
    lambda c: ([c if c <= 2 else 2], c-2),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2 if c <= 8 else 6], c-8),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2 if c <= 8 else 6], c-8),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2], c-12) if c <= 12 else ([2, 10, c-12 if c <= 18 else 6], c-18),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2], c-12) if c <= 12 else ([2, 10, c-12 if c <= 18 else 6], c-18),
    lambda c: ([c], c-2) if c <= 2 else ([2, c-2], c-16) if c <= 16 else ([2, 14, c-16], c-26) if c <= 26 else ([2, 14, 10, c-26 if c <= 32 else 6], c-32)
) 

fonctions_get = {
    # électron(s) = (Masse de l'Atome - (Masse des protons + Masse des neutrons)) / Masse d'un életron
    'électron': lambda obj: round(
        (obj.masse_atomique_relative * u
        - (  (masse_neutron * obj.neutron)
           + (masse_proton * obj.proton)
          )
        ) / masse_électron),

    # Proton(s) = (Masse de l'Atome - (Masse des électrons + Masse des neutrons)) / Masse d'un proton
    'proton': lambda obj: round(
        (obj.masse_atomique_relative * u
        - (  (masse_électron * obj.électron)
           + (masse_neutron * obj.neutron)
          )
        ) / masse_proton),

    # Neuton(s) = (Masse de l'Atome - (Masse des électrons + Masse des protons)) / Masse d'un neutron
    'neutron': lambda obj: round(
        (obj.masse_atomique_relative * u
        - (  (masse_électron * obj.électron)
           + (masse_proton * obj.proton)
          )
        ) / masse_neutron),
}


### Notations

notation_configuration_ion = (
    '1s','2s','2p','3s','3p','3d','4s','4p','4d','4f','5s','5p','5d','5f','5g')

notation_configuration_atome = (
    '1s','2s','2p','3s','3p','4s','3d','4p','5s','4d','5p','6s','4f','5d','6p','7s','5f','6d','7p')

notations_couche = (
    'K','L','M','N','O','P')

exposants = tuple('⁰¹²³⁴⁵⁶⁷⁸⁹')
sous_exposants = tuple('₀₁₂₃₄₅₆₇₈₉')


### Utitaire

def configuration_électronique(élément) -> list:
    """Génére la configuration électronique d'un atome/ion.

    Paramètres
    -------
    élément
        :Atome
        :Ion


    Retourne
    ------- 
    List
        Liste contenant le nombre d'électron par couche.
    """

    couches = []

    électrons = élément.électron
    protons = élément.proton

    if isinstance(élément, Atome):
        fonctions = fonctions_configuration_atome
    elif isinstance(élément, Ion):
        fonctions = fonctions_configuration_ion


    for i in range(5):
        couche, électrons = fonctions[i](électrons)
        couches.extend(couche)

        if électrons <= 0:
            break


    exception = exceptions.configuration.get(protons)

    if exception:
        couches[-len(exception):] = exception

    return couches


def get_info(obj, valeur) -> None:
    """Récupére les informations d'un atome grâce à son nombre de proton ou son symbole.

    Paramètres
    -------
    obj
        :Atome
        :Ion

    valeur
        :Str
            Récupérer les infos suivant le symbole indiqué
        :Int
            Récupérer les infos suivant le nombre de proton indiqué
        :Ion
            Récupérer les infos suivant le nombre de proton de l'ion,
            Pour la conversation Ion -> Atome
        :Atome
            Récupérer les infos suivant le nombre de proton de l'atome,
            Pour la conversation Atome -> Ion


    Retourne
    ------- 
    None
    """

    if isinstance(valeur, type(obj)):
        raise Exception("Cette élément est déjà un %s !" % type(obj).__name__)

    elif isinstance(valeur, (Ion, Atome)):

        obj.proton = valeur.proton
        obj.neutron = valeur.neutron

    elif isinstance(valeur, int):

        if valeur >= len(éléments):
            raise Exception("Le nombre de proton doit exister !")
        elif valeur <= 0:
            raise Exception("Le nombre de proton doit être supérieur à zéro !")
        else:
            obj.proton = valeur

    elif isinstance(valeur, str):

        obj.proton = None

        for proton, élément in enumerate(éléments):
            if élément['symbol'] == valeur:
                obj.proton = proton+1
                break

        if not obj.proton:
            raise Exception("Le symbole '%s' ne correspond à aucun élément existant !" % valeur)


    élément = éléments[obj.proton-1]

    (
        obj.élément, 
        obj.symbole, 
        obj.catégorie,
        obj.couches, 
        obj.masse_atomique_relative

        ) = (

        élément['name'],
        élément['symbol'],
        élément['category'],
        élément['shells'][:],
        élément['atomic_mass']
    )


def get(item:str, obj):
    """Récupére un item de l'objet.

    Paramètres
    -------
    item
        :str
            'électron'
                Récupére les électrons de l'objet
            'proton'
                Récupére les protons de l'objet
            'neutron'
                Récupére les neutrons de l'objet

    obj
        :Atome
        :Ion


    Retournes
    -------
    Type
    """
    return fonctions_get.get(item, lambda x:None)(obj)


def get_masse(obj) -> float:
    """Récupére la masse de l'objet.

    Paramètres
    -------
    obj
        :Atome
        :Ion


    Retournes
    -------
    Float
        Masse de l'objet.
    """
    return (obj.proton*masse_proton) + (obj.neutron*masse_neutron) + (obj.électron*masse_électron)


def decode(data:str) -> list:
    """Transforme un str en list d'atomes
    """

    atome = ''
    atomes = []
    nbr = ''

    in_molécule = False

    chiffres = list('0123456789')


    for carac in data.strip()+' ':          

        if carac == ')':
            in_molécule = ''.join(in_molécule)


        elif isinstance(in_molécule, list):
            in_molécule.append(carac)


        elif carac == '(':

            if atome:
                atomes.extend([Atome(atome)] * (int(nbr) if nbr else 1))
                atome = ''
                nbr = ''

            if in_molécule:
                atomes.extend(decode(in_molécule) * (int(nbr) if nbr else 1))
                in_molécule = False
                nbr = ''

            in_molécule = []


        elif carac.isupper():

            if in_molécule:
                atomes.extend(decode(in_molécule) * (int(nbr) if nbr else 1))
                in_molécule = False
                nbr = ''

            if atome:
                atomes.extend([Atome(atome)] * (int(nbr) if nbr else 1))

            atome = carac

            nbr = ''


        elif carac.islower():

            atome += carac


        elif carac in chiffres:

            nbr += carac


        elif in_molécule:
            atomes.extend(decode(in_molécule) * (int(nbr) if nbr else 1))
            in_molécule = False
            nbr = ''


    if atome:
        atomes.extend([Atome(atome)] * (int(nbr) if nbr else 1))


    return atomes


def verif_stable(molécule) -> None:
    """Vérifie si une molécule est stable en vérifiant son nombre de liaison
    """

    charges = sorted([ion.diff for ion in [Ion(élément) for élément in molécule.atomes if not isinstance(élément, Ion)]], reverse=True)


    for I in range(len(charges)):

        if not charges[I]:
            continue

        for i in range(len(charges)):

            if not charges[i] or i == I:
                continue

            if charges[i] > 2:
                
                if charges[I] > 2:
                    charges[I] -= 2
                    charges[i] -= 2

                else:
                    charges[I] = 0
                    charges[i] -= charges[I]

            else:

                if charges[I] > 2:
                    charges[I] -= charges[i]
                    charges[i] -= charges[i]

                else:

                    if charges[I] > charges[i]:
                        charge = charges[i]
                    else:
                        charge = charges[I]

                    charges[I] -= charge
                    charges[i] -= charge


    if any(charges):
        raise Exception("Votre molécule %s n'est pas stable !" % molécule.notation())


### Objets

class Neutron:
    """Objet d'un nombre de neutron servant pour les opérations

    Paramètres
    -------
    valeur
        :Atome
        :Ion
        :Int
        

    Retours
    -------
    Neutron
        .valeur: int
            Nombre de neutron
    """
    def __init__(self, valeur=1):

        if isinstance(valeur, (Atome, Ion)):
            self.valeur = valeur.neutron

        elif isinstance(valeur, int):
            self.valeur = valeur


class Proton:
    """Objet d'un nombre de proton servant pour les opérations

    Paramètres
    -------
    valeur
        :Atome
        :Ion
        :Int


    Retours
    -------
    Proton
        .valeur: int
            Nombre de proton
    """
    def __init__(self, valeur=1):

        if isinstance(valeur, (Atome, Ion)):
            self.valeur = valeur.proton

        elif isinstance(valeur, int):
            self.valeur = valeur


class Electron:
    """Objet d'un nombre d'électron servant pour les opérations

    Parameters
    ----------
    valeur
        :Atome
        :Ion
        :Int


    Returns
    -------
    Electron
        .valeur: int
            Nombre d'électron
    """
    def __init__(self, valeur=1):

        if isinstance(valeur, (Atome, Ion)):
            self.valeur = valeur.électron

        elif isinstance(valeur, int):
            self.valeur = valeur


class Ion:
    """Création d'un Ion.

    Paramètres
    -------
    valeur
        :Atome
            Transforme l'atome en ion.
        :Ion
            Léve une erreur
        :Int
            Equivaut au nombre de proton et créer un ion.


    Retours
    -------
    Ion
        .élément
        .symbole
        .catégorie

        .proton
        .neutron
        .électron
        .nucléon

        .masse
        .masse_atomique_relative

        .couches
        .configuration

        .diff
            Différence entre le nombre de proton et d'électron
        .charge
            Charges électrique de l'ion
    """

    __slots__ = ('élément', 'symbole', 'catégorie', 
                 'proton', 'neutron', 'électron', 'nucléon',
                 'masse', 'masse_atomique_relative',
                 'configuration', 'couches', 
                 'diff', 'charge')

    def __init__(self, valeur=1, électron=0, neutron=None):

        self.neutron = neutron

        self.électron = électron

        get_info(self, valeur)


        drn_couche = self.couches[-1]

        if 0 < drn_couche < 5:
            self.électron = self.proton - drn_couche
            self.charge = '+'
            del self.couches[-1]

        elif 4 < drn_couche < 8:
            self.électron = self.proton + (8 - drn_couche)
            self.charge = '-'
            self.couches[-1] = 8

        else:
            raise Exception('Cette atome ne peut pas être un ion !')


        if self.neutron is None:
            self.neutron = round(self.masse_atomique_relative) - self.proton

        self.diff = abs(self.proton - self.électron)

        self.masse = get_masse(self)

        self.nucléon = self.proton + self.neutron

        self.configuration = configuration_électronique(self)

    def __add__(self, obj):

        if isinstance(obj, Proton):
            return Ion(self.proton + obj.valeur)

        else:
            raise Exception("Type '%s' non compatible avec type 'Atome'." % type(obj))

    def __iadd__(self, obj):
        return self + obj

    def __sub__(self, obj):

        if isinstance(obj, Proton):
            return Atome(self.proton - obj.valeur)

        else:
            raise Exception("Type '%s' non compatible avec type 'Atome'." % type(obj))

    def __isub__(self, obj):
        return self - obj

    def __str__(self): 
        return  (  "Ion %s" % self.notation()
                +("\n Elément: %s" % self.élément[params.langue] if params.élément else '')
                +("\n Catégorie: %s" % self.catégorie[params.langue] if params.catégorie else '')
                +("\n Proton(s): %s" % self.proton if params.proton else '')
                +("\n Neutron(s): %s" % self.neutron if params.neutron else '')
                +("\n Electron(s): %s" % self.électron if params.électron else '')
                +("\n Masse: %s" % self.masse if params.masse else '')
                +("\n Masse atomique relative: %s" % self.masse_atomique_relative if params.masse_relative else '')
                +("\n Couche électronique: %s" % self.notation_couche() if params.couches else '')
                +("\n Configuration électronique: %s" % self.notation_configuration() if params.configuration else '')
                )

    def __repr__(self):
        return self.notation_symbole()

    def notation(self):
        return "%s %s%s Z=%s A=%s" % (self.symbole, self.diff, self.charge, self.proton, self.proton + self.neutron)

    def notation_symbole(self, A=True, Z=True):
        return "%s%s%s%s%s" % (''.join(exposants[int(num)] for num in str(self.proton + self.neutron)) if A else '',
                               ''.join(sous_exposants[int(num)] for num in str(self.proton)) if Z else '',
                               self.symbole,
                               ''.join(exposants[int(num)] for num in str(self.diff)),
                               {'-':'⁻', '+':'⁺'}.get(self.charge))

    def notation_couche(self):
        couches = [''.join(exposants[int(num)] for num in str(électron))
                        for électron in self.couches]
        return ' '.join(['(%s)%s' % r for r in zip(notations_couche, couches)])

    def notation_configuration(self):
        return ' '.join(
            '%s%s' % (notation, ''.join(exposants[int(num)] for num in str(électron))) for notation, électron in zip(notation_configuration_ion, self.configuration) if électron
        )


class Atome:
    """Création d'un Atome.

    Paramètres
    -------
    valeur
        :Atome
            Léve une erreur
        :Ion
            Transforme l'ion en atome.
        :Int
            Equivaut au nombre de proton et créer un Atome.

    neutron
        :Int
            Définie le nombre de proton pour l'isotope.


    Retour
    -------
    Atome
        .élément
        .symbole
        .catégorie

        .proton
        .neutron
        .électron
        .nucléon

        .masse
        .masse_atomique_relative

        .configuration
        .couches
    """

    __slots__ = ('élément', 'symbole', 'catégorie',
                 'proton', 'neutron', 'nucléon', 'électron', 
                 'masse', 'masse_atomique_relative', 
                 'configuration', 'couches')

    def __init__(self, valeur=1, neutron=None):

        self.neutron = neutron

        get_info(self, valeur)

        self.électron = self.proton

        if self.neutron is None:
            self.neutron = round(self.masse_atomique_relative) - self.proton

        self.masse = get_masse(self)

        self.nucléon = self.proton + self.neutron

        self.configuration = configuration_électronique(self)

    def __add__(self, obj):

        if isinstance(obj, Proton):
            return Atome(self.proton + obj.valeur)

        elif isinstance(obj, Neutron):
            return Atome(self.proton, self.neutron + obj.valeur)

        elif isinstance(obj, Electron):
            return Ion(self.proton, self.électron + obj.valeur)

        elif isinstance(obj, Atome):
            return Molécule([self, obj])

        else:
            raise Exception("Type '%s' non compatible avec type 'Atome'." % type(obj))

    def __iadd__(self, obj):
        return self + obj

    def __sub__(self, obj):

        if isinstance(obj, Proton):
            return Atome(self.proton - obj.valeur)

        elif isinstance(obj, Neutron):
            return Atome(self.proton, self.neutron - obj.valeur)

        elif isinstance(obj, Electron):
            return Ion(self.proton, self.électron - obj.valeur)

        else:
            raise Exception("Type '%s' non compatible avec type 'Atome'." % type(obj))

    def __isub__(self, obj):
        return self - obj

    def __mul__(self, obj):
        return Molécule([self] * obj)

    def __str__(self):
        return  (   "Atome %s" % self.notation()
                +("\n Elément: %s" % self.élément[params.langue] if params.élément else '')
                +("\n Catégorie: %s" % self.catégorie[params.langue] if params.catégorie else '')
                +("\n Proton(s): %s" % self.proton if params.proton else '')
                +("\n Neutron(s): %s" % self.neutron if params.neutron else '')
                +("\n Electron(s): %s" % self.électron if params.électron else '')
                +("\n Masse: %s" % self.masse if params.masse else '')
                +("\n Masse atomique relative: %s" % self.masse_atomique_relative if params.masse_relative else '')
                +("\n Couche électronique: %s" % self.notation_couche() if params.couches else '')
                +("\n Configuration électronique: %s" % self.notation_configuration() if params.configuration else '')
                )

    def __repr__(self):
        return self.notation_symbole()

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, obj):
        return repr(self) == repr(obj)

    def notation(self):
        return "%s Z=%s A=%s" % (self.symbole, self.proton, self.proton + self.neutron) 

    def notation_symbole(self, A=True, Z=True):
        return "%s%s%s" % (''.join(exposants[int(num)] for num in str(self.proton + self.neutron)) if A else '',
                           ''.join(sous_exposants[int(num)] for num in str(self.proton)) if Z else '',
                           self.symbole)

    def notation_couche(self):
        couches = [''.join(exposants[int(num)] for num in str(électron))
                        for électron in self.couches]
        return ' '.join(['(%s)%s' % r for r in zip(notations_couche, couches)])

    def notation_configuration(self):
        return ' '.join(
            '%s%s' % (notation, ''.join(exposants[int(num)] for num in str(électron))) for notation, électron in zip(notation_configuration_atome, self.configuration) if électron
        )

    def demonstration(self, recup, avec):
        """Retourne une démonstration de calcul

        Paramètres
        -------
        recup
            :str
                'électron'
                'neutron'
                'proton'

        avec
            :str
                'masse'
                'Z'


        Retours
        -------
        Str
            La démonstration
        """

        if recup == 'électron':

            if avec == 'masse':

                e = "électron %s = " % self.notation_symbole()

                _masse_neutrons = masse_neutron * self.neutron
                _masse_protons = masse_proton * self.proton
                _masse_neutrons_protons = _masse_neutrons + _masse_protons
                _masse_neutrons_protons_m_total = self.masse - _masse_neutrons_protons

                demo = [
                e + "(Masse de l'Atome - (Masse neutron x Nombre neutron + Masse proton x Nombre proton)) / Masse électron",
                e + "(%s - (%s x %s + %s x %s)) / %s" % (self.masse, masse_neutron, self.neutron, 
                                                         masse_proton, self.proton, masse_électron),
                e + "(%s - (%s + %s)) / %s" % (self.masse, _masse_neutrons, _masse_protons, masse_électron),
                e + "(%s - %s) / %s" % (self.masse, _masse_neutrons_protons, masse_électron),
                e + "%s / %s" % (_masse_neutrons_protons_m_total, masse_électron),
                e + "%s" % round(_masse_neutrons_protons_m_total / masse_électron)
                ]

        if recup == 'neutron':

            if avec == 'masse':

                e = "Neutron %s = " % self.notation_symbole()

                demo = [
                e + "(Masse de l'Atome - (Masse électron x Nombre électron + Masse proton x Nombre proton)) / Masse neutron",
                e + "(%s - (%s x %s + %s x %s)) / %s" % (self.masse, masse_électron, self.électron, 
                                                         masse_proton, self.proton, masse_neutron),
                e + "(%s - (%s + %s)) / %s" % (self.masse, masse_électron * self.électron, 
                                               masse_proton * self.proton, masse_neutron),
                e + "(%s - %s) / %s" % (self.masse, masse_électron * self.neutron + masse_proton * self.proton, 
                                        masse_neutron),
                e + "%s / %s" % (self.masse - (masse_électron * self.électron + masse_proton * self.proton), 
                                 masse_neutron),
                e + "%s" % round((self.masse - (masse_électron * self.électron + masse_proton * self.proton)) / masse_neutron)
                ]

            if avec == 'Z':

                e = "Neutron %s = " % self.notation_symbole()

                demo = [
                e + "nombre de nucléons - nombre de proton",
                e + "A - Z",
                e + "%s - %s" % (self.proton + self.neutron, self.proton),
                e + "%s" % self.neutron
                ]

        if recup == 'proton':

            if avec == 'masse':

                e = "Proton %s = " % self.notation_symbole()

                demo = [
                e + "(Masse de l'Atome - (Masse neutron x Nombre neutron + Masse électron x Nombre électron)) / Masse proton",
                e + "(%s - (%s x %s + %s x %s)) / %s" % (self.masse, masse_neutron, self.neutron, 
                                                         masse_électron, self.électron, masse_proton),
                e + "(%s - (%s + %s)) / %s" % (self.masse, masse_neutron * self.neutron, 
                                               masse_électron * self.électron, masse_proton),
                e + "(%s - %s) / %s" % (self.masse, masse_neutron * self.neutron + masse_électron * self.électron, 
                                        masse_proton),
                e + "%s / %s" % (self.masse - (masse_neutron * self.neutron + masse_électron * self.électron), 
                                 masse_proton),
                e + "%s" % round((self.masse - (masse_neutron * self.neutron + masse_électron * self.électron)) / masse_proton)
                ]

            if avec == 'Z':

                e = "Proton %s = " % self.notation_symbole()

                demo = [
                e + "nombre de proton",
                e + "Z",
                e + "%s" % self.proton
                ]

        return '\n'.join(demo)


class Molécule:
    """Création d'une Molécule

    Paramètres
    -------
    valeur
        :str
            Symbole de la Molécule qui sera décodé


    Retour
    -------
    Molécule
        .atomes
            :list

        .proton
        .neutron
        .électron
        .nucléon

        .masse
        .masse_moléculaire_relative
    """

    __slots__ = ('atomes', 
                 'proton', 'neutron', 'électron', 
                 'masse', 'masse_moléculaire_relative')

    def __init__(self, valeur):

        self.atomes = decode(valeur) if isinstance(valeur, str) else valeur

        if len(self.atomes) < 2:
            raise Exception("Une Molécule doit être composée de plusieurs atome.")

        verif_stable(self)

        self.proton = sum(atome.proton for atome in self.atomes)
        self.neutron = sum(atome.neutron for atome in self.atomes)
        self.électron = sum(atome.électron for atome in self.atomes)

        self.masse = sum(atome.masse for atome in self.atomes)
        self.masse_moléculaire_relative = sum(atome.masse_atomique_relative for atome in self.atomes)

    def __str__(self):

        return  (   "Molécule %s" % self.notation()
                +("\n Proton(s): %s" % self.proton if params.proton else '')
                +("\n Neutron(s): %s" % self.neutron if params.neutron else '')
                +("\n Electron(s): %s" % self.électron if params.électron else '')
                +("\n Masse: %s" % self.masse if params.masse else '')
                +("\n Masse moléculaire relative: %s" % self.masse_moléculaire_relative if params.masse_relative else '')
                )

    def __repr__(self):
        return self.notation()

    def __add__(self, obj):

        if isinstance(obj, Molécule):

            atomes = copy.deepcopy(self.atomes)
            atomes.extend(obj.atomes)
            return Molécule(atomes)

        elif isinstance(obj, Atome):

            atomes = copy.deepcopy(self.atomes)
            atomes.append(obj)
            return Molécule(atomes)

        else:
            raise Exception("Type '%s' non compatible avec type 'Molécule'." % type(obj))

    def __iadd__(self, obj):
        return self + obj

    def __sub__(self, obj):

        if isinstance(obj, Molécule):

            atomes = copy.deepcopy(self.atomes)
            for atome in obj.atomes:
                atomes.remove(atome)
            return Molécule(atomes)

        elif isinstance(obj, Atome):

            atomes = copy.deepcopy(self.atomes)
            atomes.remove(obj)
            return Molécule(atomes)

        else:
            raise Exception("Type '%s' non compatible avec type 'Molécule'." % type(obj))

    def __isub__(self, obj):
        return self - obj

    def notation(self):

        atomes = {}

        for atome in self.atomes:
            atome = atome.notation_symbole(A=False, Z=False)
            if atome not in atomes:
                atomes[atome] = 0
            atomes[atome] += 1

        return ''.join(
            '%s%s' % (atome, ''.join(sous_exposants[int(num)] for num in str(nbr)) if nbr != 1 else '') for atome, nbr in atomes.items()
        )


### Raccourcies

# Atome
C = Atome('C')
N = Atome('N')
H = Atome('H')
O = Atome('O')

# Molécule
CO2 = Molécule('CO2')
CH4 = Molécule('CH4')
