# Statement validation

Item: `S56-M-0162-STATEMENT`  
Base revision: `43ca1e9c218df4cc2d3a1d9ee187c910c850bddd`

## Frozen target

`Stage1Instances.THM_M_0162.FrenetSerretTarget` freezes the intake claim on an open real
parameter set. It uses coordinate vectors `Fin 3 -> Real`, the standard dot-product Euclidean
norm, mathlib's standard oriented cross product, explicit derivative witnesses, positive
curvature, and the torsion convention `tau = -(B' dot N)`. The derivative equations occur only
in the conclusion. Direct imports are `Mathlib.Analysis.Calculus.Deriv.Basic` and
`Mathlib.LinearAlgebra.CrossProduct`; the latter supplies the coordinate and cross-product API.

The separately elaborated mutations remove positive curvature, remove unit speed, and reverse
the torsion convention. They are deliberately distinct statement shapes, not theorems claimed
false. Endpoint behavior is excluded by the open-domain hypothesis; zero curvature is excluded
because the principal normal is undefined there.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the existing
pinned `.lake` artifacts; no dependency operation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0162/Statement.lean` | 0 | target and three structural mutations elaborated; explicit target expression printed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0162/Statement.lean lean-toolchain lake-manifest.json` | 0 | `a3b728...73c2`, `651c8a...1d2`, `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups and 1546 uniform-L0 targets; skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0162` | 0 | rank 661, planned, L0/rework-required, theorem incomplete |

This is statement-only evidence pending master acceptance. Source pinpointing remains open for the
anchor-audit phase, and no proof, kernel closure, audit completion, or theorem completion is
claimed.
