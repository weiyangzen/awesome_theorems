# Statement validation record

Item: `S56-M-1012-STATEMENT`  
Base revision: `688f1e598934169a383f99a0cde9d998eca49972`

## Frozen target

`Stage1Instances.THM_M_1012.LevyContinuityKnownLimitTarget` is the intake-selected known-limit
equivalence on an arbitrary finite-dimensional real inner product space. The specified limit
`mu0` is universally bound. Weak convergence uses the topology on `ProbabilityMeasure E`, and the
right side requires characteristic-function convergence at every `t : E`, including zero.

The direct imports are `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic` and
`Mathlib.MeasureTheory.Measure.ProbabilityMeasure`: the former supplies `charFun`, while the latter
supplies `ProbabilityMeasure` and its weak-convergence topology. Neither alone elaborates the
target, and the proof-bearing `LevyConvergence` module is intentionally absent. The checked
`target_iff_expanded` transport verifies the binder-explicit encoding.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` with the
existing pinned Lake environment; no dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1012/Statement.lean` | 0 | target, checked transport, four mutations, and zero-dimensional boundary target elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1012/check_statement.py` | 0 | expression SHA-256 `1baa1f00d8cab4be7e0121d56f06dd7c6b5455d7a87d5befd7604f629c44a618`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1012` | 0 | rank 291, planned, L0/rework-required, theorem incomplete |

## Mutation and status boundary

The validator fingerprints Lean's explicit elaborated expression and distinguishes removal of the
finite-dimensional hypothesis, specialization of the domain to `Real`, existential rebinding of
the limit measure, and exclusion of frequency zero. The separately elaborated
`zeroDimensionalBoundary` confirms that no positive-dimension premise was introduced.

This node proposes only `M3`: it freezes and elaborates a statement and supplies no proof credit.
Primary-source review, anchor audit, proof, axiom/trust closure, hermetic replay, and independent
verification remain open. No theorem-completion claim is made.
