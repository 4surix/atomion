# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------


from .. import objets
from ..objets import (
    Atome, Molecule,
    Ion, IonMonoAtomique, IonPolyAtomique,
    Electron, Proton, Neutron
)
from .. import utile
from .. import exception

from ..utile.typing import Union, Any, Optional, List


if utile.params.calculatrice:

    def Ion(*args, **kwargs):

        try: return IonMonoAtomique(*args, **kwargs)
        except Exception as exception_IMA:
            try: return IonPolyAtomique(*args, **kwargs)
            except Exception as exception_IPA:
                raise exception_IMA

    objets.Ion = Ion

    class Ion:
        pass

else:

    class Ion:
        
        def __new__(cls, *args, **kwargs):

            try: return IonMonoAtomique(*args, **kwargs)
            except Exception as exception_IMA:
                try: return IonPolyAtomique(*args, **kwargs)
                except Exception as exception_IPA:
                    raise exception_IMA

    objets.Ion = Ion


class IonMonoAtomique(Ion):
    """
    ### &doc_id ionMonoAtomique:class
    """

    if not utile.params.calculatrice:
        def __new__(cls, *args, **kwargs):
            return object.__new__(cls)

    __slots__ = (
        'element', 'symbole', 'categorie', 
        'proton', 'neutron', 'electron', 'nucleon',
        'masse', 'masse_atomique_relative',
        'configuration', 'couches', 
        'diff', 'charge'
    )

    def __init__(self, 
            valeur:Union[int, str, Atome],
            *args,
            neutron:Optional[int] = None
        ) -> None:
        """
        ### &doc_id ionMonoAtomique:init
        """

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

    def __add__(self, 
            obj: Union[Proton, Neutron, IonMonoAtomique]
        ) -> Union[Ion, IonPolyAtomique]:

        if isinstance(obj, Proton):
            return Ion(self.proton + obj.valeur)

        elif isinstance(obj, Neutron):
            return Ion(self.proton, neutron = self.neutron + obj.valeur)

        elif isinstance(obj, IonMonoAtomique):
            return IonPolyAtomique([self, obj])

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, 
            obj: Union[Proton, Neutron, IonMonoAtomique]
        ) -> Union[Ion, IonPolyAtomique]:
        return self + obj

    def __sub__(self, 
            obj: Union[Proton, Neutron]
        ) -> Ion:

        if isinstance(obj, Proton):
            return Ion(self.proton - obj.valeur)

        elif isinstance(obj, Neutron):
            return Ion(self.proton, neutron = self.neutron - obj.valeur)

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self, 
            obj: Union[Proton, Neutron]
        ) -> Ion:
        return self - obj

    def __str__(self) -> str: 
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

    def __repr__(self):
        return self.notation_symbole()

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def notation(self):
        """
        ### &doc_id ionMonoAtomique:notation
        """
        return "%s %s%s Z=%s A=%s" % (
            self.symbole, 
            self.diff, 
            self.charge, 
            self.proton, 
            self.proton + self.neutron
        )

    def notation_symbole(self, *args, A:bool = True, Z:bool = True):
        """
        ### &doc_id ionMonoAtomique:notation_symbole
        """
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
            self.diff if utile.params.calculatrice
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

objets.IonMonoAtomique = IonMonoAtomique


class IonPolyAtomique(Ion):
    """
    ### &doc_id ionPolyAtomique:class
    """

    if not utile.params.calculatrice:
        def __new__(cls, *args, **kwargs):
            return object.__new__(cls)

    __slots__ = (
        'ions', 
        'proton', 'neutron', 'electron', 'nucleon',
        'masse', 'masse_moleculaire_relative'
    )

    def __init__(self, 
            valeur:Union[str, Molecule, List[IonMonoAtomique]],
            *args,
            verif_stable:bool = False
        ) -> None:
        """
        ### &doc_id ionPolyAtomique:init
        """

        self.ions = (
            valeur if isinstance(valeur, list)
            else
                [
                    Ion(e) 
                    for e in valeur.atomes
                ] if isinstance(valeur, Molecule)
                else
                    utile.convertie_notation_vers('ions', valeur) 
        )

        if len(self.ions) < 2:
            raise exception.ValeurIncorrecte(
                "Un ion polyatomique doit être composé de plusieurs éléments."
            )

        if verif_stable:
            utile.verif_stable(self.ions)

        charge = sum(
            int('%s%s' % (ion.charge, ion.diff))
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

    def __str__(self) -> str:

        str__ = (
            "Ion polyatomique %s" % self.notation_symbole()
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

    def __add__(self, 
            obj: Union[IonMonoAtomique, IonPolyAtomique]
        ) -> IonPolyAtomique:

        if isinstance(obj, IonPolyAtomique):

            ions = self.ions[:]
            ions.extend(obj.ions)
            return IonPolyAtomique(ions)

        elif isinstance(obj, IonMonoAtomique):

            ions = self.ions[:]
            ions.append(obj)
            return IonPolyAtomique(ions)

        else:
            raise exception.Incompatible(self, obj)

    def __iadd__(self, 
            obj: Union[IonMonoAtomique, IonPolyAtomique]
        ) -> IonPolyAtomique:
        return self + obj

    def __sub__(self, 
            obj: Union[IonMonoAtomique, IonPolyAtomique]
        ) -> Union[None, IonMonoAtomique, IonPolyAtomique]:

        if isinstance(obj, IonPolyAtomique):

            ions = self.ions[:]
            for ion in obj.ions:
                ions.remove(ion)

            return (
                None if not ions
                else
                    ions[0] if len(ions) == 1
                    else
                        IonPolyAtomique(ions)
            )

        elif isinstance(obj, IonMonoAtomique):

            ions = self.ions[:]
            ions.remove(obj)

            return (
                None if not ions
                else
                    ions[0] if len(ions) == 1
                    else
                        IonPolyAtomique(ions)
            )

        else:
            raise exception.Incompatible(self, obj)

    def __isub__(self, 
            obj: Union[IonMonoAtomique, IonPolyAtomique]
        ) -> Union[None, IonMonoAtomique, IonPolyAtomique]:
        return self - obj

    def __repr__(self) -> str:
        return self.notation_symbole()

    def __eq__(self, obj: Any) -> bool:
        return repr(self) == repr(obj)

    def notation_symbole(self, *args, A:bool = True, Z:bool = True) -> str:
        """
        ### &doc_id ionPolyAtomique:notation_symbole
        """

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


objets.IonPolyAtomique = IonPolyAtomique


def MAJ_TYPE():

    variables = globals()

    for name_obj in objets.listes_noms:
        variables[name_obj] = getattr(objets, name_obj)