# Statement validation record

Item: `S56-M-1271-STATEMENT`  
Base revision: `be286e95464895d6966301556151584a57536a1b`

## Frozen target

`Stage1Instances.THM_M_1271.MountainPassTarget` formalizes the normalized classical
Ambrosetti-Rabinowitz mountain-pass claim selected by intake. `PalaisSmale` spells out bounded
functional values, derivative norm tending to zero, and a convergent subsequence. Paths are
continuous on `[0,1]`, start at zero, and end at `e`; their height is the supremum of functional
values and the mountain-pass level is the infimum of these heights.

The checked theorem `mountainPassTarget_iff_expanded` establishes definitional identity with a
direct expansion. This is statement identity evidence only, not a proof of the mountain-pass
theorem or an `H0` source-audit claim.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned Lake artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1271/Statement.lean` | 0 | target, direct expansion transport, and three mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1271/check_statement.py` | 0 | expression SHA-256 `686a7f777a77c3f91504e4c48cd3d0fab19ef802ce3df1751dc4288e62592d7b`; all three mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1271/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `984ec6...f70c`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |

The mutations remove compactness and part of the exact conclusion, restrict the arbitrary Banach
space to a finite-dimensional space, or weaken exact attainment to approximate criticality. None
has the canonical elaborated expression. No `sorry`, axiom, bodyless declaration, or placeholder is
present. Master acceptance remains separate.
