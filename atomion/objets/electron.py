# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional


###>>> CAPTURE FICHIER CALC

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
        return self.notation_symbole()

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%se%s" % (
            '' if self.valeur == 1 else self.valeur
            ,
            '-' if utile.params.calculatrice else '⁻'
        )

###<<< CAPTURE FICHIER CALC

objets.Electron = Electron


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)