"""

Objet d'un nombre d'électron servant pour les opérations/

--------
Augument

valeur
    :Atome
        Récupére le nombre d'éléctron de l'atome.
    :Ion
        Récupére le nombre d'éléctron de l'ion.
    :int
        Définie le nombre d'éléctron.

-------
Retours

:Electron
    .valeur:int
        Nombre d'électron
"""

from .. import exception

from .base import Molécule, Atome, Ion, Electron, Proton, Neutron


def __init(self, valeur=1):

    if isinstance(valeur, (Atome, Ion)):
        self.valeur = valeur.électron

    elif isinstance(valeur, int):
        self.valeur = valeur

    else:
        raise exception.ValeurIncorrecte(
            "Seulement les objets de type 'Atome', 'Ion' et 'int'"
            + " peuvent être transformés en objet de type 'Electron'."
        )

Electron.__init__ = __init