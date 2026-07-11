# THM-M-1013 rev-5.6 intake

This directory is the new rev-5.6 `planned` instance for the Cramer-Wold theorem (the
convergence device). It inherits no proof credit from the source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | weak convergence of Borel probability measures on finite-dimensional real coordinate space, characterized by every real linear projection | Exact Lean encoding and expression fingerprint belong to the statement phase |
| Forward direction | weak convergence is preserved by each continuous map `x -> t dot x` | Architecture only; no theorem invocation is credited |
| Reverse direction | convergence of all one-dimensional projections determines multivariate weak convergence | Architecture only; tightness and characteristic-function routes remain candidates |
| Quantification | every dimension `d : Nat`, sequence index `n : Nat`, limit probability measure, and coefficient vector `t` | Whether `Fin d -> Real`, Euclidean space, or an equivalent finite-dimensional space is canonical remains open |
| Boundary cases | `d = 0`, zero projection, repeated/degenerate measures | Must be mutation-tested during statement work, not silently excluded |
| Foundations | Lean 4 kernel, pinned mathlib, classical measure/topology policy | Toolchain, imports, axioms, and dependency fingerprints remain open |

The source statement, formal candidates, domains, and unresolved equivalence choices are frozen in
`intake.json` and cross-referenced in `source_statement_crosswalk.md`. The initial proof-package
scope is: statement normalization; continuous-projection implication; reverse projection device;
source and Lean anchor audit; checked composition into the biconditional.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: no canonical elaborated expression, environment fingerprint,
checked transports, or mutation results exist yet. This intake is not theorem completion.

## Validation

The exact intake-only checks and results are recorded in `validation.md`. They establish target
membership, standard consistency, JSON syntax, and dossier structure only; no Lean proof is claimed.
