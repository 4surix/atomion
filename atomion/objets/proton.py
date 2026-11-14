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


class Proton:

    __slots__ = ('valeur',)

    def __init__(self, valeur:Optional[Union[objets.Atome, objets.IonMonoAtomique, int]] = 1) -> None:

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
        return self.notation_symbole()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __add__(self,
            obj: Union[Proton, objets.Neutron]
        ) -> Union[Proton, objets.Noyau]:

        if isinstance(obj, Proton):
            return Proton(self.valeur + obj.valeur)

        elif isinstance(obj, objets.Neutron):
            return objets.Noyau(self, obj)

        else:
            raise exception.Incompatible(self, obj)

    def __mul__(self, obj: int) -> Proton:
        return Proton(self.valeur * obj)

    def __rmul__(self, obj: int) -> Proton:
        return self * obj

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%s%sp%s" % (
            '' if not A else utile.affichage.nombre_de_masse(self.valeur)
            ,
            '' if not Z else utile.affichage.numero_atomique(self.valeur)
            ,
            utile.affichage.signe('+')
        )
