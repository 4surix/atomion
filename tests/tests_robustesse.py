# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

import unittest


from atomion import *
from atomion import couples, raccourcis
from atomion.utile import params
from atomion.utile.utile import u, mol, masse_electron, masse_proton


class TestCouples(unittest.TestCase):

    def test_get_produit_oxydoreduction(self):
        # Type de retour unifié : liste de tuples (role, partenaire).
        produits = couples.get_produit(Atome('Fe'), 'oxydoreduction')
        self.assertIsInstance(produits, list)
        self.assertEqual(
            produits,
            [('reducteur', Ion('{Fe 2+}'))]
        )

    def test_get_produit_acide_base(self):
        self.assertEqual(
            couples.get_produit(Ion('{H3O +}'), 'acide/base'),
            [('acide', Molecule('H2O'))]
        )

    def test_get_produit_inconnu(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: couples.get_produit(Atome('C'), 'oxydoreduction')
        )


class TestParams(unittest.TestCase):

    def tearDown(self):
        params.config(
            langue = 'fr',
            strict = True,
            nom = True,
            categorie = True,
            proton = True,
            neutron = True,
            electron = True,
            masse = True,
            masse_relative = True,
            couches = True,
            configuration = True
        )

    def test_parametre_inconnu(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: params.config(inexistant = True)
        )

    def test_parametre_modifiable(self):
        params.config(categorie = False)
        self.assertFalse(params.categorie)

    def test_parametre_booleen_falsy(self):
        # Une valeur `False`/`None` doit pouvoir être appliquée.
        params.config(couches = False)
        self.assertFalse(params.couches)


class TestConstantes(unittest.TestCase):

    def test_mol_coherent(self):
        self.assertEqual(raccourcis.mol, mol)

    def test_u_coherent(self):
        self.assertEqual(raccourcis.u, u)

    def test_alias_masses(self):
        self.assertEqual(raccourcis.Me, masse_electron)
        self.assertEqual(raccourcis.Mp, masse_proton)


class TestIon(unittest.TestCase):

    def test_polyatomique(self):
        self.assertIsInstance(Ion('CO3'), IonPolyAtomique)

    def test_monoatomique(self):
        self.assertIsInstance(Ion('Cl'), IonMonoAtomique)

    def test_inconnu(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Ion('Zz')
        )


class TestLiaison(unittest.TestCase):

    def test_gaz_noble(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Liaison(Atome('He'), Atome('H'))
        )


class TestMoleculeOrganique(unittest.TestCase):

    def test_nomenclature_invalide(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: MoleculeOrganique('4-méthylpentan-1-anoïque')
        )

    def test_famille_indeterminee(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: MoleculeOrganique('pentane')
        )


if __name__ == '__main__':
    unittest.main()
