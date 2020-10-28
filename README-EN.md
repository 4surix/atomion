- [Atomion](atomion)
- [Overview](#overview)
- [Soon](#soon)
- [Install](#install)
- [Documentation](#documentation)

# Atomion

[![Build Status](https://travis-ci.com/4surix/atomion.svg?branch=master)](https://travis-ci.com/4surix/atomion)
[![PyPI](https://img.shields.io/pypi/v/atomion)](https://pypi.org/project/atomion/)
[![GitHub issues](https://img.shields.io/github/issues/4surix/atomion)](https://github.com/4surix/atomion/issues)

Module used for atoms, ions _(monoatomics/polyatomics)_ and molecules easy handling

You'll find a [examples.py](https//github.com/4surix/atomion/blob/master/exemples.py) file with various features.

This module is compatible with `Micro Python 1.9.4`, therefore, also with calculators !

# Overview

```python
from atomion import *

oxygen = Atome('O') # With symbol
hydrogen = Atome(1) # With proton amount

water = hydrogen * 2 + oxygen
# Or
water = Molecule('H2O')

chloride = Ion('Cl')
# Or
chloride = IonMonoAtomique('Cl')

carbonate = Ion('CO3')
# Or
carbonate = IonPolyAtomique('CO3')

equation = Equation('Cu + O2 -> CuO')
equation.equilibrer()
equation == '2 Cu + O₂ -> 2 CuO'

reaction = Reaction(
    equation = equation,
    quantites_reactifs = {
        Atome('Cu'): 1.6,
        Molecule('O2'): 1.3
    }
)
reaction.final() == {
    Atome('Cu'): 0.0,
    Molecule('O2'): 0.5,
    Molecule('CuO'): 1.6
}

from atomion.raccourcis import *

water = H * 2 + O
# Or
water = H2O

print(water)
```

To see the other functionnalities, look at [examples.py](https://github.com/4surix/atomion/blob/master/exemples.py) file.

# Soon

### v1.3.0

- Quarks adding (Up & down)
- Nucleus object adding.
  - Will contain "proton" & "neutron" objects
  - Will be able to be added with Electron objects to create atoms or ions.

### v1.4.0

- Nuclear fusion adding
- Nuclear fission adding

# Install

### Computer

- Open a Command Prompt.
  <details>
    <summary>How to ?</summary>

  Appuyez sur la touche `Windows` + la touche `R`, et écrivez `cmd` dans la fenêtre qui s'est ouverte.
  Push `Windows` and `R` keys and write `cmd` in the window.
  </details>

- Make sure to have Python 3.6 or greater installed.
  <details>
    <summary>How to know ?</summary>

  Write `python --version` in command prompt. If python is installed, it will show the version (it has to be greater or egal to 3.6)

  If it doesn't show the version, you have to [install Python](https://python.org/downloads) in a version greater or egal to 3.6 to avoid compatibility issues.
  </details>

- Make sure to have `pip` install
  <details>
    <summary>How to check ?</summary>

  Write `pip --version` in command prompt. If pip is installed, it will show its version that has to be greater than 10.0.0.

  If it is lower than 10.0.0, write `python -m pip install --upgrade pip` to update.
  </details>

- Write the following command :
  ```sh
  pip install atomion
  ```
- To update it, just add `--upgrade` to update the module :

```sh
pip install atomion --upgrade
```

- Then, create a new file, import the module and enjoy !

  ```python
  from atomion import *

  print(Atome('C') + Molecule('O2'))
  ```

### Calculator

_**Warning**, for calculators that cannot have folders, it is not possible to use this module, but a single file version is WIP to permise you to use it_

- Notice the green button with "Code" written on it on this page et push it.
- Click on "Download ZIP".
- When download is finished, open the .zip file et move the inside folder to another place (in an accessible place).
- Open the folder that you moved and put the `atomion` folder in your calculator _(that you have plugged to your computer)_.
- You can also add `exemples.py` file in your calculator to check that all is functionning properly.
- Now, unplug you calculator, execute `exemples.py` if you added it and, if all works, enjoy !

# Docs

Not yet finished but available :

- 🇫🇷 [En français](https://4surix.github.io/atomion-doc/fr/annotated.html)
- 🇪🇸 [En español](https://4surix.github.io/atomion-doc/es/annotated.html)

_Made with [DoxyTH](https://github.com/BioTheWolff/DoxyTH)._
