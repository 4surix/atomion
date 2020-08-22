
class Incompatible(Exception):

	def __init__(self, objet_1, objet_2):

		self.description = (
			"Objet '%s' non compatible avec objet '%s'."
			% (type(objet_1), type(objet_2))
		)

	def __str__(self):

		return self.description


class MoleculeInstable(Exception):

	def __init__(self, molecule):

		self.description = (
			"La molécule '%s' est instable !" % molecule.notation()
		)

	def __str__(self):

		return self.description


class ValeurIncorrecte(Exception):

	def __init__(self, description):

		self.description = description

	def __str__(self):

		return self.description