from atomion import *


oxydoR = OxydoReduction(
    Ion('{Cr2O7 2-}'),
    Atome('Fe')
)
oxydoR.don == 'Fe -> Fe²⁺ + 2 e⁻'
oxydoR.gain == 'Cr₂O₇²⁻ + 14 H⁺ + 6 e⁻ -> 2 Cr³⁺ + 7 H₂O'
oxydoR.equation == '3 Fe + Cr₂O₇²⁻ + 14 H⁺ -> 3 Fe²⁺ + 2 Cr³⁺ + 7 H₂O'