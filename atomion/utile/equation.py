# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from . import utile
from .utile import *
from .typing import *

from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import exception


###>>> CAPTURE FICHIER CALC


def analyse(
        partie:List[ Union[Molecule, Atome, Ion] ]
    ) -> List[ Dict[str, int] ]:
    # Retourne le nombre de chaque élément.

    info = []

    for element in partie:

        nombre_atomes = {}

        for espece in (
                element.atomes if isinstance(element, Molecule)
                else
                    element.ions if isinstance(element, IonPolyAtomique)
                    else
                        [element]
            ):

            symbole = espece.symbole

            if symbole not in nombre_atomes:
                nombre_atomes[symbole] = 1
            else:
                nombre_atomes[symbole] += 1

        info.append(nombre_atomes)

    return info


def analyse_charges(
        partie:List[ Union[Molecule, Atome, Ion] ]
    ) -> List[ Tuple[int, Ion, int] ]:
    # Retourne la charge de chaque espèce.
    # Si l'espèce n'est pas un ion il est ignoré
    #   vu que ça charge est égal à zéro.

    info = []

    for index, element in enumerate(partie):

        if isinstance(element, (IonPolyAtomique, IonMonoAtomique)):
            info.append(
                (
                    index, 
                    element, 
                    int('%s%s' % (element.charge, element.diff)) # charge
                )
            )

    return info


class Equation:

    __slots__ = (
        'is_equilibre', 
        'coefficients', 
        'spectatrices', 'reactifs', 'produits',
        'notation', 'demi_equation'
    )

    def __init__(
            self,
            notation:str = None,
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

        self.coefficients = [
            [1] * len(self.reactifs),
            [1] * len(self.produits)
        ] if not coefficients else coefficients

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
                '%s%s' % (
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
                '%s%s' % (
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

        List[Dict[str, int]];
        info_atomes_reactifs = analyse(self.reactifs)
        info_atomes_produits = analyse(self.produits)

        # Info charges.

        List[Tuple[int, Ion, int]];
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

                    Union[Atome, IonMonoAtomique]; 
                    element = utile.convertie_notation(symbole)

                    self.spectatrices.append(element)

                    symboles_reactifs.remove(symbole)

                    for element__ in self.reactifs:
                        if not (
                            (
                                isinstance(element__, (IonPolyAtomique, Molecule))
                                and element in element__
                            )
                            or
                            (
                                isinstance(element__, (IonMonoAtomique, Atome))
                                and element == element__
                            ) 
                        ):
                            self.reactifs.remove(element__)

        # Equilibrage.

        liste_symboles_atomes = symboles_reactifs

        configuration = self.coefficients

        nbr_symboles = len(liste_symboles_atomes)

        total_equilibre = False

        while not total_equilibre:

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

                    for index, element, charge in info_charges_reactifs:

                        value = configuration[0][index]

                        if value < min_value:
                            min_value = value
                            index__ = index

                    configuration[0][index__] += 1

                    total_equilibre = False


                elif charge_total_p2 < charge_total_p1:

                    min_value = 1000000000

                    for index, element, charge in info_charges_produits:

                        value = configuration[1][index]

                        if value < min_value:
                            min_value = value
                            index__ = index

                    configuration[1][index__] += 1

                    total_equilibre = False


        if self.demi_equation:

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
                self.reactifs.append(Molecule('H2O'))
                info_atomes_reactifs.append({'H': 2, 'O': 1})
                configuration[0].append(nombre_total_p2 - nombre_total_p1)

            elif nombre_total_p1 > nombre_total_p2:
                self.produits.append(Molecule('H2O'))
                info_atomes_produits.append({'H': 2, 'O': 1})
                configuration[1].append(nombre_total_p1 - nombre_total_p2)


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
                ion = Ion('H')
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

            elif nombre_total_p1 < nombre_total_p2:
                ion = Ion('H')
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
                electron = Electron()
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
                electron = Electron()
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
            quantites_reactifs:Dict[Union[Atome, Ion, Molecule], int] = None,
            *,
            quantites_produits:Dict[Union[Atome, Ion, Molecule], int] = None
        ):

        self.equation = equation.equilibrer()


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

    def initial(self) -> Dict[ Union[Atome, Ion, Molecule], int ]:
        return self.intermediaire(0)

    def intermediaire(self,
            nbr_transformation:Union[int, str] = 'x'
        ) -> Dict[ Union[Atome, Ion, Molecule], Union[int, str] ]:

        info = {}

        for coefficient, espece in zip(
                self.equation.coefficients[0], self.equation.reactifs
            ):
            if isinstance(nbr_transformation, str):
                info[espece] = '%s - %s * %s' % (
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
                info[espece] = '0 + %s * %s' % (
                    coefficient,
                    nbr_transformation
                )
            else:
                info[espece] = round(
                    coefficient * nbr_transformation,
                    3
                )

        return info

    def final(self) -> Dict[ Union[Atome, Ion, Molecule], int ]:

        reactif_limitant = None
        quantité_reactif_limitant = None

        for coefficient, espece in zip(
                self.equation.coefficients[0], self.equation.reactifs
            ):

            quantité = self.quantites_reactifs[espece] / coefficient

            if (
                quantité_reactif_limitant is None
                or quantité < quantité_reactif_limitant
            ):
                reactif_limitant = espece
                quantité_reactif_limitant = quantité

        return self.intermediaire(quantité_reactif_limitant)

    def reactifs_limitants(self) -> List[ Union[Atome, Ion, Molecule] ]:

        return [
            espece
            for espece, quantité in self.final().items()
            if not quantité
        ]

###<<< CAPTURE FICHIER CALC


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)