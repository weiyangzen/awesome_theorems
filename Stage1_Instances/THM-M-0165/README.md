# THM-M-0165 rev-5.6 intake

This directory is the `planned` instance for the Morse index theorem for geodesics. The target is
the fixed-endpoint Riemannian version: the index of the geodesic's index form equals the total
multiplicity of interior conjugate points, with a nonconjugate terminal endpoint.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | equality of index-form index and the finite sum of interior conjugate multiplicities | no Lean expression or fingerprint yet |
| Geometric objects | finite-dimensional Riemannian manifold, geodesic segment, Jacobi fields, conjugate points | exact mathlib representations and smoothness assumptions are open |
| Analytic objects | endpoint-zero variation fields and the second-variation index form | Sobolev versus piecewise-smooth completion is not selected |
| Boundary | terminal point is not conjugate; summation excludes both endpoints | endpoint-nullity and constant-geodesic variants are excluded |
| Bridge | energy Hessian index equals index-form index | candidate obligation only |
| Foundations | Lean 4 kernel and pinned mathlib under the rev-5.6 trust policy | environment, imports, classical dependencies, and spectral machinery are open |

The initial proof architecture remains: define Jacobi/conjugacy data, establish the second variation
and index form, split at conjugate instants, prove the local index jump equals multiplicity, and sum
the jumps. These are discovery nodes, not accepted obligations or proof coverage.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: the repository provides no identified declaration, elaborated target,
environment fingerprint, checked encoding bridge, or mutation tests. The theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish manifest membership, standard
consistency, JSON syntax, and dossier-local integrity only.
