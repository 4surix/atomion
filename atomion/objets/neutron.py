# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

"""

Objet d'un nombre de neutron servant pour les opérations.

--------
Augument

valeur
    :Atome
        Récupére le nombre de neutron de l'atome.
    :Ion
        Récupére le nombre de neutron de l'ion.
    :int
        Définie le nombre de neutron.

-------
Retours

:Neutron
    .valeur:int
        Nombre de neutron
"""

from . import base
from .. import objets
from .. import exception


class Neutron:
    
    __slots__ = ('valeur')

    def __init__(self, valeur=1):

        if isinstance(valeur, (objets.Atome, objets.Ion)):
            self.valeur = valeur.neutron

        elif isinstance(valeur, int):
            self.valeur = valeur

        else:
            raise exception.ValeurIncorrecte(
                "Seulement les objets de type 'Atome', 'Ion' et 'int'"
                + " peuvent être transformés en objet de type 'Neutron'."
            )

base.Neutron = Neutron