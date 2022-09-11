# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, Ion
)
from .. import utile
from .. import exception

from ..utile.typing import List, Union, Any, Optional


###>>> CAPTURE FICHIER CALC

class Liaison:

    __slots__ = (
        'atomes',
        'polarisee',
        'pole_moins', 'pole_plus'
    )

    def __init__(self, 
            *valeurs:List[Union[str, Atome, Ion]],
            neutron:Optional[int] = None
        ) -> None:

        self.atomes = [
            utile.convertie_notation(element.strip()) if isinstance(element, str)
            else
                element
            for element in valeurs
        ]

        if len(self.atomes) != 2:
            raise exception.ValeurIncorrecte(
                "Une liaison doit être composée de deux atomes."
            )

        self.polarisee = (
            abs(self.atomes[0].electronegativite - self.atomes[1].electronegativite) > 0.4
        )

        if self.atomes[0].electronegativite > self.atomes[1].electronegativite:
            self.pole_moins = self.atomes[0]
            self.pole_plus = self.atomes[1]
        else:
            self.pole_moins = self.atomes[1]
            self.pole_plus = self.atomes[0]

    def __iter__(self):

        for atome in self.atomes:
            yield atome

    def __str__(self):

        return (
            self.atomes[0].symbole + (
                '' if not self.polarisee else ('ᵟ' + (
                    '⁻' if self.atomes[0].electronegativite > self.atomes[1].electronegativite
                    else
                        '⁺'
                ))
            )
            + ' ── ' +
            self.atomes[1].symbole + (
                '' if not self.polarisee else ('ᵟ' + (
                    '⁻' if self.atomes[0].electronegativite < self.atomes[1].electronegativite
                    else
                        '⁺'
                ))
            )
        )


###<<< CAPTURE FICHIER CALC


objets.Liaison = Liaison

def MAJ_TYPE():
    variables = globals()
    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)