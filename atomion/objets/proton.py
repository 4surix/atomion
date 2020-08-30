# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

"""

Objet d'un nombre de proton servant pour les opérations.

--------
Augument

valeur
    :objets.Atome
        Récupére le nombre de proton de l'objets.Atome.
    :Ion
        Récupére le nombre de proton de l'ion.
    :int
        Définie le nombre de proton.

-------
Retours

:Proton
    .valeur:int
        Nombre de proton
"""

from . import base
from .. import exception
from .. import objets


class Proton:

    __slots__ = ('valeur')

    def __init__(self, valeur=1):

        if isinstance(valeur, (objets.Atome, objets.Ion)):
            self.valeur = valeur.proton

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Proton'."
            )

base.Proton = Proton