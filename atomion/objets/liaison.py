# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from __future__ import annotations

from typing import List, Union

from .. import exception, objets, utile


class Liaison:

    __slots__ = (
        'atomes',
        'polarisee',
        'pole_moins', 'pole_plus'
    )

    def __init__(self,
            *valeurs:List[Union[str, objets.Atome, objets.Ion]]
        ) -> None:

        self.atomes = [
            utile.convertie_notation(element.strip()) if isinstance(element, str)
            else
                element
            for element in valeurs
        ]

        if len(self.atomes) != 2:
            raise exception.ValeurIncorrecte(
                "Une liaison doit être composée de deux atomes."
            )

        if (
            self.atomes[0].electronegativite is None
            or self.atomes[1].electronegativite is None
        ):
            raise exception.ValeurIncorrecte(
                "L'électronégativité est inconnue pour au moins un des atomes"
                + " (gaz noble ou élément non renseigné)."
            )

        self.polarisee = (
            abs(self.atomes[0].electronegativite - self.atomes[1].electronegativite) > 0.4
        )

        if self.atomes[0].electronegativite > self.atomes[1].electronegativite:
            self.pole_moins = self.atomes[0]
            self.pole_plus = self.atomes[1]
        else:
            self.pole_moins = self.atomes[1]
            self.pole_plus = self.atomes[0]

    def __iter__(self):

        for atome in self.atomes:
            yield atome

    def __str__(self):

        return (
            self.atomes[0].symbole + (
                '' if not self.polarisee else ('ᵟ' + (
                    '⁻' if self.atomes[0].electronegativite > self.atomes[1].electronegativite
                    else
                        '⁺'
                ))
            )
            + ' ── ' +
            self.atomes[1].symbole + (
                '' if not self.polarisee else ('ᵟ' + (
                    '⁻' if self.atomes[0].electronegativite < self.atomes[1].electronegativite
                    else
                        '⁺'
                ))
            )
        )
