# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import os
import re
import unittest

import atomion


RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestVersion(unittest.TestCase):

    def test_versions_coherentes(self):
        # La version déclarée dans `pyproject.toml` doit correspondre
        #  exactement à `atomion.__version__`.
        with open(
            os.path.join(RACINE, 'pyproject.toml'), encoding='utf-8'
        ) as fichier:
            contenu = fichier.read()

        version = re.search(
            r'(?m)^version\s*=\s*"([^"]+)"', contenu
        ).group(1)

        self.assertEqual(version, atomion.__version__)


if __name__ == '__main__':
    unittest.main()
