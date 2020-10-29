# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

###>>> CAPTURE FICHIER CALC

import random

###<<< CAPTURE FICHIER CALC


from .. import objets
from ..objets import (
    Proton, Neutron
)
from .. import exception

from ..utile.typing import Union, Any, Optional, List


###>>> CAPTURE FICHIER CALC

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
        return self.notation_symbole()

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __add__(self, obj):

        if isinstance(obj, (QUp, QDown)):
            return BiQuark([self, obj])

        else:
            raise exception.Incompatible(self, obj)

    def notation_symbole(self) -> str:

        if self.charge_electrique == + 2/3:
            return 'u'

        if self.charge_electrique == - 1/3:
            return 'd'

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


class BiQuark:

    __slots__ = ('quarks')

    def __init__(self, quarks:List[Quark]):

        self.quarks = quarks

    def __repr__(self) -> str:
        return 'BiQuark{%s}' % self.quarks

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __add__(self, 
            obj:Union[QUp, QDown]
        ) -> Union[Neutron, Proton]:

        if isinstance(obj, (QUp, QDown)):

            value = sum(
                (quark.charge_electrique for quark in self.quarks),
                obj.charge_electrique
            )

            if value == 0:
                hadron = Neutron()

            elif value == 1:
                hadron = Proton()

            else:
                raise exception.Instable(self)

            if 14 - sum(
                (quark.charge_couleur **2 for quark in self.quarks),
                obj.charge_couleur **2
            ) != 0:
                raise exception.Instable(hadron)

            return hadron

        else:
            raise exception.Incompatible(self, obj)

###<<< CAPTURE FICHIER CALC


def MAJ_TYPE():
    variables = globals()
    for objet_nom in objets.listes_noms:
        variables[objet_nom] = getattr(objets, objet_nom)