# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Noyau,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional


###>>> CAPTURE FICHIER CALC

class Atome:

    __slots__ = (
        'nom', 'symbole', 'categorie',
        'proton', 'neutron', 'nucleon', 'electron', 
        'masse', 'masse_atomique_relative', 
        'configuration', 'couches', 'noyau',
        'electronegativite'
    )

    def __init__(self, 
            valeur:Union[int, str, IonMonoAtomique], 
            *args,
            neutron:Optional[int] = None
        ) -> None:

        utile.get_info(self, valeur)

        self.neutron = neutron or round(self.masse_atomique_relative) - self.proton
        self.electron = self.proton
        self.nucleon = self.proton + self.neutron
        self.masse = utile.get_masse(self)
        self.configuration = utile.configuration_electronique(self)
        self.noyau = Noyau(Proton(self.proton), Neutron(self.neutron))

    def __add__(self,
            obj: Union[Proton, Neutron, Electron, Atome]
        ) -> Union[Atome, Molecule, IonMonoAtomique]:

        if isinstance(obj, Proton):
            return Atome(self.proton + obj.valeur)

        elif isinstance(obj, Neutron):
            return Atome(self.proton, neutron = self.neutron + obj.valeur)

        elif isinstance(obj, Electron):
            # Si on ajoute des electrons la charge est négatif.
            return IonMonoAtomique(self.proton, charge = -obj.valeur)

        elif isinstance(obj, Atome):
            return Molecule([self, obj])

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, 
            obj: Union[Proton, Neutron, Electron, Atome]
        ) -> Union[Atome, Molecule, IonMonoAtomique]:
        return self + obj

    def __sub__(self, 
            obj: Union[Proton, Neutron, Electron]
        ) -> Union[Atome, IonMonoAtomique]:

        if isinstance(obj, Proton):
            return Atome(self.proton - obj.valeur)

        elif isinstance(obj, Neutron):
            return Atome(self.proton, neutron = self.neutron - obj.valeur)

        elif isinstance(obj, Electron):
            # Si on enlève des electrons la charge est positif.
            return IonMonoAtomique(self.proton, charge = +obj.valeur)

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self, 
            obj: Union[Proton, Neutron, Electron]
        ) -> Union[Atome, IonMonoAtomique]:
        return self - obj

    def __mul__(self, obj: int) -> Molecule:
        return Molecule([self] * obj)

    def __rmul__(self, obj: int) -> Molecule:
        return self * obj

    def __str__(self) -> str:
        str__ = (
            "Atome %s" % self.notation()
            + (
                "\n Elément: %s" % self.nom[utile.params.langue] 
                if utile.params.nom else ''
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
                "\n Masse atomique relative: %s" 
                % self.masse_atomique_relative
                if utile.params.masse_relative else ''
            )
            + (
                "\n Couche électronique: %s" % self.notation_couche() 
                if utile.params.couches else ''
            )
            + (
                "\n Configuration électronique: %s" 
                % self.notation_configuration()
                if utile.params.configuration else ''
            )
        )

        return (
            str__ if not utile.params.calculatrice
            else
                str__.replace('è', 'e').replace('é', 'e')
        )

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def notation(self) -> str:
        return "%s Z=%s A=%s" % (
            self.symbole, self.proton, self.proton + self.neutron
        )

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:

        return "%s%s%s" % (
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
        )

    
    notation_couche = utile.notation_couche

    notation_configuration = utile.notation_configuration

###<<< CAPTURE FICHIER CALC


objets.Atome = Atome

def MAJ_TYPE():
    variables = globals()
    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)