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
    """
    ### &doc_id molecule:class
    """

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
        """
        ### &doc_id molecule:init
        """

        self.atomes = (
            valeur if isinstance(valeur, list)
            else
                [
                    Atome(ion)
                    for ion in valeur.ions
                ] if isinstance(valeur, IonPolyAtomique)
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

        if verif_stable:
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
        """
        ### &doc_id molecule:notation_symbole
        """

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

###<<< CAPTURE FICHIER CALC

objets.Molecule = Molecule


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)