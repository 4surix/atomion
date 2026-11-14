# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Test de fumee execute par MicroPython 1.9.4 (calculatrice).

https://en.wikipedia.org/wiki/Smoke_testing_(software)

Ce script ne depend que du fichier unique `atomion.py` 
 produit par `mk_file_calculatrice.py`
 et doit donc rester compatible MicroPython 1.9.4 :
 pas de f-string, pas d'`unittest`, pas de `typing`.

Usage :
    cd <dossier contenant atomion.py>
    micropython smoke_calculatrice.py
"""

import atomion


# Le mode calculatrice doit etre actif : sinon ce test ne verifie rien.
assert atomion.params.calculatrice is True, 'mode calculatrice inactif'

# Objets et tableau periodique
assert atomion.Atome('C').symbole == 'C'
assert atomion.Atome('C').notation_symbole() == 'C'

# Ions (affichage ASCII propre au mode calculatrice)
assert atomion.Ion('Cl').notation_symbole() == '{Cl 1-}'
assert atomion.Ion('CO3').notation_symbole() == '{CO3 2-}'

# Molecules et equations
assert atomion.Molecule('H2O').notation_symbole() == 'H2O'
assert (
    str(atomion.Equation('H2 + O2 -> H2O').equilibrer())
    == '2 H2 + O2 -> 2 H2O'
)

# Regression : `couples` doit etre present dans le fichier unique
couple = atomion.get_produit(atomion.Atome('Fe'), 'oxydoreduction')
assert couple[0][0] == 'reducteur', couple

print('OK')
