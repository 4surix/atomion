# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objet Molecule : molécule chimique composée de plusieurs atomes."""

from __future__ import annotations

from typing import Any, List, Union

from .. import exception, objets, utile


class Molecule:
    """Une molécule chimique composée de plusieurs atomes."""

    __slots__ = (
        'atomes',
        'electron',
        'masse',
        'masse_moleculaire_relative',
        'neutron',
        'nucleon',
        'proton'
    )

    def __init__(
        self,
        valeur: Union[str, objets.IonPolyAtomique, List[objets.Atome]],
        *args: Any,
        verif_stable: bool = True,
    ) -> None:
        """Initialise une molécule.

        Args:
            valeur: Symbole, IonPolyAtomique ou liste d'atomes.
            *args: Arguments supplémentaires (ignorés).
            verif_stable: Vérifier la stabilité de la molécule.
        """

        self.atomes = (
            valeur if isinstance(valeur, list)
            else
                [
                    objets.Atome(ion)
                    for ion in valeur.ions
                ]
                if isinstance(valeur, objets.IonPolyAtomique)
                else
                    utile.convertie_notation_vers('atomes', valeur)
        )

        if len(self.atomes) < 2:
            raise exception.ValeurIncorrecte(
                "Une molécule doit être composée de plusieurs atomes."
            )

        for atome in self.atomes:
            if atome.symbole in (
                'He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn'
            ):
                raise exception.ValeurIncorrecte(
                    "Une molécule ne peut pas avoir de gaz noble."
                )

        if verif_stable and utile.params.strict and not utile.verif_espece_stable(self.atomes):
            raise exception.Instable(self)

        self.proton = sum(atome.proton for atome in self.atomes)
        self.neutron = sum(atome.neutron for atome in self.atomes)
        self.nucleon = self.proton + self.neutron
        self.electron = sum(atome.electron for atome in self.atomes)

        self.masse = sum(atome.masse for atome in self.atomes)
        self.masse_moleculaire_relative = sum(
            atome.masse_atomique_relative
            for atome in self.atomes
        )

    def __str__(self) -> str:
        """Représentation textuelle de la molécule."""
        str__ = (
            "Molécule {}".format(self.notation_symbole())
            + (
                "\n Proton(s): {}".format(self.proton)
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): {}".format(self.neutron)
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): {}".format(self.electron)
                if utile.params.electron else ''
            )
            + (
                "\n Masse: {}".format(self.masse)
                if utile.params.masse else ''
            )
            + (
                "\n Masse moléculaire relative: {}".format(self.masse_moleculaire_relative)
                if utile.params.masse_relative else ''
            )
        )

        return utile.affichage.sans_accents(str__)

    def __add__(
        self, obj: Union[Molecule, objets.Atome]
    ) -> Molecule:
        """Additionne deux molécules ou ajoute un atome.

        Args:
            obj: Molécule ou atome à additionner.

        Returns:
            Nouvelle molécule résultante.
        """
        if isinstance(obj, Molecule):
            return Molecule(self.atomes + obj.atomes)

        elif isinstance(obj, objets.Atome):
            return Molecule(self.atomes + [obj])

        elif isinstance(obj, objets.IonMonoAtomique):
            return objets.IonPolyAtomique(self.atomes + [obj])

        elif isinstance(obj, objets.IonPolyAtomique):
            return objets.IonPolyAtomique(self.atomes + obj.ions)

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self,
            obj: Union[Molecule, objets.Atome]
        ) -> Molecule:
        return self + obj

    def __sub__(self,
            obj: Union[Molecule, objets.Atome]
        ) -> Union[objets.Atome, Molecule, None]:

        if isinstance(obj, Molecule):

            atomes = self.atomes[:]
            for atome in obj.atomes:
                atomes.remove(atome)

            return (
                None if not atomes
                else
                    atomes[0] if len(atomes) == 1
                    else
                        Molecule(atomes)
            )

        elif isinstance(obj, objets.Atome):

            atomes = self.atomes[:]
            atomes.remove(obj)

            return (
                None if not atomes
                else
                    atomes[0] if len(atomes) == 1
                    else
                        Molecule(atomes)
            )

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self,
            obj: Union[Molecule, objets.Atome]
        ) -> Union[objets.Atome, Molecule, None]:
        return self - obj

    def __mul__(self, obj: int) -> Molecule:
        return Molecule(self.atomes * obj)

    def __rmul__(self, obj: int) -> Molecule:
        return self * obj

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def __iter__(self):
        yield from self.atomes

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        ordre = []
        atomes = {}

        for atome in self.atomes:
            atome = atome.notation_symbole(A=False, Z=False)
            if atome not in atomes:
                # L'ordre d'affichage ne doit pas dependre de l'ordre
                #  d'iteration du dictionnaire (different sur MicroPython).
                ordre.append(atome)
                atomes[atome] = 0
            atomes[atome] += 1

        return ''.join(
            '{}{}'.format(atome, utile.affichage.nombre_indice(atomes[atome]))
            for atome in ordre
        )



PREFIXS = [
    'bi',
    'tri',
    'qua',
]

THERMES = [
    'méth',
    'éth',
    'prop',
    'but',
    'pent',
    'hex',
    'hept',
    'oct',
    'non',
    'déc'
]

CHIFFRES = tuple('0123456789')


class MoleculeOrganique(Molecule):

    """Molécule organique construite à partir de sa nomenclature.

    Familles actuellement gérées :

    - alcool             : suffixe `-ol`       (ex. `butan-1-ol`) ;
    - aldéhyde           : suffixe `-anal`     (ex. `butanal`) ;
    - cétone             : suffixe `-one`      (ex. `butan-2-one`) ;
    - acide carboxylique : `acide … -anoïque`  (ex. `acide éthanoïque`).

    Limites connues :

    - les alcanes (`pentane`), alcènes, alcynes, etc. ne sont pas gérés ;
    - seuls les préfixes `bi`, `tri`, `qua` sont reconnus.

    Une nomenclature non reconnue lève `ValeurIncorrecte`.
    """

    def __init__(self, data:str):

        chemin = []

        data += '-'

        ramifications = {}

        indexs = []
        index_atome_carbone = 0

        nbr_carbone = nbr_hydrogene = 0

        value = ''

        cat = ''
        famille = None

        for carac in data:

            if carac in CHIFFRES:
                cat = 'INT'
                value += carac

            elif carac == ',':
                indexs.append(int(value))
                cat = ''
                value = ''

            elif carac == '-':

                if cat == 'INT':

                    if famille == 'AN-':
                        index_atome_carbone = int(value) - 1
                    else:
                        indexs.append(int(value))

                    cat = ''
                    value = ''

                if value == 'an':
                    value = ''

            else:
                value += carac

                if value in PREFIXS:

                    if PREFIXS.index(value) + 2 != len(indexs):
                        raise exception.ValeurIncorrecte(
                            "Nomenclature de molécule organique invalide :"
                            + " préfixe incohérent avec les indices."
                        )

                    value = ''

                elif value in THERMES:
                    nbr_carbone = THERMES.index(value) + 1
                    value = ''

                elif value == 'yl':
                    for index in indexs:
                        ramifications[index] = nbr_carbone
                    value = ''
                    indexs = []

                elif value == 'anal':
                    famille = 'Aldéhyde'
                    value = ''

                elif value == 'ol':
                    famille = 'Alcool'
                    value = ''

                elif value == 'one':
                    famille = 'Cétone'
                    value = ''

                elif value == 'acide ':
                    famille = 'Acide carboxylique'
                    value = ''

                elif value == 'anoïque':

                    if famille != 'Acide carboxylique':
                        raise exception.ValeurIncorrecte(
                            "Nomenclature de molécule organique invalide :"
                            + " 'anoïque' requiert la famille 'Acide carboxylique'."
                        )

                    value = ''


        if famille == 'Alcool':
            nbr_hydrogene += ((nbr_carbone * 2) + 2) - len(ramifications) - 1

            partie = 'OH'

        elif famille == 'Aldéhyde':
            nbr_carbone -= 1
            nbr_hydrogene += ((nbr_carbone * 2) + 1) - len(ramifications)

            partie = 'COH'

        elif famille == 'Cétone':
            nbr_carbone -= 1
            nbr_hydrogene += ((nbr_carbone * 2) + 2) - len(ramifications)

            partie = 'CO'

        elif famille == 'Acide carboxylique':
            nbr_carbone -= 1
            nbr_hydrogene += ((nbr_carbone * 2) + 1) - len(ramifications)

            partie = 'CO2H'

        else:
            raise exception.ValeurIncorrecte(
                "Nomenclature de molécule organique non reconnue."
                + " Familles gérées : alcool (-ol), aldéhyde (-anal),"
                + " cétone (-one), acide carboxylique (acide … -anoïque)."
            )


        for _index, nbr_carbone_ram in ramifications.items():
            nbr_carbone += nbr_carbone_ram
            nbr_hydrogene += (nbr_carbone_ram * 2) + 1


        super().__init__(
            '{}(C{})(H{})'.format(partie, nbr_carbone, nbr_hydrogene),
            verif_stable=False
        )

        self.famille = famille

    def __str__(self) -> str:

        str__ = (
            "Molécule Organique {}".format(self.notation_symbole())
            + (
                "\n Famille: {}".format(self.famille)
            )
            + (
                "\n Proton(s): {}".format(self.proton)
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): {}".format(self.neutron)
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): {}".format(self.electron)
                if utile.params.electron else ''
            )
            + (
                "\n Masse: {}".format(self.masse)
                if utile.params.masse else ''
            )
            + (
                "\n Masse moléculaire relative: {}".format(self.masse_moleculaire_relative)
                if utile.params.masse_relative else ''
            )
        )

        return utile.affichage.sans_accents(str__)
