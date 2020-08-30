# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

"""

Objet d'un nombre d'électron servant pour les opérations.

--------
Augument

valeur
    :objets.Atome
        Récupére le nombre d'électron de l'objets.Atome.
    :Ion
        Récupére le nombre d'électron de l'ion.
    :int
        Définie le nombre d'électron.

-------
Retours

:Electron
    .valeur:int
        Nombre d'électron
"""

from . import base
from .. import exception
from .. import objets


class Electron:

    __slots__ = ('valeur')

    def __init__(self, valeur=1):

        if isinstance(valeur, (objets.Atome, objets.Ion)):
            self.valeur = valeur.electron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Electron'."
            )

base.Electron = Electron