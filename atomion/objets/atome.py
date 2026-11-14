# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Objet Atome : atome chimique avec ses particules subatomiques."""

from __future__ import annotations

from typing import Any, Optional, Union

from .. import exception, objets, utile


class Atome:
    """Un atome chimique avec ses protons, neutrons et électrons."""

    __slots__ = (
        'nom', 'symbole', 'categorie',
        'proton', 'neutron', 'nucleon', 'electron',
        'masse', 'masse_atomique_relative',
        'configuration', 'couches', 'noyau',
        'electronegativite',
    )

    def __init__(
        self,
        valeur: Union[int, str, objets.IonMonoAtomique],
        *args: Any,  # noqa: ANN401
        neutron: Optional[int] = None,
    ) -> None:
        """Initialise un atome à partir d'une valeur.

        Args:
            valeur: Numéro atomique, symbole ou IonMonoAtomique.
            *args: Arguments positionnels supplémentaires (ignorés).
            neutron: Nombre de neutrons (optionnel).
        """
        utile.get_info(self, valeur)

        self.neutron = (
            neutron if neutron is not None
            else
                round(self.masse_atomique_relative) - self.proton
        )
        self.electron = self.proton
        self.nucleon = self.proton + self.neutron
        self.masse = utile.get_masse(self)
        self.configuration = utile.configuration_electronique(self)
        self.noyau = objets.Noyau(
            objets.Proton(self.proton), objets.Neutron(self.neutron)
        )

    def __add__(
        self,
        obj: Union[objets.Proton, objets.Neutron, objets.Electron, Atome],
    ) -> Union[Atome, objets.Molecule, objets.IonMonoAtomique]:
        """Additionne un proton, neutron, électron ou atome."""
        if isinstance(obj, objets.Proton):
            return Atome(self.proton + obj.valeur)

        elif isinstance(obj, objets.Neutron):
            return Atome(self.proton, neutron=self.neutron + obj.valeur)

        elif isinstance(obj, objets.Electron):
            # Si on ajoute des électrons la charge est négative.
            return objets.IonMonoAtomique(self.proton, charge=-obj.valeur)

        elif isinstance(obj, Atome):
            return objets.Molecule([self, obj])

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(
        self,
        obj: Union[objets.Proton, objets.Neutron, objets.Electron, Atome],
    ) -> Union[Atome, objets.Molecule, objets.IonMonoAtomique]:
        """Addition sur place."""
        return self + obj

    def __sub__(
        self,
        obj: Union[objets.Proton, objets.Neutron, objets.Electron],
    ) -> Union[Atome, objets.IonMonoAtomique]:
        """Soustrait un proton, neutron ou électron."""
        if isinstance(obj, objets.Proton):
            return Atome(self.proton - obj.valeur)

        elif isinstance(obj, objets.Neutron):
            return Atome(self.proton, neutron=self.neutron - obj.valeur)

        elif isinstance(obj, objets.Electron):
            # Si on enlève des électrons la charge est positive.
            return objets.IonMonoAtomique(self.proton, charge=+obj.valeur)

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(
        self,
        obj: Union[objets.Proton, objets.Neutron, objets.Electron],
    ) -> Union[Atome, objets.IonMonoAtomique]:
        """Soustraction sur place."""
        return self - obj

    def __mul__(self, obj: int) -> objets.Molecule:
        """Multiplie l'atome par un entier (création d'une molécule)."""
        return objets.Molecule([self] * obj)

    def __rmul__(self, obj: int) -> objets.Molecule:
        """Multiplication à gauche par un entier."""
        return self * obj

    def __str__(self) -> str:
        """Représentation textuelle détaillée de l'atome."""
        str__ = (
            "Atome %s" % self.notation()
            + (
                "\n Elément: %s" % self.nom[utile.params.langue]
                if utile.params.nom else ''
            )
            + (
                "\n Catégorie: %s" % self.categorie[utile.params.langue]
                if utile.params.categorie else ''
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
                "\n Masse atomique relative: %s"
                % self.masse_atomique_relative
                if utile.params.masse_relative else ''
            )
            + (
                "\n Couche électronique: %s" % self.notation_couche()
                if utile.params.couches else ''
            )
            + (
                "\n Configuration électronique: %s"
                % self.notation_configuration()
                if utile.params.configuration else ''
            )
        )

        return utile.affichage.sans_accents(str__)

    def __repr__(self) -> str:
        """Représentation symbolique de l'atome."""
        return self.notation_symbole()

    def __hash__(self) -> int:
        """Hash basé sur la représentation symbolique."""
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:  # noqa: ANN401
        """Compare deux atomes par leur représentation symbolique."""
        return repr(self) == repr(obj)

    def notation(self) -> str:
        """Notation simplifiée (symbole Z= A=)."""
        return "%s Z=%s A=%s" % (
            self.symbole, self.proton, self.proton + self.neutron
        )

    def notation_symbole(
        self, *args: Any,  # noqa: ANN401
        A: bool = True, Z: bool = True
    ) -> str:
        """Notation du symbole avec nombre de masse et numéro atomique."""
        return "%s%s%s" % (
            '' if not A else utile.affichage.nombre_de_masse(self.proton + self.neutron)
            ,
            '' if not Z else utile.affichage.numero_atomique(self.proton)
            ,
            self.symbole
        )

    
    notation_couche = utile.notation_couche

    notation_configuration = utile.notation_configuration
