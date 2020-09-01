# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


class Incompatible(Exception):

	def __init__(self, objet_1, objet_2):

		self.description = (
			"Objet '%s' non compatible avec objet '%s'."
			% (type(objet_1), type(objet_2))
		)

	def __str__(self):

		return self.description


class Instable(Exception):

	def __init__(self, element):

		self.description = (
			"L'élément '%s' est instable !" % element.notation_symbole()
		)

	def __str__(self):

		return self.description


class ValeurIncorrecte(Exception):

	def __init__(self, description):

		self.description = description

	def __str__(self):

		return self.description