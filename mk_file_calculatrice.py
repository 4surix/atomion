# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


try: import python_minifier
except ImportError:
    python_minifier = None


TEXTE = """
# -*- coding: utf-8 -*-
# Python 3.6.2 / MicroPython 1.9.4
# ----------------------------------------------------------------------------
"""

# L'ordre est important
parties = [
    # Obligatoire
    '__init__.py',
    'elements.py',
    'exception.py',
    'irregularites.py',
    'objets/__init__.py',
    'utile/utile.py',
    'objets/atome.py',
    'objets/electron.py',
    'objets/ion.py',
    'objets/molecule.py',
    'objets/neutron.py',
    'objets/proton.py',
    # Peut être retiré si pas besoin
    'objets/noyau.py',
    'utile/equation.py',
    'objets/quark.py',
    'raccourcis.py'
]

for partie in parties:

    with open('atomion/' + partie, encoding='utf-8') as fichier:

        capture = False

        for ligne in fichier:

            if ligne.strip() == '###>>> CAPTURE FICHIER CALC':
                capture = True
            elif ligne.strip() == '###<<< CAPTURE FICHIER CALC':
                capture = False
            elif capture:
                TEXTE += (
                    ligne
                    .replace('utile.', '')
                    .replace('exception.', '')
                    .replace('irregularites.', '')
                    .replace('objets.', '')
                )


if python_minifier:
    TEXTE = python_minifier.minify(
        TEXTE,
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
            'params',
            'ValeurIncorrecte',
            'Instable',
            'Incompatible'
        ],
        remove_object_base=True,
        convert_posargs_to_args=True
    )


with open('atomion.py', 'w', encoding='utf-8') as fichier:
    fichier.write(TEXTE)