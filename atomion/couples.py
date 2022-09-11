# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from . import utile
from . import exception


couples = {}

def __maj():

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
                ('Fe', '{Fe 2+}'),
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


def get_produit(element, categorie):

    if not couples:
        __maj()

    if categorie == 'acide/base':
        return [
            ('acide', e2) if e1 == element
            else 
                ('base', e1) if e2 == element
                else
                    None
            for e1, e2 in couples[categorie]
            if e1 == element or e2 == element
        ]

    else:
        for e1, e2 in couples[categorie]:

            if e1 == element:
                return e2

            if e2 == element:
                return e1

    raise exception.ValeurIncorrecte(
        f"Le couple comportant l'élément {repr(element)} n'est pas connu du module."
        + " N'hésitez pas à l'ajouter."
    )