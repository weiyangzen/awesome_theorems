# Statement evidence

Item: `S56-M-1013-STATEMENT`  
Base revision: `2f6e19989b487204f2450ca715a29105beb445a7`

## Frozen target

`Statement.lean` freezes the convergence-device formulation as a biconditional: for every
`d : Nat`, sequence `mu : Nat -> ProbabilityMeasure (EuclideanSpace Real (Fin d))`, and limit
`mu0`, weak convergence of `mu` to `mu0` holds if and only if every pushforward under
`x |-> inner Real x t` converges weakly. The coefficient vector `t` is universally quantified.
Dimension zero, the zero coefficient, and degenerate measures are not excluded.

The random-vector formulation is not substituted for this measure-level root. Its equivalence via
laws remains downstream work. The historical one-way `MeasureStatementShape` is also not adopted,
because it drops the forward half of the canonical biconditional.

## Imports and transport

The direct imports are `Mathlib.MeasureTheory.Measure.LevyConvergence`, which supplies the topology
on `ProbabilityMeasure`, and `Mathlib.Analysis.InnerProductSpace.PiL2`, which supplies the chosen
finite Euclidean coordinate model. `canonicalStatement_iff` is an `Iff.rfl` unfolding witness; it
checks binder order, projection maps, and the biconditional without proving Cramer-Wold.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1013/Statement.lean` | 0 | Lean 4.29.0 elaborated and printed the canonical expression |
| `python3 Stage1_Instances/THM-M-1013/check_statement.py` | 0 | expression SHA-256 `8cae819c65fe669e84ad89391b427da3df7e3475835b7c2063cb3c7bbb6edd1b`; reverse-only, single-projection, and positive-dimension mutations distinguished; mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1013` | 0 | rank 292, planned, theorem completion false |
| `python3 -m json.tool Stage1_Instances/THM-M-1013/intake.json >/dev/null` | 0 | updated structured record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1013 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This receipt supports exact statement elaboration only, pending master acceptance. It supplies no
source acceptance, anchor-audit credit, proof or theorem closure, hermetic replay, independent
validation, or theorem-completion claim.
