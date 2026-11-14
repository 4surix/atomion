# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objet Electron : particule subatomique à charge négative."""

from __future__ import annotations

from typing import Any, Optional, Union

from .. import exception, objets, utile


class Electron:
    """Un électron, particule subatomique à charge négative."""

    __slots__ = ('valeur',)

    def __init__(
        self, valeur: Optional[Union[objets.Atome, objets.Ion, int]] = 1
    ) -> None:
        """Initialise un électron à partir d'une valeur.

        Args:
            valeur: Atome, Ion ou entier représentant le nombre d'électrons.
        """
        if isinstance(valeur, (objets.Atome, objets.IonMonoAtomique, objets.IonPolyAtomique)):
            self.valeur = valeur.electron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Electron'."
            )

    def __repr__(self) -> str:
        """Représentation symbolique de l'électron."""
        return self.notation_symbole()

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:  # noqa: ANN401
        """Compare deux électrons par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def __mul__(self, obj: int) -> Electron:
        """Multiplie le nombre d'électrons par un entier."""
        return Electron(self.valeur * obj)

    def __rmul__(self, obj: int) -> Electron:
        """Multiplication à gauche par un entier."""
        return self * obj

    def notation_symbole(
        self, *args: Any,  # noqa: ANN401
        A: bool = True, Z: bool = True
    ) -> str:
        """Notation symbolique de l'électron (ex: 'e⁻' ou '2e⁻')."""
        return "%se%s" % (
            '' if self.valeur == 1 else self.valeur
            ,
            utile.affichage.signe('-')
        )
