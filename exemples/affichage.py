from atomion import *


print('\n\n> Quark: \n')
print(Quark(+ 2/3, 'R'))

print('\n\n> Proton: \n')
print(Proton(3))

print('\n\n> Neutron: \n')
print(Neutron(6))

print('\n\n> Electron: \n')
print(Electron(9))

print('\n\n> Noyau: \n')
print(Noyau(Proton(6), Neutron(6)))

print('\n\n> Atome: \n')
print(Atome('C'))

print('\n\n> Molecule: \n')
print(Molecule('O2'))

print('\n\n> Ions monoatomique: \n')
print(Ion('K'))

print('\n\n> Ions polyatomique: \n')
print(Ion('CO2'))

# Paramètrer affichage

params.config(
    calculatrice = False,
    langue = 'fr',
    element = True,
    categorie = True,
    proton = True,
    neutron = True,
    electron = True,
    masse = True,
    masse_relative = True,
    couches = True,
    configuration = True
)