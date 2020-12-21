# -*- coding: utf-8 -*-
# Python 3.6.2
# ----------------------------------------------------------------------------

# La quasi-totalité des informations viennent de : 
#   https://github.com/Bowserinator/Periodic-Table-JSON
# J'ai rajoutée moi-même la partie fr.

###>>> CAPTURE FICHIER CALC

elements = [
    {
        "name": {
            "en": "Hydrogen",
            "fr": "Hydrogène"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 1,
        "period": 1,
        "symbol": "H",
        "shells": [
            1
        ],
        "atomic_mass": 1.008,
        "density": 0.08988
    },
    {
        "name": {
            "en": "Helium",
            "fr": "Hélium"
        },
        "category": {
            "en": "noble gas",
            "fr": "gaz noble"
        },
        "number": 2,
        "period": 1,
        "symbol": "He",
        "shells": [
            2
        ],
        "atomic_mass": 4.0026022,
        "density": 0.1786
    },
    {
        "name": {
            "en": "Lithium",
            "fr": "Lithium"
        },
        "category": {
            "en": "alkali metal",
            "fr": "métal alcalin"
        },
        "number": 3,
        "period": 2,
        "symbol": "Li",
        "shells": [
            2,
            1
        ],
        "atomic_mass": 6.94,
        "density": 0.534
    },
    {
        "name": {
            "en": "Beryllium",
            "fr": "Béryllium"
        },
        "category": {
            "en": "alkaline earth metal",
            "fr": "métal alcalino-terreux"
        },
        "number": 4,
        "period": 2,
        "symbol": "Be",
        "shells": [
            2,
            2
        ],
        "atomic_mass": 9.01218315,
        "density": 1.85
    },
    {
        "name": {
            "en": "Boron",
            "fr": "Bore"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 5,
        "period": 2,
        "symbol": "B",
        "shells": [
            2,
            3
        ],
        "atomic_mass": 10.81,
        "density": 2.08
    },
    {
        "name": {
            "en": "Carbon",
            "fr": "Carbone"
        },
        "category": {
            "en": "polyatomic nonmetal",
            "fr": "polyatomique non-metal"
        },
        "number": 6,
        "period": 2,
        "symbol": "C",
        "shells": [
            2,
            4
        ],
        "atomic_mass": 12.011,
        "density": 1.821
    },
    {
        "name": {
            "en": "Nitrogen",
            "fr": "Azote"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 7,
        "period": 2,
        "symbol": "N",
        "shells": [
            2,
            5
        ],
        "atomic_mass": 14.007,
        "density": 1.251
    },
    {
        "name": {
            "en": "Oxygen",
            "fr": "Oxygène"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 8,
        "period": 2,
        "symbol": "O",
        "shells": [
            2,
            6
        ],
        "atomic_mass": 15.999,
        "density": 1.429
    },
    {
        "name": {
            "en": "Fluorine",
            "fr": "Fluor"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 9,
        "period": 2,
        "symbol": "F",
        "shells": [
            2,
            7
        ],
        "atomic_mass": 18.9984031636,
        "density": 1.696
    },
    {
        "name": {
            "en": "Neon",
            "fr": "Néon"
        },
        "category": {
            "en": "noble gas",
            "fr": "gaz noble"
        },
        "number": 10,
        "period": 2,
        "symbol": "Ne",
        "shells": [
            2,
            8
        ],
        "atomic_mass": 20.17976,
        "density": 0.9002
    },
    {
        "name": {
            "en": "Sodium",
            "fr": "Sodium"
        },
        "category": {
            "en": "alkali metal",
            "fr": "métal alcalin"
        },
        "number": 11,
        "period": 3,
        "symbol": "Na",
        "shells": [
            2,
            8,
            1
        ],
        "atomic_mass": 22.989769282,
        "density": 0.968
    },
    {
        "name": {
            "en": "Magnesium",
            "fr": "Magnésium"
        },
        "category": {
            "en": "alkaline earth metal",
            "fr": "métal alcalino-terreux"
        },
        "number": 12,
        "period": 3,
        "symbol": "Mg",
        "shells": [
            2,
            8,
            2
        ],
        "atomic_mass": 24.305,
        "density": 1.738
    },
    {
        "name": {
            "en": "Aluminium",
            "fr": "Aluminium"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 13,
        "period": 3,
        "symbol": "Al",
        "shells": [
            2,
            8,
            3
        ],
        "atomic_mass": 26.98153857,
        "density": 2.7
    },
    {
        "name": {
            "en": "Silicon",
            "fr": "Silicium"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 14,
        "period": 3,
        "symbol": "Si",
        "shells": [
            2,
            8,
            4
        ],
        "atomic_mass": 28.085,
        "density": 2.329
    },
    {
        "name": {
            "en": "Phosphorus",
            "fr": "Phosphore"
        },
        "category": {
            "en": "polyatomic nonmetal",
            "fr": "polyatomique non-metal"
        },
        "number": 15,
        "period": 3,
        "symbol": "P",
        "shells": [
            2,
            8,
            5
        ],
        "atomic_mass": 30.9737619985,
        "density": 1.823
    },
    {
        "name": {
            "en": "Sulfur",
            "fr": "Soufre"
        },
        "category": {
            "en": "polyatomic nonmetal",
            "fr": "polyatomique non-metal"
        },
        "number": 16,
        "period": 3,
        "symbol": "S",
        "shells": [
            2,
            8,
            6
        ],
        "atomic_mass": 32.06,
        "density": 2.07
    },
    {
        "name": {
            "en": "Chlorine",
            "fr": "Chlore"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 17,
        "period": 3,
        "symbol": "Cl",
        "shells": [
            2,
            8,
            7
        ],
        "atomic_mass": 35.45,
        "density": 3.2
    },
    {
        "name": {
            "en": "Argon",
            "fr": "Argon"
        },
        "category": {
            "en": "noble gas",
            "fr": "gaz noble"
        },
        "number": 18,
        "period": 3,
        "symbol": "Ar",
        "shells": [
            2,
            8,
            8
        ],
        "atomic_mass": 39.9481,
        "density": 1.784
    },
    {
        "name": {
            "en": "Potassium",
            "fr": "Potassium"
        },
        "category": {
            "en": "alkali metal",
            "fr": "métal alcalin"
        },
        "number": 19,
        "period": 4,
        "symbol": "K",
        "shells": [
            2,
            8,
            8,
            1
        ],
        "atomic_mass": 39.09831,
        "density": 0.862
    },
    {
        "name": {
            "en": "Calcium",
            "fr": "Calcium"
        },
        "category": {
            "en": "alkaline earth metal",
            "fr": "métal alcalino-terreux"
        },
        "number": 20,
        "period": 4,
        "symbol": "Ca",
        "shells": [
            2,
            8,
            8,
            2
        ],
        "atomic_mass": 40.0784,
        "density": 1.55
    },
    {
        "name": {
            "en": "Scandium",
            "fr": "Scandium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 21,
        "period": 4,
        "symbol": "Sc",
        "shells": [
            2,
            8,
            9,
            2
        ],
        "atomic_mass": 44.9559085,
        "density": 2.985
    },
    {
        "name": {
            "en": "Titanium",
            "fr": "Titane"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 22,
        "period": 4,
        "symbol": "Ti",
        "shells": [
            2,
            8,
            10,
            2
        ],
        "atomic_mass": 47.8671,
        "density": 4.506
    },
    {
        "name": {
            "en": "Vanadium",
            "fr": "Vanadium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 23,
        "period": 4,
        "symbol": "V",
        "shells": [
            2,
            8,
            11,
            2
        ],
        "atomic_mass": 50.94151,
        "density": 6.0
    },
    {
        "name": {
            "en": "Chromium",
            "fr": "Chrome"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 24,
        "period": 4,
        "symbol": "Cr",
        "shells": [
            2,
            8,
            13,
            1
        ],
        "atomic_mass": 51.99616,
        "density": 7.19
    },
    {
        "name": {
            "en": "Manganese",
            "fr": "Manganèse"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 25,
        "period": 4,
        "symbol": "Mn",
        "shells": [
            2,
            8,
            13,
            2
        ],
        "atomic_mass": 54.9380443,
        "density": 7.21
    },
    {
        "name": {
            "en": "Iron",
            "fr": "Fer"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 26,
        "period": 4,
        "symbol": "Fe",
        "shells": [
            2,
            8,
            14,
            2
        ],
        "atomic_mass": 55.8452,
        "density": 7.874
    },
    {
        "name": {
            "en": "Cobalt",
            "fr": "Cobalt"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 27,
        "period": 4,
        "symbol": "Co",
        "shells": [
            2,
            8,
            15,
            2
        ],
        "atomic_mass": 58.9331944,
        "density": 8.9
    },
    {
        "name": {
            "en": "Nickel",
            "fr": "Nickel"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 28,
        "period": 4,
        "symbol": "Ni",
        "shells": [
            2,
            8,
            16,
            2
        ],
        "atomic_mass": 58.69344,
        "density": 8.908
    },
    {
        "name": {
            "en": "Copper",
            "fr": "Cuivre"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 29,
        "period": 4,
        "symbol": "Cu",
        "shells": [
            2,
            8,
            18,
            1
        ],
        "atomic_mass": 63.5463,
        "density": 8.96
    },
    {
        "name": {
            "en": "Zinc",
            "fr": "Zinc"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 30,
        "period": 4,
        "symbol": "Zn",
        "shells": [
            2,
            8,
            18,
            2
        ],
        "atomic_mass": 65.382,
        "density": 7.14
    },
    {
        "name": {
            "en": "Gallium",
            "fr": "Gallium"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 31,
        "period": 4,
        "symbol": "Ga",
        "shells": [
            2,
            8,
            18,
            3
        ],
        "atomic_mass": 69.7231,
        "density": 5.91
    },
    {
        "name": {
            "en": "Germanium",
            "fr": "Germanium"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 32,
        "period": 4,
        "symbol": "Ge",
        "shells": [
            2,
            8,
            18,
            4
        ],
        "atomic_mass": 72.6308,
        "density": 5.323
    },
    {
        "name": {
            "en": "Arsenic",
            "fr": "Arsenic"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 33,
        "period": 4,
        "symbol": "As",
        "shells": [
            2,
            8,
            18,
            5
        ],
        "atomic_mass": 74.9215956,
        "density": 5.727
    },
    {
        "name": {
            "en": "Selenium",
            "fr": "Sélénium"
        },
        "category": {
            "en": "polyatomic nonmetal",
            "fr": "polyatomique non-metal"
        },
        "number": 34,
        "period": 4,
        "symbol": "Se",
        "shells": [
            2,
            8,
            18,
            6
        ],
        "atomic_mass": 78.9718,
        "density": 4.81
    },
    {
        "name": {
            "en": "Bromine",
            "fr": "Brome"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 35,
        "period": 4,
        "symbol": "Br",
        "shells": [
            2,
            8,
            18,
            7
        ],
        "atomic_mass": 79.904,
        "density": 3.1028
    },
    {
        "name": {
            "en": "Krypton",
            "fr": "Krypton"
        },
        "category": {
            "en": "noble gas",
            "fr": "gaz noble"
        },
        "number": 36,
        "period": 4,
        "symbol": "Kr",
        "shells": [
            2,
            8,
            18,
            8
        ],
        "atomic_mass": 83.7982,
        "density": 3.749
    },
    {
        "name": {
            "en": "Rubidium",
            "fr": "Rubidium"
        },
        "category": {
            "en": "alkali metal",
            "fr": "métal alcalin"
        },
        "number": 37,
        "period": 5,
        "symbol": "Rb",
        "shells": [
            2,
            8,
            18,
            8,
            1
        ],
        "atomic_mass": 85.46783,
        "density": 1.532
    },
    {
        "name": {
            "en": "Strontium",
            "fr": "Strontium"
        },
        "category": {
            "en": "alkaline earth metal",
            "fr": "métal alcalino-terreux"
        },
        "number": 38,
        "period": 5,
        "symbol": "Sr",
        "shells": [
            2,
            8,
            18,
            8,
            2
        ],
        "atomic_mass": 87.621,
        "density": 2.64
    },
    {
        "name": {
            "en": "Yttrium",
            "fr": "Yttrium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 39,
        "period": 5,
        "symbol": "Y",
        "shells": [
            2,
            8,
            18,
            9,
            2
        ],
        "atomic_mass": 88.905842,
        "density": 4.472
    },
    {
        "name": {
            "en": "Zirconium",
            "fr": "Zirconium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 40,
        "period": 5,
        "symbol": "Zr",
        "shells": [
            2,
            8,
            18,
            10,
            2
        ],
        "atomic_mass": 91.2242,
        "density": 6.52
    },
    {
        "name": {
            "en": "Niobium",
            "fr": "Niobium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 41,
        "period": 5,
        "symbol": "Nb",
        "shells": [
            2,
            8,
            18,
            12,
            1
        ],
        "atomic_mass": 92.906372,
        "density": 8.57
    },
    {
        "name": {
            "en": "Molybdenum",
            "fr": "Molybdène"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 42,
        "period": 5,
        "symbol": "Mo",
        "shells": [
            2,
            8,
            18,
            13,
            1
        ],
        "atomic_mass": 95.951,
        "density": 10.28
    },
    {
        "name": {
            "en": "Technetium",
            "fr": "Technétium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 43,
        "period": 5,
        "symbol": "Tc",
        "shells": [
            2,
            8,
            18,
            13,
            2
        ],
        "atomic_mass": 98,
        "density": 11
    },
    {
        "name": {
            "en": "Ruthenium",
            "fr": "Ruthénium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 44,
        "period": 5,
        "symbol": "Ru",
        "shells": [
            2,
            8,
            18,
            15,
            1
        ],
        "atomic_mass": 101.072,
        "density": 12.45
    },
    {
        "name": {
            "en": "Rhodium",
            "fr": "Rhodium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 45,
        "period": 5,
        "symbol": "Rh",
        "shells": [
            2,
            8,
            18,
            16,
            1
        ],
        "atomic_mass": 102.905502,
        "density": 12.41
    },
    {
        "name": {
            "en": "Palladium",
            "fr": "Palladium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 46,
        "period": 5,
        "symbol": "Pd",
        "shells": [
            2,
            8,
            18,
            18
        ],
        "atomic_mass": 106.421,
        "density": 12.023
    },
    {
        "name": {
            "en": "Silver",
            "fr": "Argent"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 47,
        "period": 5,
        "symbol": "Ag",
        "shells": [
            2,
            8,
            18,
            18,
            1
        ],
        "atomic_mass": 107.86822,
        "density": 10.49
    },
    {
        "name": {
            "en": "Cadmium",
            "fr": "Cadmium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 48,
        "period": 5,
        "symbol": "Cd",
        "shells": [
            2,
            8,
            18,
            18,
            2
        ],
        "atomic_mass": 112.4144,
        "density": 8.65
    },
    {
        "name": {
            "en": "Indium",
            "fr": "Indium"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 49,
        "period": 5,
        "symbol": "In",
        "shells": [
            2,
            8,
            18,
            18,
            3
        ],
        "atomic_mass": 114.8181,
        "density": 7.31
    },
    {
        "name": {
            "en": "Tin",
            "fr": "Etin"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 50,
        "period": 5,
        "symbol": "Sn",
        "shells": [
            2,
            8,
            18,
            18,
            4
        ],
        "atomic_mass": 118.7107,
        "density": 7.365
    },
    {
        "name": {
            "en": "Antimony",
            "fr": "Antimoine"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 51,
        "period": 5,
        "symbol": "Sb",
        "shells": [
            2,
            8,
            18,
            18,
            5
        ],
        "atomic_mass": 121.7601,
        "density": 6.697
    },
    {
        "name": {
            "en": "Tellurium",
            "fr": "Tellure"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 52,
        "period": 5,
        "symbol": "Te",
        "shells": [
            2,
            8,
            18,
            18,
            6
        ],
        "atomic_mass": 127.603,
        "density": 6.24
    },
    {
        "name": {
            "en": "Iodine",
            "fr": "Iode"
        },
        "category": {
            "en": "diatomic nonmetal",
            "fr": "diatomique non-metal"
        },
        "number": 53,
        "period": 5,
        "symbol": "I",
        "shells": [
            2,
            8,
            18,
            18,
            7
        ],
        "atomic_mass": 126.904473,
        "density": 4.933
    },
    {
        "name": {
            "en": "Xenon",
            "fr": "Xénon"
        },
        "category": {
            "en": "noble gas",
            "fr": "gaz noble"
        },
        "number": 54,
        "period": 5,
        "symbol": "Xe",
        "shells": [
            2,
            8,
            18,
            18,
            8
        ],
        "atomic_mass": 131.2936,
        "density": 5.894
    },
    {
        "name": {
            "en": "Cesium",
            "fr": "Césium"
        },
        "category": {
            "en": "alkali metal",
            "fr": "métal alcalin"
        },
        "number": 55,
        "period": 6,
        "symbol": "Cs",
        "shells": [
            2,
            8,
            18,
            18,
            8,
            1
        ],
        "atomic_mass": 132.905451966,
        "density": 1.93
    },
    {
        "name": {
            "en": "Barium",
            "fr": "Baryum"
        },
        "category": {
            "en": "alkaline earth metal",
            "fr": "métal alcalino-terreux"
        },
        "number": 56,
        "period": 6,
        "symbol": "Ba",
        "shells": [
            2,
            8,
            18,
            18,
            8,
            2
        ],
        "atomic_mass": 137.3277,
        "density": 3.51
    },
    {
        "name": {
            "en": "Lanthanum",
            "fr": "Lathane"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 57,
        "period": 6,
        "symbol": "La",
        "shells": [
            2,
            8,
            18,
            18,
            9,
            2
        ],
        "atomic_mass": 138.905477,
        "density": 6.162
    },
    {
        "name": {
            "en": "Cerium",
            "fr": "Cérium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 58,
        "period": 6,
        "symbol": "Ce",
        "shells": [
            2,
            8,
            18,
            19,
            9,
            2
        ],
        "atomic_mass": 140.1161,
        "density": 6.77
    },
    {
        "name": {
            "en": "Praseodymium",
            "fr": "Praséodyme"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 59,
        "period": 6,
        "symbol": "Pr",
        "shells": [
            2,
            8,
            18,
            21,
            8,
            2
        ],
        "atomic_mass": 140.907662,
        "density": 6.77
    },
    {
        "name": {
            "en": "Neodymium",
            "fr": "Néodyme"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 60,
        "period": 6,
        "symbol": "Nd",
        "shells": [
            2,
            8,
            18,
            22,
            8,
            2
        ],
        "atomic_mass": 144.2423,
        "density": 7.01
    },
    {
        "name": {
            "en": "Promethium",
            "fr": "Prométhium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 61,
        "period": 6,
        "symbol": "Pm",
        "shells": [
            2,
            8,
            18,
            23,
            8,
            2
        ],
        "atomic_mass": 145,
        "density": 7.26
    },
    {
        "name": {
            "en": "Samarium",
            "fr": "Samarium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 62,
        "period": 6,
        "symbol": "Sm",
        "shells": [
            2,
            8,
            18,
            24,
            8,
            2
        ],
        "atomic_mass": 150.362,
        "density": 7.52
    },
    {
        "name": {
            "en": "Europium",
            "fr": "Europium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 63,
        "period": 6,
        "symbol": "Eu",
        "shells": [
            2,
            8,
            18,
            25,
            8,
            2
        ],
        "atomic_mass": 151.9641,
        "density": 5.264
    },
    {
        "name": {
            "en": "Gadolinium",
            "fr": "Gadolinium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 64,
        "period": 6,
        "symbol": "Gd",
        "shells": [
            2,
            8,
            18,
            25,
            9,
            2
        ],
        "atomic_mass": 157.253,
        "density": 7.9
    },
    {
        "name": {
            "en": "Terbium",
            "fr": "Terbium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 65,
        "period": 6,
        "symbol": "Tb",
        "shells": [
            2,
            8,
            18,
            27,
            8,
            2
        ],
        "atomic_mass": 158.925352,
        "density": 8.23
    },
    {
        "name": {
            "en": "Dysprosium",
            "fr": "Dysprosium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 66,
        "period": 6,
        "symbol": "Dy",
        "shells": [
            2,
            8,
            18,
            28,
            8,
            2
        ],
        "atomic_mass": 162.5001,
        "density": 8.54
    },
    {
        "name": {
            "en": "Holmium",
            "fr": "Holmium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 67,
        "period": 6,
        "symbol": "Ho",
        "shells": [
            2,
            8,
            18,
            29,
            8,
            2
        ],
        "atomic_mass": 164.930332,
        "density": 8.79
    },
    {
        "name": {
            "en": "Erbium",
            "fr": "Erbium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 68,
        "period": 6,
        "symbol": "Er",
        "shells": [
            2,
            8,
            18,
            30,
            8,
            2
        ],
        "atomic_mass": 167.2593,
        "density": 9.066
    },
    {
        "name": {
            "en": "Thulium",
            "fr": "Thulium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 69,
        "period": 6,
        "symbol": "Tm",
        "shells": [
            2,
            8,
            18,
            31,
            8,
            2
        ],
        "atomic_mass": 168.934222,
        "density": 9.32
    },
    {
        "name": {
            "en": "Ytterbium",
            "fr": "Ytterbium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 70,
        "period": 6,
        "symbol": "Yb",
        "shells": [
            2,
            8,
            18,
            32,
            8,
            2
        ],
        "atomic_mass": 173.0451,
        "density": 6.9
    },
    {
        "name": {
            "en": "Lutetium",
            "fr": "Lutetium"
        },
        "category": {
            "en": "lanthanide",
            "fr": "lanthanide"
        },
        "number": 71,
        "period": 6,
        "symbol": "Lu",
        "shells": [
            2,
            8,
            18,
            32,
            9,
            2
        ],
        "atomic_mass": 174.96681,
        "density": 9.841
    },
    {
        "name": {
            "en": "Hafnium",
            "fr": "Hafnium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 72,
        "period": 6,
        "symbol": "Hf",
        "shells": [
            2,
            8,
            18,
            32,
            10,
            2
        ],
        "atomic_mass": 178.492,
        "density": 13.31
    },
    {
        "name": {
            "en": "Tantalum",
            "fr": "Tantale"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 73,
        "period": 6,
        "symbol": "Ta",
        "shells": [
            2,
            8,
            18,
            32,
            11,
            2
        ],
        "atomic_mass": 180.947882,
        "density": 16.69
    },
    {
        "name": {
            "en": "Tungsten",
            "fr": "Tungstène"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 74,
        "period": 6,
        "symbol": "W",
        "shells": [
            2,
            8,
            18,
            32,
            12,
            2
        ],
        "atomic_mass": 183.841,
        "density": 19.25
    },
    {
        "name": {
            "en": "Rhenium",
            "fr": "Rhénium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 75,
        "period": 6,
        "symbol": "Re",
        "shells": [
            2,
            8,
            18,
            32,
            13,
            2
        ],
        "atomic_mass": 186.2071,
        "density": 21.02
    },
    {
        "name": {
            "en": "Osmium",
            "fr": "Osmium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 76,
        "period": 6,
        "symbol": "Os",
        "shells": [
            2,
            8,
            18,
            32,
            14,
            2
        ],
        "atomic_mass": 190.233,
        "density": 22.59
    },
    {
        "name": {
            "en": "Iridium",
            "fr": "Iridium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 77,
        "period": 6,
        "symbol": "Ir",
        "shells": [
            2,
            8,
            18,
            32,
            15,
            2
        ],
        "atomic_mass": 192.2173,
        "density": 22.56
    },
    {
        "name": {
            "en": "Platinum",
            "fr": "Platine"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 78,
        "period": 6,
        "symbol": "Pt",
        "shells": [
            2,
            8,
            18,
            32,
            17,
            1
        ],
        "atomic_mass": 195.0849,
        "density": 21.45
    },
    {
        "name": {
            "en": "Gold",
            "fr": "Or"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 79,
        "period": 6,
        "symbol": "Au",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            1
        ],
        "atomic_mass": 196.9665695,
        "density": 19.3
    },
    {
        "name": {
            "en": "Mercury",
            "fr": "Mercure"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 80,
        "period": 6,
        "symbol": "Hg",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            2
        ],
        "atomic_mass": 200.5923,
        "density": 13.534
    },
    {
        "name": {
            "en": "Thallium",
            "fr": "Thallium"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 81,
        "period": 6,
        "symbol": "Tl",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            3
        ],
        "atomic_mass": 204.38,
        "density": 11.85
    },
    {
        "name": {
            "en": "Lead",
            "fr": "Plomb"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 82,
        "period": 6,
        "symbol": "Pb",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            4
        ],
        "atomic_mass": 207.21,
        "density": 11.34
    },
    {
        "name": {
            "en": "Bismuth",
            "fr": "Bismuth"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 83,
        "period": 6,
        "symbol": "Bi",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            5
        ],
        "atomic_mass": 208.980401,
        "density": 9.78
    },
    {
        "name": {
            "en": "Polonium",
            "fr": "Polonium"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 84,
        "period": 6,
        "symbol": "Po",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            6
        ],
        "atomic_mass": 209,
        "density": 9.196
    },
    {
        "name": {
            "en": "Astatine",
            "fr": "Astane"
        },
        "category": {
            "en": "metalloid",
            "fr": "métalloïde"
        },
        "number": 85,
        "period": 6,
        "symbol": "At",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            7
        ],
        "atomic_mass": 210,
        "density": 6.35
    },
    {
        "name": {
            "en": "Radon",
            "fr": "Radon"
        },
        "category": {
            "en": "noble gas",
            "fr": "gaz noble"
        },
        "number": 86,
        "period": 6,
        "symbol": "Rn",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            8
        ],
        "atomic_mass": 222,
        "density": 9.73
    },
    {
        "name": {
            "en": "Francium",
            "fr": "Francium"
        },
        "category": {
            "en": "alkali metal",
            "fr": "métal alcalin"
        },
        "number": 87,
        "period": 7,
        "symbol": "Fr",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            8,
            1
        ],
        "atomic_mass": 223,
        "density": 1.87
    },
    {
        "name": {
            "en": "Radium",
            "fr": "Radium"
        },
        "category": {
            "en": "alkaline earth metal",
            "fr": "métal alcalino-terreux"
        },
        "number": 88,
        "period": 7,
        "symbol": "Ra",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            8,
            2
        ],
        "atomic_mass": 226,
        "density": 5.5
    },
    {
        "name": {
            "en": "Actinium",
            "fr": "Actinium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 89,
        "period": 7,
        "symbol": "Ac",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            9,
            2
        ],
        "atomic_mass": 227,
        "density": 10
    },
    {
        "name": {
            "en": "Thorium",
            "fr": "Thorium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 90,
        "period": 7,
        "symbol": "Th",
        "shells": [
            2,
            8,
            18,
            32,
            18,
            10,
            2
        ],
        "atomic_mass": 232.03774,
        "density": 11.724
    },
    {
        "name": {
            "en": "Protactinium",
            "fr": "Protactinium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 91,
        "period": 7,
        "symbol": "Pa",
        "shells": [
            2,
            8,
            18,
            32,
            20,
            9,
            2
        ],
        "atomic_mass": 231.035882,
        "density": 15.37
    },
    {
        "name": {
            "en": "Uranium",
            "fr": "Uranium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 92,
        "period": 7,
        "symbol": "U",
        "shells": [
            2,
            8,
            18,
            32,
            21,
            9,
            2
        ],
        "atomic_mass": 238.028913,
        "density": 19.1
    },
    {
        "name": {
            "en": "Neptunium",
            "fr": "Neptunium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 93,
        "period": 7,
        "symbol": "Np",
        "shells": [
            2,
            8,
            18,
            32,
            22,
            9,
            2
        ],
        "atomic_mass": 237,
        "density": 20.45
    },
    {
        "name": {
            "en": "Plutonium",
            "fr": "Plutonium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 94,
        "period": 7,
        "symbol": "Pu",
        "shells": [
            2,
            8,
            18,
            32,
            24,
            8,
            2
        ],
        "atomic_mass": 244,
        "density": 19.816
    },
    {
        "name": {
            "en": "Americium",
            "fr": "Américium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 95,
        "period": 7,
        "symbol": "Am",
        "shells": [
            2,
            8,
            18,
            32,
            25,
            8,
            2
        ],
        "atomic_mass": 243,
        "density": 12
    },
    {
        "name": {
            "en": "Curium",
            "fr": "Curium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 96,
        "period": 7,
        "symbol": "Cm",
        "shells": [
            2,
            8,
            18,
            32,
            25,
            9,
            2
        ],
        "atomic_mass": 247,
        "density": 13.51
    },
    {
        "name": {
            "en": "Berkelium",
            "fr": "Berkélium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 97,
        "period": 7,
        "symbol": "Bk",
        "shells": [
            2,
            8,
            18,
            32,
            27,
            8,
            2
        ],
        "atomic_mass": 247,
        "density": 14.78
    },
    {
        "name": {
            "en": "Californium",
            "fr": "Californium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 98,
        "period": 7,
        "symbol": "Cf",
        "shells": [
            2,
            8,
            18,
            32,
            28,
            8,
            2
        ],
        "atomic_mass": 251,
        "density": 15.1
    },
    {
        "name": {
            "en": "Einsteinium",
            "fr": "Einsteinium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 99,
        "period": 7,
        "symbol": "Es",
        "shells": [
            2,
            8,
            18,
            32,
            29,
            8,
            2
        ],
        "atomic_mass": 252,
        "density": 8.84
    },
    {
        "name": {
            "en": "Fermium",
            "fr": "Fermium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 100,
        "period": 7,
        "symbol": "Fm",
        "shells": [
            2,
            8,
            18,
            32,
            30,
            8,
            2
        ],
        "atomic_mass": 257,
        "density": None
    },
    {
        "name": {
            "en": "Mendelevium",
            "fr": "Mendélévium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 101,
        "period": 7,
        "symbol": "Md",
        "shells": [
            2,
            8,
            18,
            32,
            31,
            8,
            2
        ],
        "atomic_mass": 258,
        "density": None
    },
    {
        "name": {
            "en": "Nobelium",
            "fr": "Nobélium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 102,
        "period": 7,
        "symbol": "No",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            8,
            2
        ],
        "atomic_mass": 259,
        "density": None
    },
    {
        "name": {
            "en": "Lawrencium",
            "fr": "Lawrencium"
        },
        "category": {
            "en": "actinide",
            "fr": "actinide"
        },
        "number": 103,
        "period": 7,
        "symbol": "Lr",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            8,
            3
        ],
        "atomic_mass": 266,
        "density": None
    },
    {
        "name": {
            "en": "Rutherfordium",
            "fr": "Rutherfordium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 104,
        "period": 7,
        "symbol": "Rf",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            10,
            2
        ],
        "atomic_mass": 267,
        "density": 23.2
    },
    {
        "name": {
            "en": "Dubnium",
            "fr": "Dubnium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 105,
        "period": 7,
        "symbol": "Db",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            11,
            2
        ],
        "atomic_mass": 268,
        "density": 29.3
    },
    {
        "name": {
            "en": "Seaborgium",
            "fr": "Seaborgium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 106,
        "period": 7,
        "symbol": "Sg",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            12,
            2
        ],
        "atomic_mass": 269,
        "density": 35.0
    },
    {
        "name": {
            "en": "Bohrium",
            "fr": "Bohrium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 107,
        "period": 7,
        "symbol": "Bh",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            13,
            2
        ],
        "atomic_mass": 270,
        "density": 37.1
    },
    {
        "name": {
            "en": "Hassium",
            "fr": "Hassium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 108,
        "period": 7,
        "symbol": "Hs",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            14,
            2
        ],
        "atomic_mass": 269,
        "density": 40.7
    },
    {
        "name": {
            "en": "Meitnerium",
            "fr": "Meitnérium"
        },
        "category": {
            "en": "unknown, probably transition metal",
            "fr": "inconnu"
        },
        "number": 109,
        "period": 7,
        "symbol": "Mt",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            15,
            2
        ],
        "atomic_mass": 278,
        "density": 37.4
    },
    {
        "name": {
            "en": "Darmstadtium",
            "fr": "Darmstadtium"
        },
        "category": {
            "en": "unknown, probably transition metal",
            "fr": "inconnu"
        },
        "number": 110,
        "period": 7,
        "symbol": "Ds",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            16,
            2
        ],
        "atomic_mass": 281,
        "density": 34.8
    },
    {
        "name": {
            "en": "Roentgenium",
            "fr": "Rœntgénium"
        },
        "category": {
            "en": "unknown, probably transition metal",
            "fr": "inconnu"
        },
        "number": 111,
        "period": 7,
        "symbol": "Rg",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            17,
            2
        ],
        "atomic_mass": 282,
        "density": 28.7
    },
    {
        "name": {
            "en": "Copernicium",
            "fr": "Copernicium"
        },
        "category": {
            "en": "transition metal",
            "fr": "métal de transition"
        },
        "number": 112,
        "period": 7,
        "symbol": "Cn",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            2
        ],
        "atomic_mass": 285,
        "density": 23.7
    },
    {
        "name": {
            "en": "Nihonium",
            "fr": "Nihonium"
        },
        "category": {
            "en": "unknown, probably transition metal",
            "fr": "inconnu"
        },
        "number": 113,
        "period": 7,
        "symbol": "Nh",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            3
        ],
        "atomic_mass": 286,
        "density": 16
    },
    {
        "name": {
            "en": "Flerovium",
            "fr": "Flérovium"
        },
        "category": {
            "en": "post-transition metal",
            "fr": "métal post-transitionnel"
        },
        "number": 114,
        "period": 7,
        "symbol": "Fl",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            4
        ],
        "atomic_mass": 289,
        "density": 14
    },
    {
        "name": {
            "en": "Moscovium",
            "fr": "Moscovium"
        },
        "category": {
            "en": "unknown, probably post-transition metal",
            "fr": "inconnu"
        },
        "number": 115,
        "period": 7,
        "symbol": "Mc",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            5
        ],
        "atomic_mass": 289,
        "density": 13.5
    },
    {
        "name": {
            "en": "Livermorium",
            "fr": "Livermorium"
        },
        "category": {
            "en": "unknown, probably post-transition metal",
            "fr": "inconnu"
        },
        "number": 116,
        "period": 7,
        "symbol": "Lv",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            6
        ],
        "atomic_mass": 293,
        "density": 12.9
    },
    {
        "name": {
            "en": "Tennessine",
            "fr": "Tennesse"
        },
        "category": {
            "en": "unknown, probably metalloid",
            "fr": "inconnu"
        },
        "number": 117,
        "period": 7,
        "symbol": "Ts",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            7
        ],
        "atomic_mass": 294,
        "density": 7.17
    },
    {
        "name": {
            "en": "Oganesson",
            "fr": "Oganesson"
        },
        "category": {
            "en": "unknown, predicted to be noble gas",
            "fr": "inconnu"
        },
        "number": 118,
        "period": 7,
        "symbol": "Og",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            8
        ],
        "atomic_mass": 294,
        "density": 4.95
    },
    {
        "name": {
            "en": "Ununennium",
            "fr": "Ununennium"
        },
        "category": {
            "en": "unknown, but predicted to be an alkali metal",
            "fr": "inconnu"
        },
        "number": 119,
        "period": 8,
        "symbol": "Uue",
        "shells": [
            2,
            8,
            18,
            32,
            32,
            18,
            8,
            1
        ],
        "atomic_mass": 315,
        "density": 3
    }
]

###<<< CAPTURE FICHIER CALC