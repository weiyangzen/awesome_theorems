# THM-M-0544 rev-5.6 intake

This is a new rev-5.6 `planned` instance for the Hodge theorem. The legacy slot and its abstract
Lean packages are discovery inputs only and carry no accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every degree on a smooth, compact, oriented Riemannian manifold: each real de Rham cohomology class has exactly one harmonic representative | Exact regularity, connectedness, boundary, coefficient, and universe choices remain statement-phase obligations |
| Equivalent form | The map from harmonic forms to real de Rham cohomology is an isomorphism | Equivalence to existence-and-uniqueness requires a checked Lean transport |
| Analytic layer | Hodge star, codifferential, Hodge Laplacian, ellipticity, orthogonal decomposition | No analytic theorem is credited at intake |
| Cohomological layer | Smooth closed forms modulo exact forms and the harmonic-form class map | The legacy quotient package is only an API-shape candidate |
| Boundary exclusions | Manifolds without boundary; compactness and orientation are explicit | Boundary/noncompact variants and twisted/complex coefficients are excluded, not silently generalized |
| Foundations | Lean 4 kernel and pinned mathlib under a later declared classical/choice/quotient policy | Toolchain, imports, axioms, TCB, and computation profiles remain open |

The claim is the classical harmonic-representative theorem, not merely the weaker fact that a
packaged harmonic form determines some abstract quotient class. Candidate formal surfaces and the
source mismatch are recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: the repository has only abstract interfaces whose premise fields can
contain the desired conclusion, not a canonical manifold-level target. No proof completion is
claimed.

## Validation

The commands and exact outcomes in `validation.md` validate target membership, repository
structure, dossier JSON, and local references only.
