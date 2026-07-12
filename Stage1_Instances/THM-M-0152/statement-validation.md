# Statement validation record

Item: `S56-M-0152-STATEMENT`  
Base revision: `b66e26872f7b2eb2047782e029b32e32b0ead1d8`

## Frozen target

`Stage1Instances.THM_M_0152.TheoremaEgregiumTarget` encodes the pointwise local-isometry form of
Gauss's theorem for regular smooth parametrizations `Fin 2 -> Real` into Euclidean
`Fin 3 -> Real`. The local coordinate equivalence has a displayed smooth local inverse, and its
differential preserves the induced first fundamental form on a neighborhood. Gaussian curvature
is the classical `(L*N-M^2)/(E*G-F^2)` expression. The regularity premise makes the normal and
denominator nondegenerate at relevant points; orientation reversal leaves the expression fixed.

The direct imports are only `Mathlib.Analysis.Calculus.ContDiff.Defs` and
`Mathlib.LinearAlgebra.CrossProduct`. The checked iff to `ExpandedTarget` unfolds the regularity,
local inverse, and neighborhood metric hypotheses. This statement node does not prove the target.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean commands used the existing pinned Lake
environment; no dependency update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0152/Statement.lean` | 0 | definitions, canonical target, definitional transport, four mutations, and explicit target print elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0152/check_statement.py` | 0 | expression SHA-256 `898c24a88007838d739dc3ec63103e92ba06df082fa6d0b91557ba3863de2f02`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, release build |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0152/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `411162ea...058d`, `651c8acc...b1d2`, and `321626c8...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard valid with 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0152` | 0 | rank 651, planned, L0/rework-required, theorem incomplete |

The mutations remove regularity, weaken neighborhood metric preservation to a pointwise premise,
specialize away the general map and point, or alter the conclusion expression. They are statement
identity tests, not claims that each mutated proposition is mathematically false.

This is statement-only evidence pending master acceptance. Source acceptance, anchor audit, proof,
independent validation, and theorem completion remain open.
