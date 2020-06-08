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
    .élément:str
    .symbole:str
    .catégorie:str

    .proton:int
    .neutron:int
    .électron:int
    .nucléon:int

    .masse:float
    .masse_atomique_relative:float

    .couches:list
    .configuration:list

    .diff:int
        Différence entre le nombre de proton et d'électron
    .charge:str
        Charges électrique de l'ion
"""

from .. import utile

from .base import Molécule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur=1, électron=0, neutron=None):

    self.neutron = neutron

    utile.get_info(self, valeur)


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

    self.masse = utile.get_masse(self)

    self.nucléon = self.proton + self.neutron

    self.configuration = utile.configuration_électronique(self)

Ion.__init__ = __init


def __add(self, obj):

    if isinstance(obj, Proton):
        return Ion(self.proton + obj.valeur)

    else:
        raise Exception("Type '%s' non compatible avec type 'Atome'." % type(obj))

Ion.__add__ = __add


def __iadd(self, obj):
    return self + obj

Ion.__iadd__ = __iadd


def __sub(self, obj):

    if isinstance(obj, Proton):
        return Atome(self.proton - obj.valeur)

    else:
        raise Exception("Type '%s' non compatible avec type 'Atome'." % type(obj))

Ion.__sub__ = __sub


def __isub(self, obj):
    return self - obj

Ion.__isub__ = __isub


def __str(self): 
    return  (  "Ion %s" % self.notation()
            +("\n Elément: %s" % self.élément[utile.params.langue] if utile.params.élément else '')
            +("\n Catégorie: %s" % self.catégorie[utile.params.langue] if utile.params.catégorie else '')
            +("\n Proton(s): %s" % self.proton if utile.params.proton else '')
            +("\n Neutron(s): %s" % self.neutron if utile.params.neutron else '')
            +("\n Electron(s): %s" % self.électron if utile.params.électron else '')
            +("\n Masse: %s" % self.masse if utile.params.masse else '')
            +("\n Masse atomique relative: %s" % self.masse_atomique_relative if utile.params.masse_relative else '')
            +("\n Couche électronique: %s" % self.notation_couche() if utile.params.couches else '')
            +("\n Configuration électronique: %s" % self.notation_configuration() if utile.params.configuration else '')
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
        ''.join(
            utile.exposants[int(num)] 
            for num in str(self.proton + self.neutron)
        ) if A else '',
        ''.join(
            utile.sous_exposants[int(num)] 
            for num in str(self.proton)
        ) if Z else '',
        self.symbole,
        ''.join(
            utile.exposants[int(num)] 
            for num in str(self.diff)
        ),
        {'-':'⁻', '+':'⁺'}.get(self.charge)
    )

Ion.notation_symbole = notation_symbole


def notation_couche(self):
    couches = [
        ''.join(
            utile.exposants[int(num)] 
            for num in str(électron)
        )
        for électron in self.couches
    ]
    return ' '.join('(%s)%s' % r for r in zip(utile.notations_couche, couches))

Ion.notation_couche = notation_couche


def notation_configuration(self):
    return ' '.join(
        '%s%s' % (
            notation, 
            ''.join(
                utile.exposants[int(num)] 
                for num in str(électron)
            )
        )
        for notation, électron in zip(
            utile.notation_configuration_ion, 
            self.configuration
        ) 
        if électron
    )

Ion.notation_configuration = notation_configuration