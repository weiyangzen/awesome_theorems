# THM-M-1289 Historical Intake

This is the `planned` instance for the Aubin-Talenti functions. The broad catalog label is made
executable by selecting the standard positive critical bubble with the normalization for
`-Delta U = U^((n+2)/(n-2))`. Exact Lean syntax is deliberately deferred to the statement node.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Parameters | integer `n >= 3`, center `a` in `R^n`, scale `lambda > 0` | low dimensions and nonpositive scales excluded |
| Explicit function | normalized radial translate/dilate recorded in `intake.json` | real-power and Euclidean-norm encoding not selected |
| PDE property | positivity, smoothness, and the pointwise critical equation | no weak-solution or boundary-domain variant |
| Variational property | membership in the homogeneous Sobolev class and equality in the sharp inequality | sharp-constant convention needs checked alignment |
| Classification | not part of the root | “all optimizers are bubbles” is a stronger theorem |
| Foundations | Lean 4 kernel and pinned mathlib | exact toolchain, imports, axioms, and TCB remain open |

The source/component relationship is recorded in `source_statement_crosswalk.md`. Later nodes must
separately elaborate the statement, audit formal anchors, freeze obligations, and integrate and
replay an admitted exact machine proof. New root work requires an active reviewed frontier
exception; validation then checks kernel and provenance closure.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
the exact-statement gate: there is no Lean declaration, normalized expression hash, environment
fingerprint, checked normalization transport, or mutation test. The theorem is not complete.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They establish manifest
membership, repository structural consistency, JSON syntax, and whitespace integrity only.
