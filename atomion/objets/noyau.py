# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from .. import objets
from ..objets import (
    Atome, IonMonoAtomique,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional


###>>> CAPTURE FICHIER CALC

class Noyau:

    __slots__ = ('proton', 'neutron')

    def __init__(self, proton, neutron):

        self.proton = proton
        self.neutron = neutron

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __add__(self, obj):

        if isinstance(obj, Electron):

            if obj.valeur != self.proton.valeur:
                return IonMonoAtomique(
                    self.proton.valeur,
                    neutron = self.neutron.valeur,
                    charge = self.proton.valeur - obj.valeur
                )

            else:
                return Atome(
                    self.proton.valeur,
                    neutron = self.neutron.valeur
                )

        elif isinstance(obj, Proton):
            self.proton.valeur += obj.valeur
            return self

        elif isinstance(obj, Neutron):
            self.neutron.valeur += obj.valeur
            return self

        else:
            raise exception.Incompatible(self, obj)

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%s%sX" % (
            '' if not A or utile.params.calculatrice
            else
                ''.join(
                    utile.exposants[int(num)] 
                    for num in str(
                        self.neutron.valeur + self.proton.valeur
                    )
                )
            ,
            '' if not Z or utile.params.calculatrice
            else
                ''.join(
                    utile.sous_exposants[int(num)] 
                    for num in str(self.proton.valeur)
                )
        )

###<<< CAPTURE FICHIER CALC

objets.Noyau = Noyau


def MAJ_TYPE():
    variables = globals()
    for objet_nom in objets.listes_noms:
        variables[objet_nom] = getattr(objets, objet_nom)