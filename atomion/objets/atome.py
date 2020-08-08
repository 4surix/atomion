"""

Objet atome.

---------
Arguments

valeur
    :Atome
        Léve une erreur
    :Ion
        Transforme l'ion en atome.
    :int
        Equivaut au nombre de proton et créer un Atome.

neutron
    :int
        Définie le nombre de proton pour l'isotope.

------
Retour

Atome
    .élément:str
    .symbole:str
    .catégorie:str

    .proton:int
    .neutron:int
    .électron:int
    .nucléon:int

    .masse:float
    .masse_atomique_relative:float

    .configuration:list
    .couches:list

    .notation()
    .notation_symbole()
    .notation_couche()
    .notation_configuration()
"""

from .. import utile

from .base import Molécule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur=1, neutron=None):

    self.neutron = neutron

    utile.get_info(self, valeur)

    self.électron = self.proton

    if self.neutron is None:
        self.neutron = round(self.masse_atomique_relative) - self.proton

    self.masse = utile.get_masse(self)

    self.nucléon = self.proton + self.neutron

    self.configuration = utile.configuration_électronique(self)

Atome.__init__ = __init


def __add(self, obj):

    if isinstance(obj, Proton):
        return Atome(self.proton + obj.valeur)

    elif isinstance(obj, Neutron):
        return Atome(self.proton, self.neutron + obj.valeur)

    elif isinstance(obj, Electron):
        return Ion(self.proton, self.électron + obj.valeur)

    elif isinstance(obj, Atome):
        return Molécule([self, obj])

    else:
        raise Exception(
            f"Onjet '{obj.__class__}' non compatible avec objet 'Atome'."
        )

Atome.__add__ = __add


def __iadd(self, obj):
    return self + obj

Atome.__iadd__ = __iadd


def __sub(self, obj):

    if isinstance(obj, Proton):
        return Atome(self.proton - obj.valeur)

    elif isinstance(obj, Neutron):
        return Atome(self.proton, self.neutron - obj.valeur)

    elif isinstance(obj, Electron):
        return Ion(self.proton, self.électron - obj.valeur)

    else:
        raise Exception(
            f"Objet '{obj.__class__}' non compatible avec objet 'Atome'."
        )

Atome.__sub__ = __sub


def __isub(self, obj):
    return self - obj

Atome.__isub__ = __sub


def __mul(self, obj):
    return Molécule([self] * obj)

Atome.__mul__ = __mul


def __str(self):
    return (
        "Atome %s" % self.notation()
        + (
            "\n Elément: %s" % self.élément[utile.params.langue] 
            if utile.params.élément else ''
        )
        + (
            "\n Catégorie: %s" % self.catégorie[utile.params.langue] 
            if utile.params.catégorie else ''
        )
        + (
            "\n Proton(s): %s" % self.proton 
            if utile.params.proton else ''
        )
        + (
            "\n Neutron(s): %s" % self.neutron 
            if utile.params.neutron else ''
        )
        + (
            "\n Electron(s): %s" % self.électron 
            if utile.params.électron else ''
        )
        + (
            "\n Masse: %s" % self.masse 
            if utile.params.masse else ''
        )
        + (
            "\n Masse atomique relative: %s" % self.masse_atomique_relative
            if utile.params.masse_relative else ''
        )
        + (
            "\n Couche électronique: %s" % self.notation_couche() 
            if utile.params.couches else ''
        )
        + (
            "\n Configuration électronique: %s" % self.notation_configuration()
            if utile.params.configuration else ''
        )
    )

Atome.__str__ = __str


def __repr(self):
    return self.notation_symbole()

Atome.__repr__ = __repr


def __hash(self):
    return hash(repr(self))

Atome.__hash__ = __hash


def __eq(self, obj):
    return repr(self) == repr(obj)

Atome.__eq__ = __eq


def notation(self):
    return "%s Z=%s A=%s" % (
        self.symbole, self.proton, self.proton + self.neutron
    ) 

Atome.notation = notation


def notation_symbole(self, A=True, Z=True):
    return "%s%s%s" % (
        ''.join(
            utile.exposants[int(num)] 
            for num in str(self.proton + self.neutron)
        ) if A else '',
        ''.join(
            utile.sous_exposants[int(num)] 
            for num in str(self.proton)
        ) if Z else '',
        self.symbole
    )

Atome.notation_symbole = notation_symbole


Atome.notation_couche = utile.notation_couche

Atome.notation_configuration = utile.notation_configuration


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

            _masse_neutrons = utile.masse_neutron * self.neutron
            _masse_protons = utile.masse_proton * self.proton
            _masse_neutrons_protons = _masse_neutrons + _masse_protons
            _masse_neutrons_protons_m_total = self.masse - _masse_neutrons_protons

            demo = [
            e + "(Masse de l'Atome - (Masse neutron x Nombre neutron + Masse proton x Nombre proton)) / Masse électron",
            e + "(%s - (%s x %s + %s x %s)) / %s" % (self.masse, utile.masse_neutron, self.neutron, 
                                                     utile.masse_proton, self.proton, utile.masse_électron),
            e + "(%s - (%s + %s)) / %s" % (self.masse, _masse_neutrons, _masse_protons, utile.masse_électron),
            e + "(%s - %s) / %s" % (self.masse, _masse_neutrons_protons, utile.masse_électron),
            e + "%s / %s" % (_masse_neutrons_protons_m_total, utile.masse_électron),
            e + "%s" % round(_masse_neutrons_protons_m_total / utile.masse_électron)
            ]

    if recup == 'neutron':

        if avec == 'masse':

            e = "Neutron %s = " % self.notation_symbole()

            demo = [
            e + "(Masse de l'Atome - (Masse électron x Nombre électron + Masse proton x Nombre proton)) / Masse neutron",
            e + "(%s - (%s x %s + %s x %s)) / %s" % (self.masse, utile.masse_électron, self.électron, 
                                                     utile.masse_proton, self.proton, masse_neutron),
            e + "(%s - (%s + %s)) / %s" % (self.masse, utile.masse_électron * self.électron, 
                                           utile.masse_proton * self.proton, masse_neutron),
            e + "(%s - %s) / %s" % (self.masse, utile.masse_électron * self.neutron + utile.masse_proton * self.proton, 
                                    masse_neutron),
            e + "%s / %s" % (self.masse - (utile.masse_électron * self.électron + utile.masse_proton * self.proton), 
                             masse_neutron),
            e + "%s" % round((self.masse - (utile.masse_électron * self.électron + utile.masse_proton * self.proton)) / masse_neutron)
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
            e + "(%s - (%s x %s + %s x %s)) / %s" % (self.masse, utile.masse_neutron, self.neutron, 
                                                     utile.masse_électron, self.électron, utile.masse_proton),
            e + "(%s - (%s + %s)) / %s" % (self.masse, utile.masse_neutron * self.neutron, 
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

Atome.demonstration = demonstration