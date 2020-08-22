"""

Objet ion.

---------
Arguments

valeur
    :Atome
        Transforme l'atome en ion.
    :Ion
        Léve une erreur
    :int
        Equivaut au nombre de proton et créer un ion.

-------
Retours

:Ion
    .element:str
    .symbole:str
    .categorie:str

    .proton:int
    .neutron:int
    .electron:int
    .nucleon:int

    .masse:float
    .masse_atomique_relative:float

    .couches:list
    .configuration:list

    .diff:int
        Différence entre le nombre de proton et d'électron
    .charge:str
        Charges électrique de l'ion

    .notation()
    .notation_symbole()
    .notation_couche()
    .notation_configuration()
"""

from .. import utile
from .. import exception

from .base import Molecule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur=1, electron=0, neutron=None):

    self.neutron = neutron

    utile.get_info(self, valeur)


    drn_couche = self.couches[-1]

    if 0 < drn_couche < 5:
        self.electron = self.proton - drn_couche
        self.charge = '+'
        del self.couches[-1]

    elif 4 < drn_couche < 8:
        self.electron = self.proton + (8 - drn_couche)
        self.charge = '-'
        self.couches[-1] = 8

    else:
        raise exception.ValeurIncorrecte(
            "Un gaz noble ne peut pas devenir un Ion."
        )


    if self.neutron is None:
        self.neutron = round(self.masse_atomique_relative) - self.proton

    self.diff = abs(self.proton - self.electron)

    self.masse = utile.get_masse(self)

    self.nucleon = self.proton + self.neutron

    self.configuration = utile.configuration_electronique(self)

Ion.__init__ = __init


def __add(self, obj):

    if isinstance(obj, Proton):
        return Ion(self.proton + obj.valeur)

    else:
        raise exception.Incompatible(self, obj)

Ion.__add__ = __add


def __iadd(self, obj):
    return self + obj

Ion.__iadd__ = __iadd


def __sub(self, obj):

    if isinstance(obj, Proton):
        return Atome(self.proton - obj.valeur)

    else:
        raise exception.Incompatible(self, obj)

Ion.__sub__ = __sub


def __isub(self, obj):
    return self - obj

Ion.__isub__ = __isub


def __str(self): 
    str__ = (
        "Ion %s" % self.notation()
        + (
            "\n Elément: %s" % self.element[utile.params.langue] 
            if utile.params.element else ''
        )
        + (
            "\n Catégorie: %s" % self.categorie[utile.params.langue] 
            if utile.params.categorie else ''
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
            "\n Electron(s): %s" % self.electron 
            if utile.params.electron else ''
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

    return (
        str__ if not utile.params.calculatrice
        else
            str__.replace('è', 'e').replace('é', 'e')
    )

Ion.__str__ = __str


def __repr(self):
    return self.notation_symbole()

Ion.__repr__ = __repr


def notation(self):
    return "%s %s%s Z=%s A=%s" % (
        self.symbole, 
        self.diff, 
        self.charge, 
        self.proton, 
        self.proton + self.neutron
    )

Ion.notation = notation


def notation_symbole(self, A=True, Z=True):
    return "%s%s%s%s%s" % (
        '' if not A or utile.params.calculatrice
        else
            ''.join(
                utile.exposants[int(num)] 
                for num in str(self.proton + self.neutron)
            )
        ,
        '' if not Z or utile.params.calculatrice
        else
            ''.join(
                utile.sous_exposants[int(num)] 
                for num in str(self.proton)
            )
        ,
        self.symbole
        ,
        nbr if utile.params.calculatrice
        else
            ''.join(
                utile.exposants[int(num)] 
                for num in str(self.diff)
            )
        ,
        {
            '-': '⁻' if not utile.params.calculatrice else '-',
            '+': '⁺' if not utile.params.calculatrice else '+'
        }.get(self.charge)
    )

Ion.notation_symbole = notation_symbole


Ion.notation_couche = utile.notation_couche

Ion.notation_configuration = utile.notation_configuration