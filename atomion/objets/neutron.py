# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, IonMonoAtomique,
    Proton, Neutron,
    Noyau
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional


###>>> CAPTURE FICHIER CALC

class Neutron:

    __slots__ = ('valeur')

    def __init__(self, valeur:Optional[int] = 1) -> None:

        if isinstance(valeur, (Atome, IonMonoAtomique)):
            self.valeur = valeur.neutron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Neutron'."
            )

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __add__(self, 
            obj: Union[Neutron, Proton]
        ) -> Union[Neutron, Noyau]:

        if isinstance(obj, Neutron):
            return Neutron(self.valeur + obj.valeur)

        elif isinstance(obj, Proton):
            return Noyau(obj, self)

        else:
            raise exception.Incompatible(self, obj)

    def __mul__(self, obj: int) -> Neutron:
        return Neutron(self.valeur * obj)

    def __rmul__(self, obj: int) -> Neutron:
        return self * obj

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%s%sn%s" % (
            '' if not A or utile.params.calculatrice
            else
                ''.join(
                    utile.exposants[int(num)] 
                    for num in str(self.valeur)
                )
            ,
            '' if not Z or utile.params.calculatrice
            else
                utile.sous_exposants[0]
            ,
            '' if utile.params.calculatrice else utile.exposants[0]
        )

###<<< CAPTURE FICHIER CALC

objets.Neutron = Neutron


def MAJ_TYPE():
    variables = globals()
    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)