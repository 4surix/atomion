# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Gestion des équations et réactions chimiques."""

from __future__ import annotations

from typing import Dict, List, Tuple, Union, Optional

from .. import couples, exception, objets
from . import utile
from .utile import *


def analyse(
        partie:List[ Union[objets.Molecule, objets.Atome, objets.Ion] ]
    ) -> List[Dict[str, int]]:
    """Retourne le nombre de chaque élément dans une liste d'espèces.

    Args:
        partie: Liste d'espèces chimiques (Molecule, Atome ou Ion).

    Returns:
        Liste de dictionnaires {symbole: nombre} pour chaque espèce.
    """
    # Retourne le nombre de chaque élément.

    info = []

    for element in partie:

        nombre_atomes = {}

        for espece in (
                element.atomes if isinstance(element, objets.Molecule)
                else
                    element.ions if isinstance(element, objets.IonPolyAtomique)
                    else
                        [element]
            ):

            # Les électrons n'ont pas de symbole atomique
            #  et n'entrent pas dans le décompte des atomes.
            if isinstance(espece, objets.Electron):
                continue

            symbole = espece.symbole

            if symbole not in nombre_atomes:
                nombre_atomes[symbole] = 1
            else:
                nombre_atomes[symbole] += 1

        info.append(nombre_atomes)

    return info


def analyse_charges(
        partie:List[ Union[objets.Molecule, objets.Atome, objets.Ion] ]
    ) -> List[ Tuple[int, objets.Ion, int] ]:
    # Retourne la charge de chaque espèce.
    # Si l'espèce n'est pas un ion il est ignoré
    #   vu que ça charge est égal à zéro.

    info = []

    for index, element in enumerate(partie):

        if isinstance(element, (objets.IonPolyAtomique, objets.IonMonoAtomique)):

            if element.charge == '+':
                charge = element.diff
            elif element.charge == '-':
                charge = - element.diff
            else:
                # Charge nulle (notée '?').
                charge = 0

            info.append((index, element, charge))

    return info


def DemiEquation(
        reactif:Union[str, objets.Atome, objets.Molecule, objets.Ion],
        produit:Union[str, objets.Atome, objets.Molecule, objets.Ion] = None
    ):

    if isinstance(reactif, str):
        reactif = utile.convertie_notation(reactif)

    if isinstance(produit, str):
        produit = utile.convertie_notation(produit)

    if produit is None:
        produit = couples.get_produit(reactif, 'oxydoreduction')[0][1]

    return Equation(
        reactifs = [reactif],
        produits = [produit],
        demi_equation = 'oxydoreduction'
    )


class Equation:
    """Représentation d'une équation chimique."""

    __slots__ = (
        'coefficients',
        'demi_equation',
        'is_equilibre',
        'notation',
        'produits',
        'reactifs',
        'spectatrices'
    )

    def __init__(
            self,
            notation:Optional[str] = None,
            *,
            demi_equation:bool = False,

            reactifs = None,
            produits = None,
            coefficients = None,
            is_equilibre = False
        ):

        self.demi_equation = demi_equation

        if notation:
            reactifs, produits = notation.split(' -> ')

        self.reactifs = [
            utile.convertie_notation(notation.strip())
            for notation in reactifs.split(' + ')
        ] if type(reactifs) == str else reactifs

        self.produits = [
            utile.convertie_notation(notation.strip())
            for notation in produits.split(' + ')
        ] if type(produits) == str else produits

        self.spectatrices = []

        self.coefficients = coefficients if coefficients else [[1] * len(self.reactifs), [1] * len(self.produits)]

        self.maj_notation()

        self.is_equilibre = is_equilibre

    def __str__(self):
        return self.notation

    def __repr__(self):
        return self.notation

    def __eq__(self, obj):
        return self.notation == obj

    def maj_notation(self):

        # X + X -> X
        self.notation = (
            ' + '.join(
                '{}{}'.format(
                    '' if nbr == 1
                    else
                        str(nbr) + ' '
                    ,
                    element.notation_symbole(A=False, Z=False)
                )
                for nbr, element in zip(self.coefficients[0], self.reactifs)
            )
            + ' -> '
            + ' + '.join(
                '{}{}'.format(
                    '' if nbr == 1
                    else
                        str(nbr) + ' '
                    ,
                    element.notation_symbole(A=False, Z=False)
                )
                for nbr, element in zip(self.coefficients[1], self.produits)
            )
        )

    def equilibrer(self):

        if self.is_equilibre:
            return self

        # Info atomes.

        info_atomes_reactifs = analyse(self.reactifs)
        info_atomes_produits = analyse(self.produits)

        # Info charges.

        info_charges_reactifs = analyse_charges(self.reactifs)
        info_charges_produits = analyse_charges(self.produits)

        # Collecte des symboles en retirant les doublons

        symboles_reactifs = []

        for info in info_atomes_reactifs:
            for symbole in info:
                if symbole not in symboles_reactifs:
                    symboles_reactifs.append(symbole)

        symboles_produits = []

        for info in info_atomes_produits:
            for symbole in info:
                if symbole not in symboles_produits:
                    symboles_produits.append(symbole)


        ### Collecte des possibles élements spectateurs.
        #

        if not self.demi_equation:
            # Dans le cas d'une demi-équation, exemple : {Cr2O7 2-} -> {Cr 3+},
            #  certain réactif ne sont pas dans les produits, et vise-versa,
            #  donc le code ci-dessous va les enlever.

            for symbole in symboles_reactifs:

                if symbole not in symboles_produits:

                    element = utile.convertie_notation(symbole)

                    self.spectatrices.append(element)

                    symboles_reactifs.remove(symbole)

                    for element__ in self.reactifs:
                        if not (
                            (
                                isinstance(element__, (objets.IonPolyAtomique, objets.Molecule))
                                and element in element__
                            )
                            or
                            (
                                isinstance(element__, (objets.IonMonoAtomique, objets.Atome))
                                and element == element__
                            )
                        ):
                            self.reactifs.remove(element__)


        ### Equilibrage.
        #

        liste_symboles_atomes = symboles_reactifs

        configuration = self.coefficients

        nbr_symboles = len(liste_symboles_atomes)

        total_equilibre = False

        while (
            not total_equilibre
            # Une demi-équation d'acide base est forcément déséquilibrée
            #  au niveau de ses nombres d'atomes, et pas besoin d'équilibrer
            #  les charges.
            and self.demi_equation != 'acide/base'
        ):

            total_equilibre = True

            nbr_symboles_equilibres = 0

            ### Equilibrage nombre atomes.
            #

            while nbr_symboles_equilibres != nbr_symboles:

                for symbole in liste_symboles_atomes:

                    if (
                        # Dans le cas d'une demi-équation,
                        #  on ne fait pas attention en premier
                        #  à l'hydrogéne et l'oxygéne.
                        self.demi_equation
                        and symbole in ['H', 'O']
                    ):
                        nbr_symboles_equilibres += 1
                        continue

                    nombre_total_p1 = sum(
                        element.get(symbole, 0) * configuration[0][i]
                        for i, element in enumerate(info_atomes_reactifs)
                    )

                    nombre_total_p2 = sum(
                        element.get(symbole, 0) * configuration[1][i]
                        for i, element in enumerate(info_atomes_produits)
                    )

                    if nombre_total_p1 < nombre_total_p2:

                        index = None
                        min_value = 1000000000

                        for i, info in enumerate(info_atomes_reactifs):

                            value = info.get(symbole, 0) * configuration[0][i]

                            if value and value < min_value:
                                index = i
                                min_value = value

                        configuration[0][index] += 1

                        nbr_symboles_equilibres = 0
                        total_equilibre = False
                        break

                    elif nombre_total_p2 < nombre_total_p1:

                        index = None
                        min_value = 1000000000

                        for i, info in enumerate(info_atomes_produits):

                            value = info.get(symbole, 0) * configuration[1][i]

                            if value and value < min_value:
                                index = i
                                min_value = value

                        configuration[1][index] += 1

                        nbr_symboles_equilibres = 0
                        total_equilibre = False
                        break

                    else:
                        nbr_symboles_equilibres += 1

            ### Equilibrage nombre charges.
            #

            while True:

                charge_total_p1 = sum(
                    charge * configuration[0][index]
                    for index, element, charge in info_charges_reactifs
                )

                charge_total_p2 = sum(
                    charge * configuration[1][index]
                    for index, element, charge in info_charges_produits
                )

                if (
                    not (
                        # Si les charges des 2 côtés sont toutes les 2
                        #  soit positif soit négatif, impossible de les équilibrer
                        #  en changeant leur coefficients.
                        (charge_total_p1 < 0 and charge_total_p2 < 0)
                        or (charge_total_p1 > 0 and charge_total_p2 > 0)
                    )
                    or charge_total_p1 == charge_total_p2
                ):
                    break

                elif charge_total_p1 < charge_total_p2:

                    min_value = 1000000000

                    for index, _element, _charge in info_charges_reactifs:

                        value = configuration[0][index]

                        if value < min_value:
                            min_value = value
                            index__ = index

                    configuration[0][index__] += 1

                    total_equilibre = False


                elif charge_total_p2 < charge_total_p1:

                    min_value = 1000000000

                    for index, _element, _charge in info_charges_produits:

                        value = configuration[1][index]

                        if value < min_value:
                            min_value = value
                            index__ = index

                    configuration[1][index__] += 1

                    total_equilibre = False


        if self.demi_equation == 'oxydoreduction':

            ### Equilibre de l'oxygéne en rajoutant de l'H2O
            #

            nombre_total_p1 = sum(
                element.get('O', 0) * configuration[0][i]
                for i, element in enumerate(info_atomes_reactifs)
            )

            nombre_total_p2 = sum(
                element.get('O', 0) * configuration[1][i]
                for i, element in enumerate(info_atomes_produits)
            )

            if nombre_total_p1 == nombre_total_p2:
                pass

            elif nombre_total_p1 < nombre_total_p2:
                self.reactifs.append(objets.Molecule('H2O'))
                info_atomes_reactifs.append({'H': 2, 'O': 1})
                configuration[0].append(nombre_total_p2 - nombre_total_p1)

            elif nombre_total_p1 > nombre_total_p2:
                self.produits.append(objets.Molecule('H2O'))
                info_atomes_produits.append({'H': 2, 'O': 1})
                configuration[1].append(nombre_total_p1 - nombre_total_p2)


        if self.demi_equation in ('oxydoreduction', 'acide/base'):

            ### Equilibre de l'hydrogéne en rajoutant des ions H+
            #

            nombre_total_p1 = sum(
                element.get('H', 0) * configuration[0][i]
                for i, element in enumerate(info_atomes_reactifs)
            )

            nombre_total_p2 = sum(
                element.get('H', 0) * configuration[1][i]
                for i, element in enumerate(info_atomes_produits)
            )

            if nombre_total_p1 == nombre_total_p2:
                pass

            elif nombre_total_p1 < nombre_total_p2:
                ion = objets.Ion('H')
                self.reactifs.append(ion)
                info_atomes_reactifs.append({'H': 1})
                info_charges_reactifs.append(
                    (
                        len(configuration[0]),
                        ion,
                        1
                    )
                )
                configuration[0].append(nombre_total_p2 - nombre_total_p1)

            elif nombre_total_p1 > nombre_total_p2:
                ion = objets.Ion('H')
                self.produits.append(ion)
                info_atomes_produits.append({'H': 1})
                info_charges_produits.append(
                    (
                        len(configuration[1]),
                        ion,
                        1
                    )
                )
                configuration[1].append(nombre_total_p1 - nombre_total_p2)


            ### Equilibre des charges
            #

            charge_total_p1 = sum(
                charge * configuration[0][index]
                for index, element, charge in info_charges_reactifs
            )

            charge_total_p2 = sum(
                charge * configuration[1][index]
                for index, element, charge in info_charges_produits
            )

            if charge_total_p1 == charge_total_p2:
                pass

            elif charge_total_p1 > charge_total_p2:
                electron = objets.Electron()
                self.reactifs.append(electron)
                info_charges_reactifs.append(
                    (
                        len(configuration[0]),
                        electron,
                        -1
                    )
                )
                configuration[0].append(charge_total_p1 - charge_total_p2)

            elif charge_total_p1 < charge_total_p2:
                electron = objets.Electron()
                self.produits.append(electron)
                info_charges_produits.append(
                    (
                        len(configuration[1]),
                        electron,
                        -1
                    )
                )
                configuration[1].append(charge_total_p2 - charge_total_p1)


        self.is_equilibre = True
        self.maj_notation()

        return self


class Reaction:

    __slots__ = (
        'equation', 'quantites_reactifs'
    )

    def __init__(self,
            equation:Equation,
            quantites_reactifs:Optional[Dict[Union[objets.Atome, objets.Ion, objets.Molecule], int]] = None,
            *,
            quantites_produits:Optional[Dict[Union[objets.Atome, objets.Ion, objets.Molecule], int]] = None
        ):

        if isinstance(equation, str):
            equation = Equation(equation)

        if isinstance(equation, Equation):
            self.equation = equation.equilibrer()

        else:
            raise exception.ValeurIncorrecte(
                "L'équation doit être un objet de type 'Equation' ou du texte."
            )

        if quantites_produits:

            quantites_reactifs = {}

            coefficient = self.equation.coefficients[1][0]
            espece = self.equation.produits[0]

            xf = quantites_produits[espece] / coefficient

            for coefficient, espece in zip(
                    self.equation.coefficients[0], self.equation.reactifs
                ):
                quantites_reactifs[espece] = round(coefficient * xf, 3)

        if not quantites_reactifs:
            raise exception.ValeurIncorrecte(
                "Merci d'indiquer la quantité de réactif ou de produit."
            )

        self.quantites_reactifs = quantites_reactifs

    def initial(self) -> Dict[ Union[objets.Atome, objets.Ion, objets.Molecule], int ]:
        return self.intermediaire(0)

    def intermediaire(self,
            nbr_transformation:Union[int, str] = 'x'
        ) -> Dict[ Union[objets.Atome, objets.Ion, objets.Molecule], Union[int, str] ]:

        info = {}

        for coefficient, espece in zip(
                self.equation.coefficients[0], self.equation.reactifs
            ):
            if isinstance(nbr_transformation, str):
                info[espece] = '{} - {} * {}'.format(
                    self.quantites_reactifs[espece],
                    coefficient,
                    nbr_transformation
                )
            else:
                info[espece] = round(
                    (
                        self.quantites_reactifs[espece]
                        - coefficient * nbr_transformation
                    ),
                    3
                )

        for coefficient, espece in zip(
                self.equation.coefficients[1], self.equation.produits
            ):
            if isinstance(nbr_transformation, str):
                info[espece] = '0 + {} * {}'.format(
                    coefficient,
                    nbr_transformation
                )
            else:
                info[espece] = round(
                    coefficient * nbr_transformation,
                    3
                )

        return info

    def final(self) -> Dict[ Union[objets.Atome, objets.Ion, objets.Molecule], int ]:

        quantité_reactif_limitant = None

        for coefficient, espece in zip(
                self.equation.coefficients[0], self.equation.reactifs
            ):

            quantité = self.quantites_reactifs[espece] / coefficient

            if (
                quantité_reactif_limitant is None
                or quantité < quantité_reactif_limitant
            ):
                quantité_reactif_limitant = quantité

        return self.intermediaire(quantité_reactif_limitant)

    def reactifs_limitants(self) -> List[ Union[objets.Atome, objets.Ion, objets.Molecule] ]:

        return [
            espece
            for espece, quantité in self.final().items()
            if not quantité
        ]
