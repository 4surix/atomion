# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objet Proton : particule subatomique à charge positive."""

from __future__ import annotations

from typing import Any, Optional, Union

from .. import exception, objets, utile


class Proton:
    """Un proton, particule subatomique à charge positive."""

    __slots__ = ('valeur',)

    def __init__(
        self,
        valeur: Optional[Union[objets.Atome, objets.IonMonoAtomique, int]] = 1,
    ) -> None:
        """Initialise un proton à partir d'une valeur.

        Args:
            valeur: Atome, IonMonoAtomique ou entier représentant le nombre de protons.
        """
        if isinstance(valeur, (objets.Atome, objets.IonMonoAtomique)):
            self.valeur = valeur.proton

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Proton'."
            )

    def __repr__(self) -> str:
        """Représentation symbolique du proton."""
        return self.notation_symbole()

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        """Compare deux protons par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def __add__(
        self, obj: Union[Proton, objets.Neutron]
    ) -> Union[Proton, objets.Noyau]:
        """Additionne un proton ou un neutron."""
        if isinstance(obj, Proton):
            return Proton(self.valeur + obj.valeur)

        elif isinstance(obj, objets.Neutron):
            return objets.Noyau(self, obj)

        else:
            raise exception.Incompatible(self, obj)

    def __mul__(self, obj: int) -> Proton:
        """Multiplie le nombre de protons par un entier."""
        return Proton(self.valeur * obj)

    def __rmul__(self, obj: int) -> Proton:
        """Multiplication à gauche par un entier."""
        return self * obj

    def notation_symbole(
        self, *args: Any,
        A: bool = True, Z: bool = True
    ) -> str:
        """Notation symbolique du proton (ex: '1p+')."""
        return "{}{}p{}".format(
            '' if not A else utile.affichage.nombre_de_masse(self.valeur)
            ,
            '' if not Z else utile.affichage.numero_atomique(self.valeur)
            ,
            utile.affichage.signe('+')
        )
