# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

# Atomion — manipulation d'atomes, ions et molécules.
# Copyright (C) 2026 Asurix
#
# Ce programme est un logiciel libre : vous pouvez le redistribuer et/ou le
# modifier selon les termes de la GNU Affero General Public License, version 3
# ou ultérieure (AGPL-3.0-or-later), publiée par la Free Software Foundation.
# Voir le fichier LICENSE pour le texte complet.

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


__version__ = '1.6.1'

###<<< CAPTURE FICHIER CALC


from .objets import *
from .utile import params, mol
from .utile.equation import Equation, Reaction, DemiEquation
from .utile.oxydo_reduction import OxydoReduction
from .utile.acido_basique import AcidoBasique
from . import exception