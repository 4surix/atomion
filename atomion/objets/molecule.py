"""

Objet molécule.

---------
Arguments

valeur
    :str
        Notation de la Molécule qui sera décodée.

------
Retour

:Molécule
    .atomes:list
        Liste de tout les :Atomes composant la molécule.

    .proton:int
        Nombre total de proton dans la molécule.
    .neutron:int
        Nombre total de neutron dans la molécule.
    .électron:int
        Nombre total d'électron dans la molécule.
    .nucléon:int
        Nombre total de nucléon dans la molécule.

    .masse:float
    .masse_moléculaire_relative:float
"""

import copy

from .. import utile

from .base import Molécule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur):

    self.atomes = utile.convertie_notation_vers_atomes(valeur) if isinstance(valeur, str) else valeur

    if len(self.atomes) < 2:
        raise Exception("Une Molécule doit être composée de plusieurs atome.")

    utile.verif_stable(self)

    self.proton = sum(atome.proton for atome in self.atomes)
    self.neutron = sum(atome.neutron for atome in self.atomes)
    self.électron = sum(atome.électron for atome in self.atomes)

    self.masse = sum(atome.masse for atome in self.atomes)
    self.masse_moléculaire_relative = sum(atome.masse_atomique_relative for atome in self.atomes)

Molécule.__init__ = __init


def __str(self):

    return  (   "Molécule %s" % self.notation()
            +("\n Proton(s): %s" % self.proton if utile.params.proton else '')
            +("\n Neutron(s): %s" % self.neutron if utile.params.neutron else '')
            +("\n Electron(s): %s" % self.électron if utile.params.électron else '')
            +("\n Masse: %s" % self.masse if utile.params.masse else '')
            +("\n Masse moléculaire relative: %s" % self.masse_moléculaire_relative if utile.params.masse_relative else '')
            )

Molécule.__str__ = __str


def __repr(self):
    return self.notation()

Molécule.__repr__ = __repr


def __add(self, obj):

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

Molécule.__add__ = __add


def __iadd(self, obj):
    return self + obj

Molécule.__iadd__ = __iadd


def __sub(self, obj):

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

Molécule.__sub__ = __sub


def __isub(self, obj):
    return self - obj

Molécule.__isub__ = __isub


def notation(self):

    atomes = {}

    for atome in self.atomes:
        atome = atome.notation_symbole(A=False, Z=False)
        if atome not in atomes:
            atomes[atome] = 0
        atomes[atome] += 1

    return ''.join(
        '%s%s' % (
            atome, 
            ''.join(
                utile.sous_exposants[int(num)] 
                for num in str(nbr)
            ) if nbr != 1 else ''
        ) 
        for atome, nbr in atomes.items()
    )

Molécule.notation = notation