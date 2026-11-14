# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------

"""Génère `atomion.py`, la version « fichier unique » pour calculatrices.

Le fichier est construit en concaténant les blocs délimités par
`###>>> CAPTURE FICHIER CALC` et `###<<< CAPTURE FICHIER CALC` des modules du
paquet, puis (si `python_minifier` est installé) minifié.

Usage :
    python mk_file_calculatrice.py
"""

import os

try: import python_minifier
except ImportError:
    python_minifier = None


RACINE = os.path.dirname(os.path.abspath(__file__))


TEXTE_DEPART = """
# coding: utf-8
# Python 3.9
#
# Atomion - manipulation of atoms, ions and molecules.
# Copyright (C) 2026 Asurix
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# ----------------------------------------------------------------------------
"""

# L'ordre est important
parties = [
    # Obligatoire
    '__init__.py',
    'elements.py',
    'exception.py',
    'irregularites.py',
    'utile/typing.py',
    'objets/__init__.py',
    'utile/utile.py',
    'objets/atome.py',
    'objets/electron.py',
    'objets/ion.py',
    'objets/molecule.py',
    'objets/neutron.py',
    'objets/proton.py',
    'objets/liaison.py',
    # Peut être retiré si pas besoin
    'objets/noyau.py',
    'utile/equation.py',
    'objets/quark.py',
    'raccourcis.py',
    'couples.py',
    'utile/oxydo_reduction.py',
    'utile/acido_basique.py'
]


def generer():
    """Retourne le contenu du fichier `atomion.py` (sans l'écrire)."""

    texte = TEXTE_DEPART

    for partie in parties:

        with open(os.path.join(RACINE, 'atomion', partie), encoding='utf-8') as fichier:

            capture = False

            for ligne in fichier:

                if ligne.strip() == '###>>> CAPTURE FICHIER CALC':
                    capture = True
                elif ligne.strip() == '###<<< CAPTURE FICHIER CALC':
                    capture = False
                elif capture:
                    texte += (
                        ligne
                        .replace('utile.', '')
                        .replace('exception.', '')
                        .replace('irregularites.', '')
                        .replace('objets.', '')
                        .replace('couples.', '')
                    )

    if python_minifier:
        texte = python_minifier.minify(
            texte,
            filename=None,
            remove_annotations=True,
            remove_pass=True,
            remove_literal_statements=True,
            combine_imports=True,
            hoist_literals=True,
            rename_locals=True,
            preserve_locals=None,
            rename_globals=True,
            preserve_globals=[
                # Objets
                'Neutron',
                'Proton',
                'Electron',
                'Atome',
                'Molecule',
                'Ion',
                'IonMonoAtomique',
                'IonPolyAtomique',
                'Noyau',
                'Quark',
                'QUp',
                'QDown',
                'Equation',
                'Reaction',
                # Globales
                'params',
                'u',
                'mol',
                # Exceptions
                'ValeurIncorrecte',
                'Instable',
                'Incompatible'
            ],
            remove_object_base=True,
            convert_posargs_to_args=True
        )

    return texte


def main():

    with open('atomion.py', 'w', encoding='utf-8') as fichier:
        fichier.write(generer())


if __name__ == '__main__':
    main()
