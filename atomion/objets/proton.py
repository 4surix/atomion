"""

Objet d'un nombre de proton servant pour les opérations.

--------
Augument

valeur
    :Atome
        Récupére le nombre de proton de l'atome.
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

from .base import Molécule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur=1):

    if isinstance(valeur, (Atome, Ion)):
        self.valeur = valeur.proton

    elif isinstance(valeur, int):
        self.valeur = valeur

Proton.__init__ = __init