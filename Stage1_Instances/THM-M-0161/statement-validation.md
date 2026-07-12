# Statement validation record

Item: `S56-M-0161-STATEMENT`  
Base revision: `93c99233108bb249d1bca807a3a56a2b63e0cd54`

## Frozen target

`Stage1Instances.THM_M_0161.FundamentalTheoremOfSpaceCurvesTarget` freezes the nonempty open-
interval formulation over `E3 := Fin 3 -> Real`. Prescribed curvature and signed torsion are
differentiable on the interval, curvature is positive, and the resulting curve is `C3` and unit
speed. The conclusion includes existence and uniqueness on the interval under a determinant-one
Euclidean rigid motion. Explicit Euclidean dot product and length definitions prevent accidental
use of the Pi space's supremum norm.

The two direct imports are `Mathlib.Analysis.Calculus.ContDiff.Defs` and
`Mathlib.LinearAlgebra.CrossProduct`. No theorem proof, source proof, formal anchor, or axiom is
introduced.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0161/Statement.lean` | 0 | exact target and all four structural mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0161/check_statement.py` | 0 | expression SHA-256 `c140d1d15da39c41b3cc430e5119c4ec5194856f15481e2040cc0ea710c47f82`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0161/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `82f74a...3060`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0161` | 0 | no whitespace errors |

The validator kills mutations that admit zero curvature, omit existence, permit reflections, or
move the coefficient hypotheses to a closed interval. This is statement-only evidence pending
master acceptance; all later nodes and theorem completion remain open.
