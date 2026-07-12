# Statement validation record

Item: `S56-M-1285-STATEMENT`  
Base revision: `0b1783610a62e88f5df9a118d9e9a0661c1fd0e9`.

## Frozen target

`Stage1Instances.THM_M_1285.SchwarzRearrangementTarget` fixes the intake's
least-broadened theorem-shaped reading on `EuclideanSpace Real (Fin n)`. The
input and witness are `ENNReal`-valued, dimension zero is excluded, and every
positive strict superlevel of the input must have finite volume. The witness is
measurable, radial, radially nonincreasing, and has the same volume at every
positive strict superlevel. `schwarzRearrangementTarget_iff_expandedTarget`
checks the expanded distribution-function encoding by definitional equality.
This node contains no construction or proof of the rearrangement.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned
environment. No dependency update, fetch, build, or `.lake` mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1285/Statement.lean` | 0 | root, predicates, definitional transport, and four mutations elaborated; explicit root printed |
| `python3 ../../Stage1_Instances/THM-M-1285/check_statement.py` | 0 | expression SHA-256 `ffce7418...d41ac`; all four structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1285/Statement.lean lean-toolchain lake-manifest.json` | 0 | `5b3e9ec5...c5e6`, `651c8acc...b1d2`, `321626c8...2d81` |
| import probe using `Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace` | 0 | the sole selected direct import elaborates the complete statement |
| import probe using `Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar` | 1 | expected missing `MeasureSpace (Euclidean n)`; this smaller-looking module is insufficient |

The mutations include dimension zero, remove the finite-superlevel premise,
change strict superlevels to non-strict ones, or remove radial monotonicity.
Each elaborates as a proposition but has a different explicit kernel rendering
from the root. This is statement-only evidence pending master acceptance;
source, anchor, proof, full validation, and release gates remain open.
