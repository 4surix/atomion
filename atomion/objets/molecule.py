# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional, List


###>>> CAPTURE FICHIER CALC

class Molecule:

    __slots__ = (
        'atomes', 
        'proton', 'neutron', 'electron', 'nucleon',
        'masse', 'masse_moleculaire_relative'
    )

    def __init__(self, 
            valeur:Union[str, IonPolyAtomique, List[Atome]],
            *args,
            verif_stable:bool = True
        ) -> None:

        self.atomes = (
            valeur if isinstance(valeur, list)
            else
                [
                    Atome(ion)
                    for ion in valeur.ions
                ]
                if isinstance(valeur, IonPolyAtomique)
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

        if verif_stable and utile.params.strict:
            if not utile.verif_espece_stable(self.atomes):
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

        str__ = (
            "Molécule %s" % self.notation_symbole()
            + (
                "\n Proton(s): %s" % self.proton
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): %s" % self.neutron
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): %s" % self.electron
                if utile.params.electron else ''
            )
            + (
                "\n Masse: %s" % self.masse
                if utile.params.masse else ''
            )
            + (
                "\n Masse moléculaire relative: %s"
                % (self.masse_moleculaire_relative)
                if utile.params.masse_relative else ''
            )
        )

        return (
            str__ if not utile.params.calculatrice
            else
                str__.replace('è', 'e').replace('é', 'e')
        )

    def __add__(self, 
            obj: Union[Molecule, Atome]
        ) -> Molecule:

        if isinstance(obj, Molecule):
            return Molecule(self.atomes + obj.atomes)

        elif isinstance(obj, Atome):
            return Molecule(self.atomes + [obj])

        elif isinstance(obj, IonMonoAtomique):
            return IonPolyAtomique(self.atomes + [obj])

        elif isinstance(obj, IonPolyAtomique):
            return IonPolyAtomique(self.atomes + obj.ions)

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, 
            obj: Union[Molecule, Atome]
        ) -> Molecule:
        return self + obj

    def __sub__(self, 
            obj: Union[Molecule, Atome]
        ) -> Union[None, Atome, Molecule]:

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

        elif isinstance(obj, Atome):

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
            obj: Union[Molecule, Atome]
        ) -> Union[None, Atome, Molecule]:
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
        for element in self.atomes:
            yield element

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        atomes = {}

        for atome in self.atomes:
            atome = atome.notation_symbole(A=False, Z=False)
            if atome not in atomes:
                atomes[atome] = 0
            atomes[atome] += 1

        return ''.join(
            '%s%s' % (
                atome,
                '' if nbr == 1
                else
                    nbr if utile.params.calculatrice
                    else
                        ''.join(
                            utile.sous_exposants[int(num)] 
                            for num in str(nbr)
                        )
            )
            for atome, nbr in atomes.items()
        )

objets.Molecule = Molecule


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

    def __init__(self, data:str):

        chemin = []

        data += '-'

        ramifications = {}

        indexs = []
        index_atome_carbone = 0

        nbr_carbone = nbr_hydrogene = 0

        value = ''

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
                        raise ValueError()

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
                        raise ValueError()

                    value = ''


        if famille == 'Alcool':
            nbr_hydrogene += ((nbr_carbone * 2) + 2) - len(ramifications) - 1

            partie = 'OH'

        if famille == 'Aldéhyde':
            nbr_carbone -= 1
            nbr_hydrogene += ((nbr_carbone * 2) + 1) - len(ramifications)

            partie = 'COH'

        if famille == 'Cétone':
            nbr_carbone -= 1
            nbr_hydrogene += ((nbr_carbone * 2) + 2) - len(ramifications)

            partie = 'CO'

        if famille == 'Acide carboxylique':
            nbr_carbone -= 1
            nbr_hydrogene += ((nbr_carbone * 2) + 1) - len(ramifications)

            partie = 'CO2H'


        for index, nbr_carbone_ram in ramifications.items():
            nbr_carbone += nbr_carbone_ram
            nbr_hydrogene += (nbr_carbone_ram * 2) + 1


        super().__init__(f'{partie}(C{nbr_carbone})(H{nbr_hydrogene})', verif_stable=False)

        self.famille = famille

    def __str__(self) -> str:

        str__ = (
            "Molécule Organique %s" % self.notation_symbole()
            + (
                "\n Famille: %s" % self.famille
            )
            + (
                "\n Proton(s): %s" % self.proton
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): %s" % self.neutron
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): %s" % self.electron
                if utile.params.electron else ''
            )
            + (
                "\n Masse: %s" % self.masse
                if utile.params.masse else ''
            )
            + (
                "\n Masse moléculaire relative: %s"
                % (self.masse_moleculaire_relative)
                if utile.params.masse_relative else ''
            )
        )

        return (
            str__ if not utile.params.calculatrice
            else
                str__.replace('è', 'e').replace('é', 'e')
        )

objets.MoleculeOrganique = MoleculeOrganique

###<<< CAPTURE FICHIER CALC


def MAJ_TYPE():
    variables = globals()
    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)