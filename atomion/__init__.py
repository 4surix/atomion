# coding: utf-8

"""Module utilitaire pour les atomes, ions et Molécules.

Ce module a pour but de manipuler des atomes, ions et Molécules, 
 ainsi que d'avoir des informations respectives à ces éléments.

Je suis très loin d'être proffesionelle dans ce domaine,
 donc il est fort probable qu'il y est des erreurs.

Tout amélioration est la bienvenue.

Lien du github : https://github.com/4surix/atomion
"""


__version__ = '1.0.1'


from .objets import (
	molecule, atome, ion, electron, proton, neutron, # Modules
	Molécule, Atome, Ion, Electron, Proton, Neutron  # Objets
)