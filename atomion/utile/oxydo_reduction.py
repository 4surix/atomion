# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from .typing import *
from .utile import *
from .equation import *

from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import exception
from .. import couples


###>>> CAPTURE FICHIER CALC


class OxydoReduction:

    def __init__(
            self,
            reactif_1:Union[Atome, Ion, Molecule],
            reactif_2:Union[Atome, Ion, Molecule]
        ):

        produit_1 = couples.get_produit(reactif_1)
        produit_2 = couples.get_produit(reactif_2)

        if not produit_1 or not produit_2:
            return NotImplemented


        ### Définition des demi-équations
        #

        demi_equation_1 = Equation(
            reactifs = [reactif_1],
            produits = [produit_1],
            demi_equation = True
        ).equilibrer()

        demi_equation_2 = Equation(
            reactifs = [reactif_2],
            produits = [produit_2],
            demi_equation = True
        ).equilibrer()

        if type(demi_equation_1.produits[-1]) == Electron:

            if not (type(demi_equation_2.reactifs[-1]) == Electron):
                raise

            demi_equation_1.produits.pop()
            demi_equation_2.reactifs.pop()

            demi_equation_don = demi_equation_1
            demi_equation_gain = demi_equation_2

        elif type(demi_equation_2.produits[-1]) == Electron:

            if not (type(demi_equation_1.reactifs[-1]) == Electron):
                raise

            demi_equation_1.reactifs.pop()
            demi_equation_2.produits.pop()

            demi_equation_don = demi_equation_2
            demi_equation_gain = demi_equation_1


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

        elif multiple_don > multiple_gain:

            if multiple_don % multiple_gain == 0:
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


###<<< CAPTURE FICHIER CALC


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)