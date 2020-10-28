# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import exception

from ..utile.typing import Union, Any, Optional


class Neutron:
    """
    ### &doc_id particule:neutron
    """

    __slots__ = ('valeur')

    def __init__(self, valeur:Optional[int] = 1) -> None:

        if isinstance(valeur, (Atome, Ion)):
            self.valeur = valeur.neutron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Neutron'."
            )

    def __repr__(self) -> str:
        return 'Neutron(%s)' % self.valeur

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

objets.Neutron = Neutron


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)