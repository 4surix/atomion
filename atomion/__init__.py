# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------


"""

Module utilitaire pour les atomes, ions et molécules.

Ce module a pour but de manipuler des atomes, ions et molécules,
 ainsi que d'avoir des informations respectives à ces éléments.

Je suis très loin d'être proffesionelle dans ce domaine,
 donc il est fort probable qu'il y est des erreurs.

Toutes amélioration et suggestion sont la bienvenue.

Lien du github : https://github.com/4surix/atomion

"""


__version__ = '1.8.0'


from . import exception
from .objets import *
from .utile import mol, params
from .utile.acido_basique import AcidoBasique
from .utile.equation import DemiEquation, Equation, Reaction
from .utile.oxydo_reduction import OxydoReduction

__all__ = (
    'AcidoBasique',
    'Atome',
    'DemiEquation',
    'Electron',
    # Équations et réactions
    'Equation',
    'Ion',
    'IonMonoAtomique',
    'IonPolyAtomique',
    'Liaison',
    'Molecule',
    'MoleculeOrganique',
    'Neutron',
    'Noyau',
    'OxydoReduction',
    'Proton',
    'QDown',
    'QUp',
    # Objets
    'Quark',
    'Reaction',
    'exception',
    'mol',
    # Divers
    'params',
)
