# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from __future__ import annotations

from typing import Union

from .. import couples, exception, objets
from . import utile
from .equation import Equation


class AcidoBasique:

    def __init__(
            self,
            reactif_1:Union[objets.Atome, objets.Ion, objets.Molecule],
            reactif_2:Union[objets.Atome, objets.Ion, objets.Molecule]
        ):

        reactif_1 = utile.convertie_notation(reactif_1.strip()) if isinstance(reactif_1, str) else reactif_1
        reactif_2 = utile.convertie_notation(reactif_2.strip()) if isinstance(reactif_2, str) else reactif_2

        produits_1 = couples.get_produit(reactif_1, 'acide/base')
        produits_2 = couples.get_produit(reactif_2, 'acide/base')

        # TODO: Dans le futur, essayer de deviner le couple, et donc le produit,
        #        avec des calculs si le couple n'est pas dans la liste.

        i1 = 0
        i2 = 0

        while (
            produits_1[i1][0] == produits_2[i2][0]
            and (i1 < len(produits_1) - 1 or i2 < len(produits_2) - 1)
        ):

            if i1 < len(produits_1) - 1:
                i1 += 1
            elif i2 < len(produits_2) - 1:
                i2 += 1

        # Si les deux réactifs jouent le même rôle
        #  (acide/acide ou base/base), aucune réaction acido-basique
        #  n'est possible.
        if produits_1[i1][0] == produits_2[i2][0]:
            raise exception.ValeurIncorrecte(
                "Les deux réactifs de la réaction acido-basique"
                + " jouent le même rôle, un acide et une base sont nécessaires."
            )

        produit_1 = produits_1[i1][1]
        produit_2 = produits_2[i2][1]


        ### Définition des demi-équations
        #

        demi_equation_1 = Equation(
            reactifs = [reactif_1],
            produits = [produit_1],
            demi_equation = 'acide/base'
        ).equilibrer()

        demi_equation_2 = Equation(
            reactifs = [reactif_2],
            produits = [produit_2],
            demi_equation = 'acide/base'
        ).equilibrer()

        if (
            len([e for e in reactif_1 if e.symbole == 'H'])
            <
            len([e for e in produit_1 if e.symbole == 'H'])
        ):
            demi_equation_gain = demi_equation_1
            demi_equation_don = demi_equation_2
        else:
            demi_equation_don = demi_equation_1
            demi_equation_gain = demi_equation_2


        ### Attributs
        #

        self.demi_equation_don = self.don = demi_equation_don
        self.demi_equation_gain = self.gain = demi_equation_gain
        self.equation = Equation(
            reactifs = (
                demi_equation_don.reactifs + demi_equation_gain.reactifs[:-1]
            ),
            produits = (
                demi_equation_don.produits[:-1] + demi_equation_gain.produits
            ),
            is_equilibre = True
        )

    def __str__(self):

        demi_equation_don = str(self.demi_equation_don)
        demi_equation_gain = str(self.demi_equation_gain)
        equation = str(self.equation)

        longueur = max(
            len(demi_equation_don),
            len(demi_equation_gain),
            len(equation)
        )

        return (
                     'Don : ' + str(self.demi_equation_don)
            + '\n' + 'Gain: ' + str(self.demi_equation_gain)
            + '\n      ' + '─' * longueur
            + '\n      ' + equation
        )
