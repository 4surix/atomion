# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from .. import exception, objets, utile
from ..objets import Atome, Electron, Ion, IonMonoAtomique, IonPolyAtomique
from ..utile.typing import Any, Optional, Union

###>>> CAPTURE FICHIER CALC

class Electron:

    __slots__ = ('valeur',)

    def __init__(self, valeur:Optional[Union[Atome, Ion, int]] = 1) -> None:

        if isinstance(valeur, (Atome, IonMonoAtomique, IonPolyAtomique)):
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
            '-' if utile.params.calculatrice else '⁻'
        )

###<<< CAPTURE FICHIER CALC

objets.Electron = Electron


def MAJ_TYPE():
    variables = globals()
    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)
