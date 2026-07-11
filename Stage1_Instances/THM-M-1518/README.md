# THM-M-1518 rev-5.6 intake

This is a `planned` dossier for Hamilton's stationary-action principle. The Chinese legacy label
literally says "least action", but unrestricted action extrema need not be minima. The frozen scope
is therefore the standard fixed-endpoint implication from stationary first variation to the
Euler-Lagrange equation. Changing that implication requires re-intake rather than silently swapping
in a minimization theorem.

## Scope map

| Surface | Included at intake | Boundary / open work |
|---|---|---|
| Model | Finite-dimensional real configuration space, initially Euclidean | Manifolds and infinite-dimensional systems excluded |
| Data | Compact nondegenerate time interval, `C2` Lagrangian and path | Exact Lean regularity and integral APIs are not selected |
| Variations | Sufficiently smooth variations vanishing at both endpoints | The test-function space and first-variation derivative need exact definitions |
| Root implication | Stationary action implies the Euler-Lagrange equation in the interval interior | Converse and boundary/transversality conditions excluded |
| Semantics | Stationary action, not universal least action | A minimum theorem would require extra hypotheses and a separate target |
| Foundations | Lean 4 kernel and pinned mathlib | Imports, toolchain, axioms, TCB, and environment fingerprint remain open |

## Open task DAG

`STMT-MODEL` freezes scalar/configuration types and interval conventions. `STMT-ACTION` defines the
action and admissible variations. `STMT-FIRST-VAR` states stationarity without hidden analytic
assumptions. `STMT-EL` fixes the pointwise Euler-Lagrange conclusion. `STMT-EXACT` composes these into
an elaborated target and mutation-tests endpoints, regularity, quantifier scope, and stationary
versus minimum semantics. In parallel after statement acceptance, `SRC-PINPOINT` audits the source
formulas and `ANCHOR-AUDIT` searches immutable Lean candidates. No task has proof credit at intake.

The provisional root vector is `[H2, M4, R4]`. The first failed theorem gate is exact statement:
there is no Lean declaration, normalized expression hash, checked transport, environment
fingerprint, or mutation record. The theorem and its audit are not complete.

