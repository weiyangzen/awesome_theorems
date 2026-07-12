# THM-M-1013 rev-5.6 intake

This directory is the new rev-5.6 `planned` instance for the Cramer-Wold theorem (the
convergence device). It inherits no proof credit from the source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | weak convergence of Borel probability measures on finite-dimensional real coordinate space, characterized by every real linear projection | Frozen as `Stage1Instances.THM_M_1013.StatementShape` |
| Forward direction | weak convergence is preserved by each continuous map `x -> t dot x` | Architecture only; no theorem invocation is credited |
| Reverse direction | convergence of all one-dimensional projections determines multivariate weak convergence | Architecture only; tightness and characteristic-function routes remain candidates |
| Quantification | every dimension `d : Nat`, sequence index `n : Nat`, limit probability measure, and coefficient vector `t` | Canonical space is `EuclideanSpace Real (Fin d)` |
| Boundary cases | `d = 0`, zero projection, repeated/degenerate measures | Included; the positive-dimension mutation is structurally distinct |
| Foundations | Lean 4 kernel, pinned mathlib, classical measure/topology policy | Lean 4.29.0 and mathlib `8a178386...a95` fingerprinted in `intake.json` |

The source statement, formal candidates, domains, and unresolved equivalence choices are frozen in
`intake.json` and cross-referenced in `source_statement_crosswalk.md`. The initial proof-package
scope is: statement normalization; continuous-projection implication; reverse projection device;
source and Lean anchor audit; checked composition into the biconditional.

## Statement verdict

Lifecycle remains `planned`; provisional root vector remains `[H1, M3, R3]`. The exact statement
is locally elaborated, its definitional unfolding is checked by `canonicalStatement_iff`, and three
scope mutations are distinguished. Master acceptance and every anchor, proof, validation, source,
and release gate remain open. This is not theorem completion.

## Validation

The exact commands and results are recorded in `statement-evidence.md`. They establish statement
elaboration only; no proof of `StatementShape` is claimed.
