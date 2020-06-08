
### 

class Neutron:
    
    __slots__ = ('valeur')


class Proton:

    __slots__ = ('valeur')


class Electron:

    __slots__ = ('valeur')


### 

class Atome:

    __slots__ = ('élément', 'symbole', 'catégorie',
                 'proton', 'neutron', 'nucléon', 'électron', 
                 'masse', 'masse_atomique_relative', 
                 'configuration', 'couches')


class Ion:

    __slots__ = ('élément', 'symbole', 'catégorie', 
                 'proton', 'neutron', 'électron', 'nucléon',
                 'masse', 'masse_atomique_relative',
                 'configuration', 'couches', 
                 'diff', 'charge')


### 

class Molécule:

    __slots__ = ('atomes', 
                 'proton', 'neutron', 'électron', 
                 'masse', 'masse_moléculaire_relative')