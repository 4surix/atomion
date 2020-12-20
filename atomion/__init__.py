# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

###>>> CAPTURE FICHIER CALC

"""

Module utilitaire pour les atomes, ions et molécules.

Ce module a pour but de manipuler des atomes, ions et molécules, 
 ainsi que d'avoir des informations respectives à ces éléments.

Je suis très loin d'être proffesionelle dans ce domaine,
 donc il est fort probable qu'il y est des erreurs.

Toutes amélioration et suggestion sont la bienvenue.

Lien du github : https://github.com/4surix/atomion

"""


__version__ = '1.3.0'

###<<< CAPTURE FICHIER CALC


from .objets import *
from .utile import params, mol
from .utile.equation import Equation, Reaction
from .utile.oxydo_reduction import OxydoReduction
from . import exception