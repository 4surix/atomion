# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from __future__ import annotations

from typing import Any, Optional, Union

from .. import exception, objets, utile


class Electron:

    __slots__ = ('valeur',)

    def __init__(self, valeur:Optional[Union[objets.Atome, objets.Ion, int]] = 1) -> None:

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
        return self.notation_symbole()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __mul__(self, obj: int) -> Electron:
        return Electron(self.valeur * obj)

    def __rmul__(self, obj: int) -> Electron:
        return self * obj

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%se%s" % (
            '' if self.valeur == 1 else self.valeur
            ,
            utile.affichage.signe('-')
        )
