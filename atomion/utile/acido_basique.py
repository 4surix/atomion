# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from . import utile
from .typing import List, Tuple, Union
from .equation import Equation

from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique
)
from .. import exception
from .. import couples


###>>> CAPTURE FICHIER CALC


class AcidoBasique:

    def __init__(
            self,
            reactif_1:Union[Atome, Ion, Molecule],
            reactif_2:Union[Atome, Ion, Molecule]
        ):

        reactif_1 = utile.convertie_notation(reactif_1.strip()) if isinstance(reactif_1, str) else reactif_1
        reactif_2 = utile.convertie_notation(reactif_2.strip()) if isinstance(reactif_2, str) else reactif_2

        List[Tuple[str, Union[Atome, Ion]]];
        produits_1 = couples.get_produit(reactif_1, 'acide/base')
        produits_2 = couples.get_produit(reactif_2, 'acide/base')

        # TODO: Dans le futur, essayer de deviner le couple, et donc le produit,
        #        avec des calculs si le couple n'est pas dans la liste.
        if not produits_1 or not produits_2:
            return NotImplemented

        i1 = 0
        i2 = 0

        while produits_1[i1][0] == produits_2[i2][0]:

            if i1 < len(produits_1) - 1:
                i1 += 1
            elif i2 < len(produits_2) - 1:
                i2 += 1

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

        H = Atome('H')

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


###<<< CAPTURE FICHIER CALC


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)