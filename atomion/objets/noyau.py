# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from .. import objets
from ..objets import (
    Atome, IonMonoAtomique,
    Noyau,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional, List


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

    def __lshift__(self, obj:Noyau) -> List[ Union[Noyau, Neutron] ]:
        # Fusion

        if isinstance(obj, Noyau):

            int; protons = self.proton.valeur + obj.proton.valeur
            int; neutrons = self.neutron.valeur + obj.neutron.valeur

            nouvelles_especes = [] 

            atome = Atome(protons)
            neutrons -= atome.neutron

            nouvelles_especes.append(atome.noyau)

            if neutrons < 0:
                # On retire les neutrons en trop.
                # Noyau(2, 1) << Noyau(2, 2) == Noyau(4, 3)
                atome.noyau.neutron.valeur += neutron

            elif neutrons > 0:
                # On rajoute les neutrons qui ne sont pas 
                #  dans le nouveau noyau mais qui étaient là de base.
                # Noyau(2, 3) << Noyau(2, 2) == [Neutron(), Noyau(4, 4)]
                nouvelles_especes.append(Neutron(neutrons))

            return nouvelles_especes

        else:
            raise exception.Incompatible(self, obj)

    def __rshift__(self, obj):
        # Fission
        return NotImplemented

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