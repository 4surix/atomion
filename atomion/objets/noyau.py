# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objet Noyau : noyau atomique composé de protons et de neutrons."""

from __future__ import annotations

from typing import Any, List, Optional, Union

from .. import exception, objets, utile


class Noyau:
    """Un noyau atomique, composé de protons et de neutrons."""

    __slots__ = ('proton', 'neutron')

    def __init__(
        self, proton: objets.Proton, neutron: objets.Neutron
    ) -> None:
        """Initialise un noyau avec un proton et un neutron.

        Args:
            proton: Objet Proton.
            neutron: Objet Neutron.
        """
        self.proton = proton
        self.neutron = neutron

    def __repr__(self) -> str:
        """Représentation symbolique du noyau."""
        return self.notation_symbole()

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:  # noqa: ANN401
        """Compare deux noyaux par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def __add__(
        self,
        obj: Union[objets.Electron, objets.Proton, objets.Neutron],
    ) -> Union[objets.Atome, objets.IonMonoAtomique, Noyau]:
        """Additionne un électron, proton ou neutron au noyau."""
        if isinstance(obj, objets.Electron):

            if obj.valeur != self.proton.valeur:
                return objets.IonMonoAtomique(
                    self.proton.valeur,
                    neutron=self.neutron.valeur,
                    charge=self.proton.valeur - obj.valeur,
                )

            else:
                return objets.Atome(
                    self.proton.valeur,
                    neutron=self.neutron.valeur,
                )

        elif isinstance(obj, objets.Proton):
            self.proton.valeur += obj.valeur
            return self

        elif isinstance(obj, objets.Neutron):
            self.neutron.valeur += obj.valeur
            return self

        else:
            raise exception.Incompatible(self, obj)

    def __lshift__(
        self, obj: Noyau
    ) -> List[Union[Noyau, objets.Neutron]]:
        """Fusion nucléaire (opérateur <<)."""
        if isinstance(obj, Noyau):

            protons = self.proton.valeur + obj.proton.valeur
            neutrons = self.neutron.valeur + obj.neutron.valeur

            nouvelles_especes: List[Union[Noyau, objets.Neutron]] = []

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

    def __rshift__(self, obj: Any) -> Optional[Any]:  # noqa: ANN401
        """Fission nucléaire (opérateur >>, non implémenté)."""
        # Fission
        return NotImplemented

    def notation_symbole(
        self, *args: Any,  # noqa: ANN401
        A: bool = True, Z: bool = True
    ) -> str:
        """Notation symbolique du noyau (ex: '⁴₂X')."""
        return "%s%sX" % (
            '' if not A
            else
                utile.affichage.nombre_de_masse(
                    self.neutron.valeur + self.proton.valeur
                )
            ,
            '' if not Z else utile.affichage.numero_atomique(self.proton.valeur),
        )
