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

from .base import Molécule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur=1):

    if isinstance(valeur, (Atome, Ion)):
        self.valeur = valeur.neutron

    elif isinstance(valeur, int):
        self.valeur = valeur

Neutron.__init__ = __init