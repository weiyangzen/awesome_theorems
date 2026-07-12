# THM-M-0164 rev-5.6 intake

This directory is the `planned` dossier for the forward Jacobi-field theorem. The Stage0 wording,
"the second derivative of a geodesic variation," is frozen here as the standard claim that the
variation field of a smooth variation through geodesics satisfies the Jacobi equation. The converse
realization theorem and second-variation formulas are related results, not silent additions to the
root.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | a geodesic variation field satisfies `D_t^2 J + R(J, gamma') gamma' = 0` | no Lean expression or expression fingerprint yet |
| Ambient geometry | finite-dimensional Riemannian manifold with its Levi-Civita connection | exact model, universes, regularity, and instances remain open |
| Variation | a sufficiently smooth two-parameter map whose longitudinal curves are geodesics | interval and endpoint conventions remain open |
| Differential identities | interchange of covariant variation derivatives, geodesic equation, curvature commutator | future typed obligations only |
| Convention boundary | curvature tensor argument order and sign | must be frozen and mutation-tested before statement credit |
| Exclusions | converse realization, conjugate points, boundary uniqueness, second variation, Morse index theorem | each is a distinct theorem or downstream application |
| Foundations | Lean 4 kernel and the repository-pinned mathlib | imports, TCB, axioms, and dependency closure remain open |

The anticipated proof architecture is: define the coordinate vector fields of the variation, use
torsion-freeness to interchange the first covariant derivatives, commute the next pair using the
curvature identity, and use the geodesic equation for every longitudinal curve. This is a scope map,
not a frozen obligation registry or proof-coverage claim.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The statement phase must select exact parameter domains and regularity, inspect the pinned manifold
and connection APIs, elaborate the root, serialize its environment, and mutation-test the geodesic
hypothesis, variation-field definition, parameter scope, dimension/domain, and curvature sign.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R3]`. `H1` records a standard
published proof family whose edition/page/assumption/errata crosswalk is not yet accepted. `M4`
records that intake has identified no exact repo-local Lean closure. The first failed theorem gate is
the exact Lean statement gate. The theorem is not complete.

## Validation

The commands and exact results in `validation.md` establish target membership, repository-standard
consistency, JSON syntax, and dossier-local integrity only. They do not elaborate or prove the
Jacobi equation.
