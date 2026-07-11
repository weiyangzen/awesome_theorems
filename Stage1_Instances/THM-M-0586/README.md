# THM-M-0586 rev-5.6 intake

This directory is the `planned` intake for the high-dimensional generalized Poincare conjecture.
It freezes the intended human claim as the topological classification of a closed smooth
`n`-manifold homotopy equivalent to `S^n`, for `n >= 5`, while leaving the precise category,
regularity conventions, and primary-source theorem wording to the statement phase.

The legacy Lean module is discovery input only. Its abstract terminal package receives no rev-5.6
statement or proof credit. The provisional root vector is `[H2, M4, R4]`; no elaborated canonical
target, audit completion, or theorem completion is claimed. The scope map, source crosswalk, and
open task DAG define the downstream work. Validation commands and results are in `validation.md`.

## Statement phase handoff

The statement phase proposes `Stage1Instances.THMM0586.HighDimensionalPoincareTarget` in
`Statement.lean` as the exact intake-selected Lean target. It elaborates from the sole direct
import `Mathlib.Geometry.Manifold.PoincareConjecture`; `statement.json` records the explicit
expression hash, environment fingerprint, checked implication from the broader mathlib statement
shape, structural mutations, and the included dimension-five boundary. Exact commands and results
are recorded in `statement-validation.md`.

This is statement-only work pending master acceptance. It does not upgrade `H2`, prove the target,
or claim audit/theorem completion.
