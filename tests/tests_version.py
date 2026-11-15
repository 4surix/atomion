# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

import re
import unittest

import atomion
from pathlib import Path


RACINE = Path(__file__).resolve().parent.parent


class TestVersion(unittest.TestCase):

    def test_versions_coherentes(self):
        # La version déclarée dans `pyproject.toml` doit correspondre
        #  exactement à `atomion.__version__`.
        with Path(RACINE, 'pyproject.toml').open(encoding='utf-8') as fichier:
            contenu = fichier.read()

        version = re.search(
            r'(?m)^version\s*=\s*"([^"]+)"', contenu
        ).group(1)

        self.assertEqual(version, atomion.__version__)


if __name__ == '__main__':
    unittest.main()
