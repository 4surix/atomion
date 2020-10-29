import unittest

from atomion import *
from atomion.raccourcis import *


class TestObjet(unittest.TestCase):

    def test_ionmonoatomique(self):
        self.assertEqual(
            Ion('O'),
            IonMonoAtomique('O')
        )

    def test_ionpolyatomique(self):
        self.assertEqual(
            Ion('O2'),
            IonPolyAtomique('O2')
        )

    def test_stable(self):
        for symbole in [
            'O3',
            'CH4',
            'C6H12O6',
            'O2',
            'CO2',
            'NH3',
            'C60',
            'C2H6',
            'CH4',
            'C2H4',
            'C3H4',
            'C2H2',
            'C6H6',
            'C2H5Br',
            'C2H5OH',
            'C6H6O',
            'C2H4O2',
            'C2H4O',
            'C3H6O',
            'H2O',
            'SO3',
            'C4H10O',
            'NH3',
            'C2H5CHO',
            'C2H3OH',
            'CH3CHO',
            'C2O2H4'
        ]:
            Molecule(symbole)


class TestException(unittest.TestCase):

    def test_molecule_instable(self):
        self.assertRaises(
            exception.Instable,
            lambda: Molecule('LiC')
        )

    def test_proton_instable(self):
        self.assertRaises(
            exception.Instable,
            lambda: QUp('R') + QUp('V') + QDown('V')
        )

    def test_neutron_instable(self):
        self.assertRaises(
            exception.Instable,
            lambda: QUp('R') + QDown('V') + QDown('V')
        )

    def test_atome_valeurIncorrecte(self):
        self.assertRaises(
            exception.ValeurIncorrecte,
            lambda: Atome('Carbone')
        )

    def test_atome_incompatible(self):
        self.assertRaises(
            exception.Incompatible,
            lambda: Atome('C') + 2
        )


class TestAddition(unittest.TestCase):

    def test_atome_proton(self):
        a = Atome('C') + Proton(3)
        b = Atome('F')
        self.assertTrue(a == b and a.proton == b.proton == 9)

    def test_atome_electron(self):
        a = Atome('Cl') + Electron(1)
        b = Ion('Cl')
        self.assertTrue(a == b and a.electron == b.electron == 18)

    def test_atome_atome(self):
        self.assertEqual(Atome('O') + Atome('O'), Molecule('O2'))

    def test_ion_ion(self):
        self.assertEqual(
            IonMonoAtomique('O') + IonMonoAtomique('O'),
            IonPolyAtomique('O2')
        )

    def test_molecule_molecule(self):
        self.assertEqual(
            Molecule('CO2') + Molecule('CH4'), 
            Molecule('C2O2H4')
        )

    def test_molecule_atome(self):
        self.assertEqual(
            Molecule('C2H4') + Atome('C'),
            Molecule('C3H4')
        )

    def test_proton_proton(self):
        self.assertEqual(
            Proton(2) + Proton(3),
            Proton(5)
        )

    def test_neutron_neutron(self):
        self.assertEqual(
            Neutron(2) + Neutron(3),
            Neutron(5)
        )

    def test_proton_neutron(self):
        self.assertEqual(
            Proton(2) + Neutron(3),
            Noyau(Proton(2), Neutron(3))
        )

    def test_neutron_proton(self):
        self.assertEqual(
            Neutron(2) + Proton(3),
            Noyau(Proton(3), Neutron(2))
        )

    def test_noyau_electron__atome(self):
        self.assertEqual(
            Noyau(Proton(3), Neutron(4)) + Electron(3),
            Atome(3)
        )

    def test_noyau_electron__ion(self):
        self.assertEqual(
            Noyau(Proton(3), Neutron(4)) + Electron(2),
            Ion(3)
        )

    def test_quark__proton(self):
        self.assertEqual(
            QUp(1) + QUp(2) + QDown(3),
            Proton()
        )

    def test_quark__neutron(self):
        self.assertEqual(
            QUp(1) + QDown(2) + QDown(3),
            Neutron()
        )


class TestSubstraction(unittest.TestCase):

    def test_atome_proton(self):
        a = Atome('C') - Proton(3)
        b = Atome('Li')
        self.assertTrue(a == b and a.proton == b.proton == 3)

    def test_atome_electron(self):
        a = Atome('Al') - Electron(3)
        b = Ion('Al')
        self.assertTrue(a == b and a.electron == b.electron == 10)

    def test_molecule_molecule(self):
        self.assertEqual(
            Molecule('C3H4') - Molecule('C2'), 
            Molecule('CH4')
        )

    def test_molecule_atome(self):
        self.assertEqual(Molecule('C2H4') - Atome('C'), Molecule('CH4'))


class TestMultiplication(unittest.TestCase):

    def test_atome_int(self):
        self.assertEqual(Atome('O') * 2, Molecule('O2'))


class TestEquation(unittest.TestCase):

    def test_equilibrage_atome(self):
        self.assertEqual(
            Equation('Cu2S + Cu2O -> Cu + SO2').equilibrer(),
            'Cu₂S + 2 Cu₂O -> 6 Cu + SO₂'
        )

    def test_equilibrage_charge(self):
        self.assertEqual(
            Equation('{Cu 2+} + Al -> Cu + {Al 3+}').equilibrer(),
            '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'
        )


class TestReactionQuantitesReactifs(unittest.TestCase):

    def setUp(self):
        self.reaction = Reaction(
            equation = Equation('Al + O2 -> Al2O3'),
            quantites_reactifs = {Atome('Al'): 1.6, Molecule('O2'): 1.3}
        )

    def test_initial(self):
        self.assertEqual(
            self.reaction.initial(),
            {
                Atome('Al'): 1.6,
                Molecule('O2'): 1.3,
                Molecule('Al2O3'): 0
            }
        )

    def test_intermediaire(self):
        self.assertEqual(
            self.reaction.intermediaire(0.1),
            {
                Atome('Al'): 1.2,
                Molecule('O2'): 1.0,
                Molecule('Al2O3'): 0.2
            }
        )

    def test_final(self):
        self.assertEqual(
            self.reaction.final(),
            {
                Atome('Al'): 0.0,
                Molecule('O2'): 0.1,
                Molecule('Al2O3'): 0.8
            }
        )

    def test_reactifs_limitants(self):
        self.assertEqual(
            self.reaction.reactifs_limitants(),
            [Atome('Al')]
        )


class TestReactionQuantitesProduits(unittest.TestCase):

    def setUp(self):
        self.reaction = Reaction(
            equation = Equation('Al + O2 -> Al2O3'),
            quantites_produits = {Molecule('Al2O3'): 0.7}
        )

    def test_initial(self):
        self.assertEqual(
            self.reaction.initial(),
            {
                Atome('Al'): 1.4,
                Molecule('O2'): 1.05,
                Molecule('Al2O3'): 0
            }
        )

    def test_intermediaire(self):
        self.assertEqual(
            self.reaction.intermediaire(0.1),
            {
                Atome('Al'): 1.0,
                Molecule('O2'): 0.75,
                Molecule('Al2O3'): 0.2
            }
        )

    def test_final(self):
        self.assertEqual(
            self.reaction.final(),
            {
                Atome('Al'): 0,
                Molecule('O2'): 0,
                Molecule('Al2O3'): 0.7
            }
        )

    def test_reactifs_limitants(self):
        self.assertEqual(
            self.reaction.reactifs_limitants(),
            [Atome('Al'), Molecule('O2')]
        )


if __name__ == '__main__':
    unittest.main()