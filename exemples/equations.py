from atomion import *


# Equilibre atomes
equation = Equation('Cu2S + Cu2O -> Cu + SO2')
equation.equilibrer() == 'Cu₂S + 2 Cu₂O -> 6 Cu + SO₂'

# Equilibre charges
equation = Equation('{Cu 2+} + Al -> Cu + {Al 3+}')
equation.equilibrer() == '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'

# Attributs
equation.notation == '3 Cu²⁺ + 2 Al -> 3 Cu + 2 Al³⁺'
equation.coefficients == [[3, 2], [3, 2]]
equation.spectatrices == []
equation.reactifs == [Ion('Cu'), Atome('Al')]
equation.produits == [Atome('Cu'), Atome('Al')]

# Demi-équation
equation = DemiEquation('Cl2', '{Cl -}')
equation.equilibrer()
equation == 'Cl₂ + 2 e⁻ -> 2 Cl⁻'