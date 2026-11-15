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


class OxydoReduction:

    def __init__(
            self,
            reactif_1:Union[objets.Atome, objets.Ion, objets.Molecule],
            reactif_2:Union[objets.Atome, objets.Ion, objets.Molecule]
        ):

        reactif_1 = utile.convertie_notation(reactif_1.strip()) if isinstance(reactif_1, str) else reactif_1
        reactif_2 = utile.convertie_notation(reactif_2.strip()) if isinstance(reactif_2, str) else reactif_2

        produit_1 = couples.get_produit(reactif_1, 'oxydoreduction')[0][1]
        produit_2 = couples.get_produit(reactif_2, 'oxydoreduction')[0][1]


        ### Définition des demi-équations
        #

        demi_equation_1 = Equation(
            reactifs = [reactif_1],
            produits = [produit_1],
            demi_equation = 'oxydoreduction'
        ).equilibrer()

        demi_equation_2 = Equation(
            reactifs = [reactif_2],
            produits = [produit_2],
            demi_equation = 'oxydoreduction'
        ).equilibrer()

        if type(demi_equation_1.produits[-1]) == objets.Electron:

            if not (type(demi_equation_2.reactifs[-1]) == objets.Electron):
                raise exception.ValeurIncorrecte(
                    "Il n'y a pas de réaction d'oxydo-réduction possible"
                    + " entre ces deux réactifs."
                )

            demi_equation_1.produits.pop()
            demi_equation_2.reactifs.pop()

            demi_equation_don = demi_equation_1
            demi_equation_gain = demi_equation_2

        elif type(demi_equation_2.produits[-1]) == objets.Electron:

            if not (type(demi_equation_1.reactifs[-1]) == objets.Electron):
                raise exception.ValeurIncorrecte(
                    "Il n'y a pas de réaction d'oxydo-réduction possible"
                    + " entre ces deux réactifs."
                )

            demi_equation_1.reactifs.pop()
            demi_equation_2.produits.pop()

            demi_equation_don = demi_equation_2
            demi_equation_gain = demi_equation_1

        else:
            # Aucune demi-équation ne libère d'électron :
            #  les deux réactifs jouent le même rôle (oxydant/oxydant ou
            #  réducteur/réducteur), il n'y a donc pas de réaction possible.
            raise exception.ValeurIncorrecte(
                "Aucun couple oxydant/réducteur n'est formé par ces réactifs."
            )


        ### Equilibre coefficients
        #

        multiple_don = demi_equation_don.coefficients[1].pop()
        multiple_gain = demi_equation_gain.coefficients[0].pop()


        if multiple_don == multiple_gain:
            multiple_don = multiple_gain = 1

        elif multiple_don < multiple_gain:

            if multiple_gain % multiple_don == 0:
                multiple_gain = multiple_gain // multiple_don
                multiple_don = 1

        elif multiple_don > multiple_gain and multiple_don % multiple_gain == 0:
            multiple_don = multiple_don // multiple_gain
            multiple_gain = 1


        for coefficients in demi_equation_gain.coefficients:
            for i in range(len(coefficients)):
                coefficients[i] *= multiple_don

        for coefficients in demi_equation_don.coefficients:
            for i in range(len(coefficients)):
                coefficients[i] *= multiple_gain


        ### Attributs
        #

        self.demi_equation_don = self.don = demi_equation_don
        self.demi_equation_gain = self.gain = demi_equation_gain
        self.equation = Equation(
            reactifs = (
                demi_equation_don.reactifs + demi_equation_gain.reactifs
            ),
            produits = (
                demi_equation_don.produits + demi_equation_gain.produits
            ),
            coefficients = [
                demi_equation_don.coefficients[0]
                + demi_equation_gain.coefficients[0]
                ,
                demi_equation_don.coefficients[1]
                + demi_equation_gain.coefficients[1]
            ],
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
