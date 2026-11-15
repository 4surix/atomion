# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objet Neutron : particule subatomique neutre."""

from __future__ import annotations

from typing import Any, Optional, Union

from .. import exception, objets, utile


class Neutron:
    """Un neutron, particule subatomique neutre."""

    __slots__ = ('valeur',)

    def __init__(self, valeur: Optional[int] = 1) -> None:
        """Initialise un neutron à partir d'une valeur.

        Args:
            valeur: Atome, IonMonoAtomique ou entier représentant le nombre de neutrons.
        """
        if isinstance(valeur, (objets.Atome, objets.IonMonoAtomique)):
            self.valeur = valeur.neutron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Neutron'."
            )

    def __repr__(self) -> str:
        """Représentation symbolique du neutron."""
        return self.notation_symbole()

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        """Compare deux neutrons par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def __add__(
        self, obj: Union[Neutron, objets.Proton]
    ) -> Union[Neutron, objets.Noyau]:
        """Additionne un neutron ou un proton."""
        if isinstance(obj, Neutron):
            return Neutron(self.valeur + obj.valeur)

        elif isinstance(obj, objets.Proton):
            return objets.Noyau(obj, self)

        else:
            raise exception.Incompatible(self, obj)

    def __mul__(self, obj: int) -> Neutron:
        """Multiplie le nombre de neutrons par un entier."""
        return Neutron(self.valeur * obj)

    def __rmul__(self, obj: int) -> Neutron:
        """Multiplication à gauche par un entier."""
        return self * obj

    def notation_symbole(
        self, *args: Any,
        A: bool = True, Z: bool = True
    ) -> str:
        """Notation symbolique du neutron (ex: '1n0')."""
        return "{}{}n{}".format(
            '' if not A else utile.affichage.nombre_de_masse(self.valeur)
            ,
            '' if not Z else utile.affichage.numero_atomique(0)
            ,
            utile.affichage.signe('0')
        )
