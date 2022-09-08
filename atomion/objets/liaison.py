# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome
)
from .. import utile
from .. import exception

from ..utile.typing import List, Any, Optional


###>>> CAPTURE FICHIER CALC

class Liaison:

    __slots__ = (
        'atomes',
        'polarisee'
    )

    def __init__(self, 
            *valeurs:List[Atome],
            neutron:Optional[int] = None
        ) -> None:

        self.atomes = valeurs

        if len(self.atomes) != 2:
            raise exception.ValeurIncorrecte(
                "Une liaison doit être composée de deux atomes."
            )

        self.polarisee = (
            abs(self.atomes[0].electronegativite - self.atomes[1].electronegativite) > 0.4
        )

    def __iter__(self):

        for atome in self.atomes:
            yield atome


###<<< CAPTURE FICHIER CALC


objets.Liaison = Liaison

def MAJ_TYPE():
    variables = globals()
    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)