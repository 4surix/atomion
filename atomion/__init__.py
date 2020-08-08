# coding: utf-8

"""Module utilitaire pour les atomes, ions et molécules.

Ce module a pour but de manipuler des atomes, ions et molécules, 
 ainsi que d'avoir des informations respectives à ces éléments.

Je suis très loin d'être proffesionelle dans ce domaine,
 donc il est fort probable qu'il y est des erreurs.

Tout amélioration et suggestion sont la bienvenue.

Lien du github : https://github.com/4surix/atomion
"""


__version__ = '1.0.2'


from .utile import params
from . import exception

from .objets import (
	molecule, atome, ion, electron, proton, neutron, # Modules
	Molécule, Atome, Ion, Electron, Proton, Neutron  # Objets
)