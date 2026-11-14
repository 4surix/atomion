# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Exceptions pédagogiques utilisées par la bibliothèque atomion."""

from __future__ import annotations

from typing import Any


class Incompatible(Exception):
	"""Exception levée quand deux objets ne sont pas compatibles entre eux."""

	def __init__(self, objet_1: Any,  # noqa: ANN401
                 objet_2: Any) -> None:  # noqa: ANN401
		"""Initialise l'exception avec les deux objets incompatibles.

		Args:
			objet_1: Premier objet.
			objet_2: Second objet.
		"""
		self.description = (
			"Objet '%s' non compatible avec objet '%s'."
			% (type(objet_1), type(objet_2))
		)

	def __str__(self) -> str:
		"""Retourne la description de l'incompatibilité."""
		return self.description


class Instable(Exception):
	"""Exception levée quand une espèce chimique est instable."""

	def __init__(self, element: Any) -> None:  # noqa: ANN401
		"""Initialise l'exception avec l'élément instable.

		Args:
			element: L'atome ou l'ion instable.
		"""
		self.description = (
			"L'élément '%s' est instable !" % element.notation_symbole()
		)

	def __str__(self) -> str:
		"""Retourne la description de l'instabilité."""
		return self.description


class ValeurIncorrecte(Exception):
	"""Exception levée quand une valeur fournie est incorrecte."""

	def __init__(self, description: str) -> None:
		"""Initialise l'exception avec une description.

		Args:
			description: Description de la valeur incorrecte.
		"""
		self.description = description

	def __str__(self) -> str:
		"""Retourne la description de la valeur incorrecte."""
		return self.description
