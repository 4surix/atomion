
### 

class Neutron:
    
    __slots__ = ('valeur')


class Proton:

    __slots__ = ('valeur')


class Electron:

    __slots__ = ('valeur')


### 

class Atome:

    __slots__ = ('element', 'symbole', 'categorie',
                 'proton', 'neutron', 'nucleon', 'electron', 
                 'masse', 'masse_atomique_relative', 
                 'configuration', 'couches')


class Ion:

    __slots__ = ('element', 'symbole', 'categorie', 
                 'proton', 'neutron', 'electron', 'nucleon',
                 'masse', 'masse_atomique_relative',
                 'configuration', 'couches', 
                 'diff', 'charge')


### 

class Molecule:

    __slots__ = ('atomes', 
                 'proton', 'neutron', 'electron', 
                 'masse', 'masse_moleculaire_relative')