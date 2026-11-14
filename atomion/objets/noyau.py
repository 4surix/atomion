# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from __future__ import annotations

from typing import Any, List, Union

from .. import exception, objets, utile


class Noyau:

    __slots__ = ('proton', 'neutron')

    def __init__(self, proton, neutron):

        self.proton = proton
        self.neutron = neutron

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __add__(self,
            obj:Union[objets.Electron, objets.Proton, objets.Neutron]
        ) -> Union[objets.Atome, objets.IonMonoAtomique, Noyau]:

        if isinstance(obj, objets.Electron):

            if obj.valeur != self.proton.valeur:
                return objets.IonMonoAtomique(
                    self.proton.valeur,
                    neutron = self.neutron.valeur,
                    charge = self.proton.valeur - obj.valeur
                )

            else:
                return objets.Atome(
                    self.proton.valeur,
                    neutron = self.neutron.valeur
                )

        elif isinstance(obj, objets.Proton):
            self.proton.valeur += obj.valeur
            return self

        elif isinstance(obj, objets.Neutron):
            self.neutron.valeur += obj.valeur
            return self

        else:
            raise exception.Incompatible(self, obj)

    def __lshift__(self, obj:Noyau) -> List[ Union[Noyau, objets.Neutron] ]:
        # Fusion

        if isinstance(obj, Noyau):

            protons = self.proton.valeur + obj.proton.valeur
            neutrons = self.neutron.valeur + obj.neutron.valeur

            nouvelles_especes = []

            atome = objets.Atome(protons)
            neutrons -= atome.neutron

            nouvelles_especes.append(atome.noyau)

            if neutrons < 0:
                # On retire les neutrons en trop.
                # Noyau(2, 1) << Noyau(2, 2) == Noyau(4, 3)
                atome.noyau.neutron.valeur += neutrons

            elif neutrons > 0:
                # On rajoute les neutrons qui ne sont pas
                #  dans le nouveau noyau mais qui étaient là de base.
                # Noyau(2, 3) << Noyau(2, 2) == [Neutron(), Noyau(4, 4)]
                nouvelles_especes.append(objets.Neutron(neutrons))

            return nouvelles_especes

        else:
            raise exception.Incompatible(self, obj)

    def __rshift__(self, obj):
        # Fission
        return NotImplemented

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%s%sX" % (
            '' if not A
            else
                utile.affichage.nombre_de_masse(
                    self.neutron.valeur + self.proton.valeur
                )
            ,
            '' if not Z else utile.affichage.numero_atomique(self.proton.valeur)
        )
