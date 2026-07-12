# Statement validation record

Item: `S56-M-0349-STATEMENT`  
Base revision: `cc46a50150dae27c90dca0938294d8da17db9109`

## Frozen target

`Stage1Instances.THM_M_0349.ConjugateFunctionTheoremTarget` states the strong periodic
conjugate-function theorem for complex `Lp` equivalence classes on `AddCircle 1` with Haar measure.
For each `1 < p < infinity`, it asserts a nonnegative real bound and an `Lp` conjugate whose Fourier
coefficients use multiplier `-i sign(n)`, with zero constant mode. The sole direct import is
`Mathlib.Analysis.Fourier.AddCircle`.

## Commands and results

Commands ran in this worker clone; Lean commands ran from `Formalizations/Lean` against the existing
pinned Lake environment. No update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0349/Statement.lean` | 0 | exact target and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0349/check_statement.py` | 0 | expression SHA-256 `5f80bebbbf59938add2cb517d6b6219f7a7a22ad8f09586d01e508db2e2ac908`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0349/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `c54899...cf62`, `651c8a...b1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 pass |
| `python3 scripts/stage1_target.py show THM-M-0349` | 0 | rank 842, planned, theorem incomplete |

The mutations remove the lower endpoint hypothesis, change the circle to the real line, move the
bound outside the exponent binder, and include the upper endpoint. They elaborate but have distinct
explicit expressions, so none silently substitutes for the target.

This is statement-only evidence pending master acceptance. The repository gloss has no pinpoint
source passage, so the selected classical conventions still require source audit. No proof, H0,
M0, R0, audit completion, theorem completion, or downstream-node credit is claimed.
