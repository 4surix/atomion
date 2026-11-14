# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Dictionnaire des couples acide/base et oxydo-reduction."""

from __future__ import annotations

from typing import Any

from . import utile
from . import exception


couples: dict[str, list[tuple[Any, Any]]] = {}

def __maj() -> None:
    """Initialise le dictionnaire des couples acide/base et oxydo-reduction."""

    global couples

    couples = {
        'oxydoreduction': [
            (
                utile.convertie_notation(e1),
                utile.convertie_notation(e2)
            )
            for e1, e2 in [
                # Source listant les couples :
                #  https://guy-chaumeton.pagesperso-orange.fr/site2004/oxydantreducteur.html
                ('F2', '{F -}'),
                ('PbO2', 'PbSO4'),
                ('{MnO4 -}', '{Mn 2+}'),
                ('{Au 3+}', 'Au'),
                ('{ClO4 -}', '{Cl -}'),
                ('Cl2', '{Cl -}'),
                ('HNO2', 'N2O'),
                ('{Cr2O7 2-}', '{Cr 3+}'),
                ('O2', 'H2O'),
                ('MnO2', '{Mn 2+}'),
                ('Br2', '{Br -}'),
                ('{Fe 2+}', 'Fe'),
            ]
        ],
        'acide/base': [
            (
                utile.convertie_notation(e1),
                utile.convertie_notation(e2)
            )
            for e1, e2 in [
                # Source listant les couples :
                #  https://fr.wikipedia.org/wiki/R%C3%A9action_acido-basique#Quelques_couples_acide-base
                ('{H3O +}', 'H2O'),
                ('H2O', '{HO -}'),
                ('C2O4H2', '{HC2O4 -}'),
                ('{HC2O4 -}', '{C2O4 2-}'),
                ('H3PO4', '{H2PO4 -}'),
                ('{H2PO4 -}', '{HPO4 2-}'),
                ('CO2(H2O)', '{CO2(HO) -}'),
                ('{CO2(HO) -}', '{CO3 2-}'),
                ('H2SO4', '{HSO4 -}'),
                ('{HSO4 -}', '{SO4 2-}'),
                ('SO2(H2O)', '{SO2(HO) -}'),
                ('{SO2(HO) -}', '{SO3 2-}'),
                ('{NH3(OH) +}', 'NH2O'),

                ('{NH4 +}', 'NH3'),
                ('H3BO3', '{H2BO3 -}'),
                ('HCIO', '{CIO -}'),
                ('C2H5COOH', '{C2H5COO -}'),
                ('CH3COOH', '{CH3COO -}'),
                ('HCOOH', '{HCOO -}'),
                ('HF', '{F -}'),
            ]
        ]
    }


def get_produit(element: Any,  # noqa: ANN401
                categorie: str) -> list[tuple[str, Any]]:
    """Retourne la liste des couples associés à un élément.

    Chaque couple est un tuple `(role, partenaire)` :
    - pour `'acide/base'`, le rôle est `'acide'` ou `'base'` ;
    - pour les autres catégories (dont `'oxydoreduction'`),
       le rôle est `'oxydant'` ou `'reducteur'`.

    Lève `ValeurIncorrecte` si aucun couple ne comporte cet élément.
    """

    if not couples:
        __maj()

    if categorie not in couples:
        raise exception.ValeurIncorrecte(
            "La catégorie de couple '%s' n'existe pas." % categorie
        )

    if categorie == 'acide/base':
        role_1, role_2 = 'acide', 'base'
    else:
        role_1, role_2 = 'oxydant', 'reducteur'

    produits = [
        (role_1, e2) if e1 == element else (role_2, e1)
        for e1, e2 in couples[categorie]
        if e1 == element or e2 == element
    ]

    if not produits:
        raise exception.ValeurIncorrecte(
            "Le couple comportant l'élément %s n'est pas connu du module."
            % repr(element)
            + " N'hésitez pas à l'ajouter."
        )

    return produits
