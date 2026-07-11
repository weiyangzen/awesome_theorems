# THM-M-0110: Kodaira vanishing theorem

This directory is the rev-5.6 `planned` intake instance. It adopts the standard algebraic
characteristic-zero formulation provisionally; the dependent statement phase must elaborate and
mutation-test it before it becomes canonical machine evidence.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Smooth projective variety `X` over a characteristic-zero field, ample invertible sheaf `L`, and `H^i(X, omega_X tensor L) = 0` for `i > 0` | Prose target only; no normalized Lean expression or fingerprint |
| Object model | structure morphism, smoothness, projectivity, line bundle, ampleness, canonical/dualizing sheaf | Exact mathlib representations remain a statement-phase decision |
| Cohomology | derived/sheaf cohomology object and categorical zero predicate | Degree convention and comparison to classical groups remain open |
| Transport | dual form `H^i(X,L^{-1}) = 0` for `i < dim X` | Requires checked Serre-duality and dimension/index transports |
| Historical form | compact Kahler/positive line-bundle analytic theorem | Outside canonical credit unless an explicit comparison bridge is checked |
| Exclusions | positive characteristic, singular/nonprojective varieties, degree zero, nef-only bundles | No broadened generalization or special case may substitute for the root |
| Trust | Lean 4 kernel and pinned mathlib | Foundation, TCB, imports, and environment fingerprints remain open |

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The statement node must settle the scheme/variety model, exact canonical sheaf construction,
cohomology functor, universe constraints, and checked alternate transports. The anchor audit must
re-audit the legacy `S1_M_034.lean` file without inheriting any proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate. This intake is self-tested as a dossier, but the theorem is not
complete and no kernel closure is claimed.
