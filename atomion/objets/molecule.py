"""

Objet Molecule.

---------
Arguments

valeur
    :str
        Notation de la molécule qui sera decodée.

------
Retour

:Molecule
    .atomes:list
        Liste de tout les :Atomes composant la Molecule.

    .proton:int
        Nombre total de proton dans la molécule.
    .neutron:int
        Nombre total de neutron dans la molécule.
    .electron:int
        Nombre total d'électron dans la molécule.
    .nucleon:int
        Nombre total de nucléon dans la molécule.

    .masse:float
    .masse_moleculaire_relative:float

    .notation()
"""

from .. import utile
from .. import exception

from .base import Molecule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur):

    self.atomes = (
        utile.convertie_notation_vers_atomes(valeur) 
        if isinstance(valeur, str) else valeur
    )

    if len(self.atomes) < 2:
        raise exception.ValeurIncorrecte(
            "Une molécule doit être composée de plusieurs atomes."
        )

    utile.verif_stable(self)

    self.proton = sum(atome.proton for atome in self.atomes)
    self.neutron = sum(atome.neutron for atome in self.atomes)
    self.electron = sum(atome.electron for atome in self.atomes)

    self.masse = sum(atome.masse for atome in self.atomes)
    self.masse_moleculaire_relative = sum(
        atome.masse_atomique_relative 
        for atome in self.atomes
    )

Molecule.__init__ = __init


def __str(self):

    str__ = (
        "Molécule %s" % self.notation()
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
            "\n Masse moléculaire relative: %s"
            % (self.masse_moleculaire_relative)
            if utile.params.masse_relative else ''
        )
    )

    return (
        str__ if not utile.params.calculatrice
        else
            str__.replace('è', 'e').replace('é', 'e')
    )

Molecule.__str__ = __str


def __repr(self):
    return self.notation()

Molecule.__repr__ = __repr


def __add(self, obj):

    if isinstance(obj, Molecule):

        atomes = self.atomes[:]
        atomes.extend(obj.atomes)
        return Molecule(atomes)

    elif isinstance(obj, Atome):

        atomes = self.atomes[:]
        atomes.append(obj)
        return Molecule(atomes)

    else:
        raise exception.Incompatible(self, obj)

Molecule.__add__ = __add


def __iadd(self, obj):
    return self + obj

Molecule.__iadd__ = __iadd


def __sub(self, obj):

    if isinstance(obj, Molecule):

        atomes = self.atomes[:]
        for atome in obj.atomes:
            atomes.remove(atome)
        return Molecule(atomes)

    elif isinstance(obj, Atome):

        atomes = self.atomes[:]
        atomes.remove(obj)
        return Molecule(atomes)

    else:
        raise exception.Incompatible(self, obj)

Molecule.__sub__ = __sub


def __isub(self, obj):
    return self - obj

Molecule.__isub__ = __isub


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
            '' if nbr == 1
            else
                nbr if not utile.params.calculatrice
                else
                    ''.join(
                        utile.sous_exposants[int(num)] 
                        for num in str(nbr)
                    )
        )
        for atome, nbr in atomes.items()
    )

Molecule.notation = notation