# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

"""

Objet IonMonoAtomique.

---------
Arguments

valeur
    :objets.Atome
        Transforme l'objets.Atome en IonMonoAtomique.
    :Ion
        Léve une erreur
    :int
        Equivaut au nombre de proton et créer un IonMonoAtomique.

-------
Retours

:Ion
    .element:str
    .symbole:str
    .categorie:str

    .proton:int
    .neutron:int
    .electron:int
    .nucleon:int

    .masse:float
    .masse_atomique_relative:float

    .couches:list
    .configuration:list

    .diff:int
        Différence entre le nombre de proton et d'électron
    .charge:str
        Charges électrique de l'ion

    .notation()
    .notation_symbole()
    .notation_couche()
    .notation_configuration()
"""

from . import base
from .. import utile
from .. import objets
from .. import exception


class Ion:
    
    def __new__(cls, *args, **kwargs):

        try: return IonMonoAtomique(*args, **kwargs)
        except Exception as exception_IMA:
            try: return IonPolyAtomique(*args, **kwargs)
            except Exception as exception_IPA:
                raise exception_IMA

base.Ion = Ion


class IonMonoAtomique(Ion):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    __slots__ = (
        'element', 'symbole', 'categorie', 
        'proton', 'neutron', 'electron', 'nucleon',
        'masse', 'masse_atomique_relative',
        'configuration', 'couches', 
        'diff', 'charge'
    )

    def __init__(self, valeur=1, electron=0, neutron=None):

        self.neutron = neutron

        utile.get_info(self, valeur)

        drn_couche = self.couches[-1]

        if 0 < drn_couche < 5:
            self.electron = self.proton - drn_couche
            self.charge = '+'
            del self.couches[-1]

        elif 4 < drn_couche < 8:
            self.electron = self.proton + (8 - drn_couche)
            self.charge = '-'
            self.couches[-1] = 8

        else:
            raise exception.ValeurIncorrecte(
                "Un gaz noble ne peut pas devenir un ion monoatomique."
            )


        if self.neutron is None:
            self.neutron = round(self.masse_atomique_relative) - self.proton

        self.diff = abs(self.proton - self.electron)

        self.masse = utile.get_masse(self)

        self.nucleon = self.proton + self.neutron

        self.configuration = utile.configuration_electronique(self)

    def __add__(self, obj):

        if isinstance(obj, Proton):
            return Ion(self.proton + obj.valeur)

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, obj):
        return self + obj

    def __sub__(self, obj):

        if isinstance(obj, Proton):
            return objets.Atome(self.proton - obj.valeur)

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self, obj):
        return self - obj

    def __str__(self): 
        str__ = (
            "Ion monoatomique %s" % self.notation()
            + (
                "\n Elément: %s" % self.element[utile.params.langue] 
                if utile.params.element else ''
            )
            + (
                "\n Catégorie: %s" % self.categorie[utile.params.langue] 
                if utile.params.categorie else ''
            )
            + (
                "\n Proton(s): %s" % self.proton 
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): %s" % self.neutron 
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): %s" % self.electron 
                if utile.params.electron else ''
            )
            + (
                "\n Masse: %s" % self.masse 
                if utile.params.masse else ''
            )
            + (
                "\n Masse atomique relative: %s" % self.masse_atomique_relative
                if utile.params.masse_relative else ''
            )
            + (
                "\n Couche électronique: %s" % self.notation_couche() 
                if utile.params.couches else ''
            )
            + (
                "\n Configuration électronique: %s" % self.notation_configuration()
                if utile.params.configuration else ''
            )
        )

        return (
            str__ if not utile.params.calculatrice
            else
                str__.replace('è', 'e').replace('é', 'e')
        )

    def __repr__(self):
        return self.notation_symbole()

    def notation(self):
        return "%s %s%s Z=%s A=%s" % (
            self.symbole, 
            self.diff, 
            self.charge, 
            self.proton, 
            self.proton + self.neutron
        )

    def notation_symbole(self, A=True, Z=True):
        return "%s%s%s%s%s" % (
            '' if not A or utile.params.calculatrice
            else
                ''.join(
                    utile.exposants[int(num)] 
                    for num in str(self.proton + self.neutron)
                )
            ,
            '' if not Z or utile.params.calculatrice
            else
                ''.join(
                    utile.sous_exposants[int(num)] 
                    for num in str(self.proton)
                )
            ,
            self.symbole
            ,
            nbr if utile.params.calculatrice
            else
                ''.join(
                    utile.exposants[int(num)] 
                    for num in str(self.diff)
                )
            ,
            {
                '-': '⁻' if not utile.params.calculatrice else '-',
                '+': '⁺' if not utile.params.calculatrice else '+'
            }.get(self.charge)
        )

    notation_couche = utile.notation_couche

    notation_configuration = utile.notation_configuration

base.IonMonoAtomique = IonMonoAtomique

"""
Objet IonPolyAtomique.

---------
Arguments

valeur
    :str
        Notation de la molécule qui sera decodée.

------
Retour

:Molecule
    .ions:list
        Liste de tout les :IonMonoAtomique composant l':IonPolyAtomique.

    .proton:int
        Nombre total de proton.
    .neutron:int
        Nombre total de neutron.
    .electron:int
        Nombre total d'électron.
    .nucleon:int
        Nombre total de nucléon.

    .masse:float
    .masse_moleculaire_relative:float

    .notation()
"""


class IonPolyAtomique(Ion):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    __slots__ = (
        'ions', 
        'proton', 'neutron', 'electron', 'nucleon',
        'masse', 'masse_moleculaire_relative'
    )

    def __init__(self, valeur, *, verif_stable=False):

        self.ions = (
            utile.convertie_notation_vers_atomes(valeur) 
            if isinstance(valeur, str) else valeur
        )

        if len(self.ions) < 2:
            raise exception.ValeurIncorrecte(
                "Un ion polyatomique doit être composé de plusieurs éléments."
            )

        if verif_stable:
            utile.verif_stable(self.ions)

        charge = sum(
            int('%s%s' % ion.charge, ion.diff)
            for ion in self.ions
        )

        self.proton = sum(ion.proton for ion in self.ions)
        self.neutron = sum(ion.neutron for ion in self.ions)
        self.electron = sum(ion.electron for ion in self.ions)

        self.nucleon = self.proton + self.neutron

        self.masse = sum(ion.masse for ion in self.ions)
        self.masse_moleculaire_relative = sum(
            ion.masse_atomique_relative 
            for ion in self.ions
        )

    def __str__(self):

        str__ = (
            "Ion polyatomique %s" % self.notation()
            + (
                "\n Proton(s): %s" % self.proton
                if utile.params.proton else ''
            )
            + (
                "\n Neutron(s): %s" % self.neutron
                if utile.params.neutron else ''
            )
            + (
                "\n Electron(s): %s" % self.electron
                if utile.params.electron else ''
            )
            + (
                "\n Masse: %s" % self.masse
                if utile.params.masse else ''
            )
            + (
                "\n Masse moléculaire relative: %s"
                % (self.masse_moleculaire_relative)
                if utile.params.masse_relative else ''
            )
        )

        return (
            str__ if not utile.params.calculatrice
            else
                str__.replace('è', 'e').replace('é', 'e')
        )

    def __repr__(self):
        return self.notation()

    def __add__(self, obj):

        if isinstance(obj, Molecule):

            ions = self.ions[:]
            ions.extend(obj.ions)
            return Molecule(ions)

        elif isinstance(obj, objets.Atome):

            ions = self.ions[:]
            ions.append(obj)
            return Molecule(ions)

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, obj):
        return self + obj

    def __sub__(self, obj):

        if isinstance(obj, Molecule):

            ions = self.ions[:]
            for ion in obj.ions:
                ions.remove(ion)
            return Molecule(ions)

        elif isinstance(obj, objets.Atome):

            ions = self.ions[:]
            ions.remove(obj)
            return Molecule(ions)

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self, obj):
        return self - obj

    def notation(self):

        ions = {}

        for atome in self.ions:
            atome = atome.notation_symbole(A=False, Z=False)
            if atome not in ions:
                ions[atome] = 0
            ions[atome] += 1

        return ''.join(
            '%s%s' % (
                atome,
                '' if nbr == 1
                else
                    nbr if not utile.params.calculatrice
                    else
                        ''.join(
                            utile.sous_exposants[int(num)] 
                            for num in str(nbr)
                        )
            )
            for atome, nbr in ions.items()
        )


base.IonPolyAtomique = IonPolyAtomique