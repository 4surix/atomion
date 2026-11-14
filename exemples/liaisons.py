# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

from atomion import *
from atomion.raccourcis import *

assert Liaison(C, H).polarisee == False
assert Liaison(O, H).polarisee == True
