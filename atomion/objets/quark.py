# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


import random


from .. import objets
from ..objets import (
	Proton, Neutron
)
from .. import exception

from ..utile.typing import Union, Any, Optional


CHARGES_ELECTRIQUES = [
    - 1/3,
    + 2/3
]
CHARGES_COULEURS = {
    'R': 1,
    'V': 2,
    'B': 3
}


class Quark:

    __slots__ = ('charge_electrique', 'charge_couleur')

    def __init__(self, charge_electrique, charge_couleur):

        if charge_electrique not in CHARGES_ELECTRIQUES:
            raise exception.ValeurIncorrecte(
            	'La charge electrique doit être + 2/3 ou - 1/3.'
            )

        charge_couleur = CHARGES_COULEURS.get(
            charge_couleur, charge_couleur
        )
        if charge_couleur not in CHARGES_COULEURS.values():
            raise exception.ValeurIncorrecte(
            	'La charge electrique doit être R, V ou B.'
            )

        self.charge_electrique = charge_electrique
        self.charge_couleur = charge_couleur

    def __repr__(self) -> str:
        return 'Quark{%s, %s}' % (
            self.charge_electrique,
            self.charge_couleur
        )

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

objets.Quark = Quark


class QUp(Quark):

    def __init__(self, charge_couleur:str = None):

        Quark.__init__(
            self, 
            + 2/3, 
            charge_couleur if charge_couleur
            else
                random.choice(CHARGES_COULEURS.values())
        )

objets.QUp = QUp


class QDown(Quark):

    def __init__(self, charge_couleur:str = None):

        Quark.__init__(
            self, 
            - 1/3, 
            charge_couleur if charge_couleur
            else
                random.choice(CHARGES_COULEURS.values())
        )

objets.QDown = QDown


def MAJ_TYPE():
    variables = globals()
    for objet_nom in objets.listes_noms:
        variables[objet_nom] = getattr(objets, objet_nom)