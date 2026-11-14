# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objets de physique des particules : Quark, QUp, QDown, BiQuark."""

from __future__ import annotations

try:
    import random
except ImportError:
    # MicroPython 1.9.4 : le module s'appelle `urandom`
    #  (et n'expose que `getrandbits()` / `seed()`).
    import urandom as random


from typing import Any, List, Optional, Union

from .. import exception, objets


CHARGES_ELECTRIQUES: list[float] = [
    -1 / 3,
    +2 / 3,
]
CHARGES_COULEURS: dict[str, int] = {
    'R': 1,
    'V': 2,
    'B': 3,
}
COULEURS: tuple[str, ...] = ('R', 'V', 'B')


def couleur_aleatoire() -> str:
    """Retourne une couleur aleatoire ('R', 'V' ou 'B').

    `getrandbits()` est la seule primitive disponible a la fois sur CPython
     et sur MicroPython 1.9.4.
    """
    return COULEURS[random.getrandbits(8) % len(COULEURS)]


class Quark:
    """Un quark, particule élémentaire de la matière."""

    __slots__ = ('charge_electrique', 'charge_couleur')

    def __init__(
        self, charge_electrique: float, charge_couleur: str
    ) -> None:
        """Initialise un quark avec sa charge électrique et sa couleur.

        Args:
            charge_electrique: Doit être +2/3 ou -1/3.
            charge_couleur: Doit être 'R', 'V' ou 'B'.
        """
        if charge_electrique not in CHARGES_ELECTRIQUES:
            raise exception.ValeurIncorrecte(
                'La charge electrique doit être + 2/3 ou - 1/3.'
            )

        charge_couleur = CHARGES_COULEURS.get(
            charge_couleur, charge_couleur
        )
        if charge_couleur not in CHARGES_COULEURS.values():
            raise exception.ValeurIncorrecte(
                'La charge de couleur doit être R, V ou B.'
            )

        self.charge_electrique = charge_electrique
        self.charge_couleur = charge_couleur

    def __repr__(self) -> str:
        """Représentation symbolique du quark."""
        return self.notation_symbole()

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:  # noqa: ANN401
        """Compare deux quarks par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def __add__(self, obj: Quark) -> BiQuark:
        """Additionne deux quarks pour former un BiQuark."""
        if isinstance(obj, Quark):
            return BiQuark([self, obj])

        else:
            raise exception.Incompatible(self, obj)

    def notation_symbole(self) -> str:
        """Symbole du quark ('u' pour up, 'd' pour down)."""
        if self.charge_electrique == +2 / 3:
            return 'u'

        if self.charge_electrique == -1 / 3:
            return 'd'

        raise exception.ValeurIncorrecte(
            "La charge électrique d'un quark doit être + 2/3 ou - 1/3."
        )


class QUp(Quark):
    """Quark up (charge électrique +2/3)."""

    def __init__(self, charge_couleur: Optional[str] = None) -> None:
        """Initialise un quark up avec une couleur optionnelle.

        Args:
            charge_couleur: Couleur ('R', 'V', 'B') ou None pour aléatoire.
        """
        Quark.__init__(
            self,
            +2 / 3,
            charge_couleur if charge_couleur
            else
                couleur_aleatoire()
        )


class QDown(Quark):
    """Quark down (charge électrique -1/3)."""

    def __init__(self, charge_couleur: Optional[str] = None) -> None:
        """Initialise un quark down avec une couleur optionnelle.

        Args:
            charge_couleur: Couleur ('R', 'V', 'B') ou None pour aléatoire.
        """
        Quark.__init__(
            self,
            -1 / 3,
            charge_couleur if charge_couleur
            else
                couleur_aleatoire()
        )


class BiQuark:
    """Un biquark, composé de deux quarks."""

    __slots__ = ('quarks',)

    def __init__(self, quarks: List[Quark]) -> None:
        """Initialise un biquark avec une liste de quarks.

        Args:
            quarks: Liste des quarks composant le biquark.
        """
        self.quarks = quarks

    def __repr__(self) -> str:
        """Représentation symbolique du biquark."""
        return 'BiQuark{%s}' % self.quarks

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:  # noqa: ANN401
        """Compare deux biquarks par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def __add__(
        self, obj: Quark
    ) -> Union[objets.Neutron, objets.Proton]:
        """Additionne un quark pour former un hadron (neutron ou proton)."""
        if isinstance(obj, Quark):

            value = sum(
                (quark.charge_electrique for quark in self.quarks),
                obj.charge_electrique,
            )

            if value == 0:
                hadron = objets.Neutron()

            elif value == 1:
                hadron = objets.Proton()

            else:
                raise exception.Instable(self)

            if 14 - sum(
                (quark.charge_couleur ** 2 for quark in self.quarks),
                obj.charge_couleur ** 2,
            ) != 0:
                raise exception.Instable(hadron)

            return hadron

        else:
            raise exception.Incompatible(self, obj)
