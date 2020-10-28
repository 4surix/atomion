# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


TEXTE = """
# -*- coding: utf-8 -*-
# Python 3.6.2 / MicroPython 1.9.4
# ----------------------------------------------------------------------------
"""

# L'ordre est important
parties = [
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
    'objets/noyau.py',
    'objets/proton.py',
    'objets/quark.py',
    'utile/equation.py'
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


with open('atomion.py', 'w', encoding='utf-8') as fichier:
    fichier.write(TEXTE)