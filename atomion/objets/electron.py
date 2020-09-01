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


class Electron:
    """
    ### &doc_id particule:electron
    """

    __slots__ = ('valeur')

    def __init__(self, valeur:Optional[int] = 1) -> None:

        if isinstance(valeur, (Atome, Ion)):
            self.valeur = valeur.electron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Electron'."
            )

    def __repr__(self) -> str:
        return 'Electron(%s)' % self.valeur

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

objets.Electron = Electron


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)