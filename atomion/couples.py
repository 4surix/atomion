# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from . import utile
from . import exception


###>>> CAPTURE FICHIER CALC

import json
import os


# Chemin du fichier de couples personnalisés, relatif au module
#  (et non au répertoire courant) pour être indépendant du CWD.
try:
    FICHIER_COUPLES = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'couples.json'
    )
except Exception:
    # MicroPython : `os.path` peut être indisponible.
    FICHIER_COUPLES = 'couples.json'


couples = {}

def __maj():

    global couples

    data = None

    try:
        with open(FICHIER_COUPLES) as fichier:
            data = json.loads(fichier.read())
    except OSError:
        data = None


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

                *(data.get('oxydoreduction', []) if data else [])
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

                *(data.get('acide/base', []) if data else [])
            ]
        ]
    }


def get_produit(element, categorie):
    """Retourne la liste des couples associés à un élément.

    Chaque couple est un tuple `(role, partenaire)` :
    - pour `'acide/base'`, le rôle est `'acide'` ou `'base'` ;
    - pour les autres catégories (dont `'oxydoreduction'`),
       le rôle est `'oxydant'` ou `'reducteur'`.

    Lève `ValeurIncorrecte` si aucun couple ne comporte cet élément.
    """

    if not couples:
        __maj()

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

###<<< CAPTURE FICHIER CALC