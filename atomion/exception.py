
class Incompatible(Exception):

	def __init__(self, objet_1, objet_2):

		self.description = (
			"Objet '%s' non compatible avec objet '%s'."
			% (objet_1.__class__.__name__, objet_2.__class__.__name__)
		)

	def __str__(self):

		return self.description


class MoleculeInstable(Exception):

	def __init__(self, molecule):

		self.description = (
			f"La molécule '{molecule.notation()}' est instable !"
		)

	def __str__(self):

		return self.description


class ValeurIncorrecte(Exception):

	def __init__(self, description):

		self.description = description

	def __str__(self):

		return self.description