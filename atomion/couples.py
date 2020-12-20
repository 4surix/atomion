# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

from . import utile


couples = []

def __maj():

    global couples

    couples = [
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
            ('Fe', '{Fe 2+}')
        ]
    ]


def get_produit(element):

    if not couples:
        __maj()

    for e1, e2 in couples:

        if e1 == element:
            return e2

        if e2 == element:
            return e1